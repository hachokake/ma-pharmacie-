"""
Services métier pour la pharmacie
Contient toute la logique métier complexe
"""

from django.db import transaction
from django.db.models import Sum, F, Q
from django.utils import timezone
from decimal import Decimal
from .models import (
    Medicament, LotMedicament, MouvementStock, Vente, ItemVente,
    Client, Prescription, LignePrescription, Inventaire, LigneInventaire,
    SessionCaisse
)


class StockService:
    """Service de gestion des stocks"""
    
    @staticmethod
    def verifier_disponibilite(medicament, quantite_demandee):
        """
        Vérifie si la quantité demandée est disponible
        Retourne (disponible: bool, message: str, lots_disponibles: list)
        """
        stock_disponible = medicament.quantite_stock
        
        if stock_disponible < quantite_demandee:
            return False, f"Stock insuffisant. Disponible: {stock_disponible}", []
        
        # Récupérer les lots disponibles (FEFO: First Expired First Out)
        lots = LotMedicament.objects.filter(
            medicament=medicament,
            actif=True,
            quantite__gt=0
        ).order_by('date_expiration', 'date_reception')
        
        return True, "Stock disponible", list(lots)
    
    @staticmethod
    @transaction.atomic
    def prelever_stock(medicament, quantite, utilisateur, vente=None, reference=""):
        """
        Prélève le stock en respectant le FEFO
        Crée les mouvements de stock associés
        Retourne la liste des lots prélevés
        """
        disponible, message, lots = StockService.verifier_disponibilite(medicament, quantite)
        
        if not disponible:
            raise ValueError(message)
        
        quantite_restante = quantite
        lots_preleves = []
        
        for lot in lots:
            if quantite_restante <= 0:
                break
            
            quantite_a_prelever = min(quantite_restante, lot.quantite)
            quantite_avant = lot.quantite
            
            # Mettre à jour le lot
            lot.quantite -= quantite_a_prelever
            lot.save()
            
            # Créer le mouvement de stock
            mouvement = MouvementStock.objects.create(
                lot=lot,
                medicament=medicament,
                type_mouvement='SORTIE',
                quantite=quantite_a_prelever,
                quantite_avant=quantite_avant,
                quantite_apres=lot.quantite,
                utilisateur=utilisateur,
                cout_unitaire=lot.prix_achat_unitaire,
                vente=vente,
                reference_document=reference
            )
            
            lots_preleves.append({
                'lot': lot,
                'quantite': quantite_a_prelever,
                'mouvement': mouvement
            })
            
            quantite_restante -= quantite_a_prelever
        
        # Mettre à jour le stock total du médicament
        medicament.recalculer_stock_total()
        
        return lots_preleves
    
    @staticmethod
    @transaction.atomic
    def ajouter_stock(medicament, lot_data, utilisateur, commande=None):
        """
        Ajoute un nouveau lot au stock
        lot_data: dict contenant les informations du lot
        """
        lot = LotMedicament.objects.create(
            medicament=medicament,
            numero_lot=lot_data['numero_lot'],
            date_fabrication=lot_data['date_fabrication'],
            date_expiration=lot_data['date_expiration'],
            quantite_initiale=lot_data['quantite'],
            quantite=lot_data['quantite'],
            prix_achat_unitaire=lot_data['prix_achat_unitaire'],
            prix_vente_unitaire=lot_data['prix_vente_unitaire'],
            fournisseur=lot_data.get('fournisseur'),
            commande=commande
        )
        
        # Créer le mouvement de stock
        MouvementStock.objects.create(
            lot=lot,
            medicament=medicament,
            type_mouvement='ENTREE',
            quantite=lot_data['quantite'],
            quantite_avant=0,
            quantite_apres=lot_data['quantite'],
            utilisateur=utilisateur,
            cout_unitaire=lot_data['prix_achat_unitaire'],
            commande=commande,
            reference_document=lot_data.get('reference_document', '')
        )
        
        # Mettre à jour le stock total
        medicament.recalculer_stock_total()
        
        return lot
    
    @staticmethod
    def get_lots_expires():
        """Retourne tous les lots expirés"""
        return LotMedicament.objects.filter(
            date_expiration__lt=timezone.now().date(),
            actif=True,
            quantite__gt=0
        ).select_related('medicament', 'fournisseur')
    
    @staticmethod
    def get_lots_proche_expiration(jours=90):
        """Retourne les lots qui expirent dans X jours"""
        from datetime import timedelta
        date_limite = timezone.now().date() + timedelta(days=jours)
        
        return LotMedicament.objects.filter(
            date_expiration__lte=date_limite,
            date_expiration__gte=timezone.now().date(),
            actif=True,
            quantite__gt=0
        ).select_related('medicament', 'fournisseur').order_by('date_expiration')
    
    @staticmethod
    def calculer_valeur_stock_total():
        """Calcule la valeur totale du stock"""
        lots = LotMedicament.objects.filter(actif=True, quantite__gt=0)
        
        valeur_achat = sum(lot.valeur_stock() for lot in lots)
        valeur_vente = sum(lot.quantite * lot.prix_vente_unitaire for lot in lots)
        marge = valeur_vente - valeur_achat
        
        return {
            'valeur_achat': valeur_achat,
            'valeur_vente': valeur_vente,
            'marge_potentielle': marge,
            'taux_marge': (marge / valeur_achat * 100) if valeur_achat > 0 else 0
        }


class VenteService:
    """Service de gestion des ventes"""
    
    @staticmethod
    @transaction.atomic
    def creer_vente(items_data, client, vendeur, methode_paiement, 
                   caisse=None, session_caisse=None, prescription=None, remarques=""):
        """
        Crée une vente complète avec gestion du stock
        items_data: liste de dict {'medicament': obj, 'quantite': int, 'prix': decimal}
        """
        # Vérifier la disponibilité de tous les items
        for item in items_data:
            disponible, message, _ = StockService.verifier_disponibilite(
                item['medicament'], 
                item['quantite']
            )
            if not disponible:
                raise ValueError(f"{item['medicament'].nom}: {message}")
        
        # Créer la vente
        vente = Vente.objects.create(
            client=client,
            vendeur=vendeur,
            methode_paiement=methode_paiement,
            caisse=caisse,
            session_caisse=session_caisse,
            prescription=prescription,
            remarques=remarques
        )
        
        # Créer les items et prélever le stock
        for item_data in items_data:
            medicament = item_data['medicament']
            quantite = item_data['quantite']
            prix = item_data.get('prix', medicament.prix_unitaire)
            
            # Prélever le stock (FEFO)
            lots_preleves = StockService.prelever_stock(
                medicament, 
                quantite, 
                vendeur, 
                vente=vente,
                reference=f"Vente {vente.numero_facture}"
            )
            
            # Créer l'item de vente (un par lot si multiple)
            for lot_info in lots_preleves:
                ItemVente.objects.create(
                    vente=vente,
                    medicament=medicament,
                    lot=lot_info['lot'],
                    quantite=lot_info['quantite'],
                    prix_unitaire=prix
                )
        
        # Calculer le total
        vente.calculer_total()
        
        # Si paiement comptant, marquer comme payé
        if vente.type_vente == 'COMPTANT':
            vente.montant_paye = vente.montant_total
            vente.montant_restant = 0
            vente.save()
        
        return vente
    
    @staticmethod
    @transaction.atomic
    def annuler_vente(vente, utilisateur, motif=""):
        """
        Annule une vente et remet le stock
        """
        if not vente.peut_etre_annulee():
            raise ValueError("Cette vente ne peut plus être annulée")
        
        # Remettre le stock
        for item in vente.items.all():
            if item.lot:
                quantite_avant = item.lot.quantite
                item.lot.quantite += item.quantite
                item.lot.save()
                
                # Créer mouvement de stock
                MouvementStock.objects.create(
                    lot=item.lot,
                    medicament=item.medicament,
                    type_mouvement='RETOUR_CLIENT',
                    quantite=item.quantite,
                    quantite_avant=quantite_avant,
                    quantite_apres=item.lot.quantite,
                    utilisateur=utilisateur,
                    cout_unitaire=item.lot.prix_achat_unitaire,
                    vente=vente,
                    reference_document=f"Annulation vente {vente.numero_facture}",
                    remarque=motif
                )
                
                item.medicament.recalculer_stock_total()
        
        vente.statut = 'ANNULEE'
        vente.remarques += f"\n[ANNULÉE le {timezone.now()}] {motif}"
        vente.save()
        
        return vente
    
    @staticmethod
    def verifier_prescription_requise(items_medicaments):
        """
        Vérifie si une prescription est requise pour les médicaments
        Retourne (requis: bool, medicaments_requérant_prescription: list)
        """
        medicaments_requis = []
        
        for medicament in items_medicaments:
            if not medicament.peut_etre_vendu_sans_ordonnance():
                medicaments_requis.append(medicament)
        
        return len(medicaments_requis) > 0, medicaments_requis


class PrescriptionService:
    """Service de gestion des prescriptions"""
    
    @staticmethod
    @transaction.atomic
    def creer_prescription(medecin, patient, lignes_data, receptionniste, 
                          date_validite=None, fichier_scan=None):
        """
        Crée une prescription
        lignes_data: liste de dict {'medicament': obj, 'posologie': str, 'quantite': int}
        """
        from datetime import timedelta
        
        # Date de validité par défaut: 3 mois
        if not date_validite:
            date_validite = timezone.now().date() + timedelta(days=90)
        
        # Générer numéro d'ordonnance
        date_str = timezone.now().strftime('%Y%m%d')
        last_prescription = Prescription.objects.filter(
            numero_ordonnance__startswith=f'ORD-{date_str}'
        ).order_by('-numero_ordonnance').first()
        
        if last_prescription:
            last_num = int(last_prescription.numero_ordonnance.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        numero = f'ORD-{date_str}-{new_num:04d}'
        
        # Créer la prescription
        prescription = Prescription.objects.create(
            numero_ordonnance=numero,
            medecin=medecin,
            patient=patient,
            date_prescription=timezone.now().date(),
            date_validite=date_validite,
            receptionniste=receptionniste,
            fichier_scan=fichier_scan
        )
        
        # Créer les lignes
        for ligne_data in lignes_data:
            LignePrescription.objects.create(
                prescription=prescription,
                medicament=ligne_data['medicament'],
                posologie=ligne_data['posologie'],
                quantite_prescrite=ligne_data['quantite'],
                substitution_autorisee=ligne_data.get('substitution_autorisee', True)
            )
        
        return prescription
    
    @staticmethod
    def verifier_prescription_complete(prescription):
        """Vérifie si toutes les lignes sont délivrées"""
        lignes = prescription.lignes.all()
        
        if not lignes:
            return False
        
        return all(ligne.est_completement_delivree() for ligne in lignes)


class InventaireService:
    """Service de gestion des inventaires"""
    
    @staticmethod
    @transaction.atomic
    def creer_inventaire(responsable):
        """Crée un nouvel inventaire"""
        from datetime import datetime
        
        # Générer référence
        date_str = datetime.now().strftime('%Y%m%d')
        reference = f'INV-{date_str}-{Inventaire.objects.filter(reference__startswith=f"INV-{date_str}").count() + 1:03d}'
        
        inventaire = Inventaire.objects.create(
            reference=reference,
            date_debut=timezone.now(),
            responsable=responsable,
            statut='EN_COURS'
        )
        
        # Créer les lignes pour tous les lots actifs
        lots = LotMedicament.objects.filter(actif=True, quantite__gt=0).select_related('medicament')
        
        for lot in lots:
            LigneInventaire.objects.create(
                inventaire=inventaire,
                lot=lot,
                medicament=lot.medicament,
                quantite_theorique=lot.quantite,
                quantite_reelle=0,  # À remplir lors du comptage
                prix_unitaire=lot.prix_achat_unitaire,
                compteur=responsable
            )
        
        return inventaire
    
    @staticmethod
    @transaction.atomic
    def valider_inventaire(inventaire, valideur):
        """Valide un inventaire et ajuste les stocks"""
        if inventaire.statut != 'TERMINE':
            raise ValueError("L'inventaire doit être terminé avant validation")
        
        # Ajuster les stocks selon les écarts
        for ligne in inventaire.lignes.filter(ajustement_effectue=False):
            if ligne.ecart != 0:
                lot = ligne.lot
                quantite_avant = lot.quantite
                lot.quantite = ligne.quantite_reelle
                lot.save()
                
                # Créer mouvement de stock
                type_mouvement = 'INVENTAIRE_PLUS' if ligne.ecart > 0 else 'INVENTAIRE_MOINS'
                
                MouvementStock.objects.create(
                    lot=lot,
                    medicament=ligne.medicament,
                    type_mouvement=type_mouvement,
                    quantite=abs(ligne.ecart),
                    quantite_avant=quantite_avant,
                    quantite_apres=lot.quantite,
                    utilisateur=valideur,
                    cout_unitaire=ligne.prix_unitaire,
                    reference_document=f"Inventaire {inventaire.reference}",
                    remarque=f"Ajustement inventaire: {ligne.commentaire}"
                )
                
                ligne.ajustement_effectue = True
                ligne.save()
                
                # Recalculer stock total
                ligne.medicament.recalculer_stock_total()
        
        # Mettre à jour l'inventaire
        inventaire.statut = 'VALIDE'
        inventaire.valideur = valideur
        inventaire.date_validation = timezone.now()
        inventaire.calculer_statistiques()
        
        return inventaire


class CaisseService:
    """Service de gestion des caisses"""
    
    @staticmethod
    @transaction.atomic
    def ouvrir_session(caisse, caissier, fond_ouverture):
        """Ouvre une nouvelle session de caisse"""
        # Vérifier qu'il n'y a pas déjà une session ouverte
        session_active = caisse.session_active()
        if session_active:
            raise ValueError(f"Une session est déjà ouverte pour cette caisse par {session_active.caissier}")
        
        session = SessionCaisse.objects.create(
            caisse=caisse,
            caissier=caissier,
            date_ouverture=timezone.now(),
            fond_caisse_ouverture=fond_ouverture
        )
        
        return session
    
    @staticmethod
    @transaction.atomic
    def fermer_session(session, fond_fermeture):
        """Ferme une session de caisse"""
        if session.date_fermeture:
            raise ValueError("Cette session est déjà fermée")
        
        session.date_fermeture = timezone.now()
        session.fond_caisse_fermeture = fond_fermeture
        
        # Calculer les totaux
        session.calculer_totaux()
        session.calculer_ecart()
        
        return session


class RapportService:
    """Service de génération de rapports"""
    
    @staticmethod
    def rapport_ventes_periode(date_debut, date_fin):
        """Génère un rapport des ventes pour une période"""
        ventes = Vente.objects.filter(
            date_vente__range=[date_debut, date_fin],
            statut='VALIDEE'
        ).select_related('client', 'vendeur', 'caisse')
        
        total_ventes = ventes.aggregate(
            nombre=Sum('id'),
            montant_total=Sum('montant_total'),
            montant_paye=Sum('montant_paye'),
            montant_restant=Sum('montant_restant')
        )
        
        # Par méthode de paiement
        par_methode = {}
        for methode, _ in Vente.METHODE_PAIEMENT_CHOICES:
            montant = ventes.filter(methode_paiement=methode).aggregate(
                total=Sum('montant_total')
            )['total'] or 0
            par_methode[methode] = montant
        
        # Par vendeur
        par_vendeur = ventes.values('vendeur__username').annotate(
            nombre_ventes=Sum('id'),
            montant_total=Sum('montant_total')
        ).order_by('-montant_total')
        
        return {
            'periode': {'debut': date_debut, 'fin': date_fin},
            'totaux': total_ventes,
            'par_methode_paiement': par_methode,
            'par_vendeur': list(par_vendeur),
            'nombre_ventes': ventes.count()
        }
    
    @staticmethod
    def rapport_stock_valeur():
        """Génère un rapport de la valeur du stock"""
        return StockService.calculer_valeur_stock_total()
    
    @staticmethod
    def rapport_medicaments_rotation():
        """Analyse la rotation des médicaments"""
        from django.db.models import Count
        from datetime import timedelta
        
        date_limite = timezone.now() - timedelta(days=90)
        
        # Médicaments les plus vendus
        plus_vendus = ItemVente.objects.filter(
            vente__date_vente__gte=date_limite,
            vente__statut='VALIDEE'
        ).values('medicament__nom').annotate(
            quantite_vendue=Sum('quantite'),
            nombre_ventes=Count('vente')
        ).order_by('-quantite_vendue')[:20]
        
        # Médicaments en stagnation
        medicaments_actifs = Medicament.objects.filter(actif=True, quantite_stock__gt=0)
        stagnants = []
        
        for med in medicaments_actifs:
            derniere_vente = ItemVente.objects.filter(
                medicament=med,
                vente__statut='VALIDEE'
            ).order_by('-vente__date_vente').first()
            
            if not derniere_vente or derniere_vente.vente.date_vente < date_limite:
                stagnants.append({
                    'medicament': med.nom,
                    'stock': med.quantite_stock,
                    'valeur': med.quantite_stock * med.prix_achat_ht,
                    'derniere_vente': derniere_vente.vente.date_vente if derniere_vente else None
                })
        
        return {
            'plus_vendus': list(plus_vendus),
            'stagnants': stagnants
        }
