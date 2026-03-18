from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont


class Categorie(models.Model):
    """Catégorie de médicaments"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.nom


class Medicament(models.Model):
    """Modèle pour les médicaments avec classification pharmaceutique complète"""
    
    # Choix de classification
    CLASSIFICATION_CHOICES = [
        ('LIBRE', 'Vente libre'),
        ('ORDONNANCE', 'Ordonnance obligatoire'),
        ('STUPEFIANT', 'Stupéfiant'),
        ('PSYCHOTROPE', 'Psychotrope'),
    ]
    
    FORME_GALENIQUE_CHOICES = [
        ('COMPRIME', 'Comprimé'),
        ('GELULE', 'Gélule'),
        ('SIROP', 'Sirop'),
        ('SUSPENSION', 'Suspension'),
        ('SOLUTION', 'Solution'),
        ('INJECTABLE', 'Injectable'),
        ('POMMADE', 'Pommade'),
        ('CREME', 'Crème'),
        ('GEL', 'Gel'),
        ('SUPPOSITOIRE', 'Suppositoire'),
        ('OVULE', 'Ovule'),
        ('COLLYRE', 'Collyre'),
        ('AEROSOL', 'Aérosol'),
        ('POUDRE', 'Poudre'),
        ('CAPSULE', 'Capsule'),
        ('PATCH', 'Patch'),
        ('AUTRE', 'Autre'),
    ]
    
    LISTE_STUPEFIANT_CHOICES = [
        ('', 'Non applicable'),
        ('I', 'Liste I'),
        ('II', 'Liste II'),
        ('III', 'Liste III'),
        ('IV', 'Liste IV'),
    ]
    
    # Informations de base
    nom = models.CharField(max_length=200, verbose_name="Nom commercial")
    dci = models.CharField(max_length=200, blank=True, verbose_name="DCI (Dénomination Commune Internationale)")
    description = models.TextField(blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='medicaments')
    
    # Classification et réglementation
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, default='LIBRE', 
                                     verbose_name="Classification réglementaire")
    liste_stupefiant = models.CharField(max_length=10, choices=LISTE_STUPEFIANT_CHOICES, blank=True,
                                       verbose_name="Liste stupéfiants/psychotropes")
    prescription_obligatoire = models.BooleanField(default=False, verbose_name="Prescription obligatoire")
    
    # Forme et dosage
    forme_galenique = models.CharField(max_length=20, choices=FORME_GALENIQUE_CHOICES, default='COMPRIME',
                                       verbose_name="Forme galénique")
    dosage = models.CharField(max_length=100, blank=True, verbose_name="Dosage/Concentration", 
                             help_text="Ex: 500mg, 10%, 100UI/ml")
    
    # Prix et marges
    prix_achat_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                        verbose_name="Prix d'achat HT")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de vente TTC")
    tva_taux = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Taux TVA (%)")
    marge_min = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, 
                                   verbose_name="Marge minimale (%)")
    marge_max = models.DecimalField(max_digits=5, decimal_places=2, default=50.00,
                                   verbose_name="Marge maximale (%)")
    
    # Stock (quantité globale - sera calculée à partir des lots)
    quantite_stock = models.IntegerField(default=0, verbose_name="Quantité totale en stock")
    seuil_alerte = models.IntegerField(default=10, help_text="Niveau de stock minimum avant alerte")
    
    # Informations supplémentaires
    date_expiration = models.DateField(verbose_name="Date d'expiration (lot principal)")
    numero_lot = models.CharField(max_length=100, blank=True, verbose_name="Numéro de lot principal")
    fabricant = models.CharField(max_length=200, blank=True)
    pays_origine = models.CharField(max_length=100, blank=True, verbose_name="Pays d'origine")
    numero_amm = models.CharField(max_length=100, blank=True, verbose_name="N° AMM (Autorisation de Mise sur le Marché)")
    code_barre = models.CharField(max_length=100, blank=True, unique=True)
    code_cip = models.CharField(max_length=20, blank=True, verbose_name="Code CIP", 
                               help_text="Code Identifiant de Présentation")
    
    # Métadonnées
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='medicaments_crees', verbose_name="Ajouté par")
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Médicament"
        verbose_name_plural = "Médicaments"
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['dci']),
            models.Index(fields=['code_barre']),
            models.Index(fields=['classification']),
        ]
    
    def __str__(self):
        return f"{self.nom} {self.dosage} - Stock: {self.quantite_stock}"
    
    def est_en_rupture(self):
        """Vérifie si le médicament est en rupture de stock"""
        return self.quantite_stock <= 0
    
    def necessite_alerte(self):
        """Vérifie si le stock est en dessous du seuil d'alerte"""
        return self.quantite_stock <= self.seuil_alerte
    
    def est_expire(self):
        """Vérifie si le médicament est expiré"""
        return self.date_expiration < timezone.now().date()
    
    def peut_etre_vendu_sans_ordonnance(self):
        """Vérifie si le médicament peut être vendu sans ordonnance"""
        return self.classification == 'LIBRE' and not self.prescription_obligatoire
    
    def calculer_marge_actuelle(self):
        """Calcule la marge actuelle en pourcentage"""
        if self.prix_achat_ht > 0:
            return ((self.prix_unitaire - self.prix_achat_ht) / self.prix_achat_ht) * 100
        return 0
    
    def get_prix_vente_ht(self):
        """Calcule le prix de vente HT"""
        if self.tva_taux > 0:
            return self.prix_unitaire / (1 + (self.tva_taux / 100))
        return self.prix_unitaire
    
    def recalculer_stock_total(self):
        """Recalcule le stock total à partir des lots"""
        total = self.lots.filter(actif=True).aggregate(
            total=Coalesce(Sum('quantite'), 0)
        )['total']
        self.quantite_stock = total
        self.save(update_fields=['quantite_stock'])
        return total


class Client(models.Model):
    """Modèle pour les clients avec gestion d'assurance"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    numero_carte_identite = models.CharField(max_length=50, blank=True, verbose_name="N° Carte d'identité")
    
    # Assurance
    assurance = models.ForeignKey('Assurance', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='clients', verbose_name="Assurance")
    numero_assure = models.CharField(max_length=50, blank=True, verbose_name="N° Assuré")
    taux_couverture = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                         verbose_name="Taux de couverture (%)",
                                         help_text="Pourcentage pris en charge par l'assurance")
    
    # Gestion des créances
    credit_autorise = models.BooleanField(default=False, verbose_name="Crédit autorisé")
    plafond_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        verbose_name="Plafond de crédit")
    
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom', 'prenom']
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['telephone']),
        ]
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    def get_credit_disponible(self):
        """Calcule le crédit encore disponible"""
        from django.db.models import Sum
        total_credit = self.ventes.filter(
            type_vente='CREDIT',
            montant_restant__gt=0
        ).aggregate(total=Sum('montant_restant'))['total'] or 0
        return self.plafond_credit - total_credit
    
    def a_des_impaye(self):
        """Vérifie si le client a des impayés"""
        return self.ventes.filter(montant_restant__gt=0).exists()


class Vente(models.Model):
    """Modèle pour les ventes avec gestion crédit et tiers-payant"""
    METHODE_PAIEMENT_CHOICES = [
        ('ESPECE', 'Espèces'),
        ('CARTE', 'Carte bancaire'),
        ('MOBILE', 'Mobile Money'),
        ('CHEQUE', 'Chèque'),
        ('MIXTE', 'Paiement mixte'),
    ]
    
    TYPE_VENTE_CHOICES = [
        ('COMPTANT', 'Comptant'),
        ('CREDIT', 'Crédit'),
        ('TIERS_PAYANT', 'Tiers payant (assurance)'),
    ]
    
    STATUT_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('VALIDEE', 'Validée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    # Informations de base
    numero_facture = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="N° Facture")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventes')
    date_vente = models.DateTimeField(default=timezone.now)
    vendeur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ventes')
    caisse = models.ForeignKey('Caisse', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='ventes', verbose_name="Caisse")
    session_caisse = models.ForeignKey('SessionCaisse', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='ventes')
    
    # Montants
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                       verbose_name="Montant total")
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                       verbose_name="Montant payé")
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                         verbose_name="Montant restant dû")
    remise = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                verbose_name="Remise accordée")
    
    # Type et méthode de paiement
    type_vente = models.CharField(max_length=20, choices=TYPE_VENTE_CHOICES, default='COMPTANT')
    methode_paiement = models.CharField(max_length=10, choices=METHODE_PAIEMENT_CHOICES, default='ESPECE')
    
    # Prescription (si applicable)
    prescription = models.ForeignKey('Prescription', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='ventes', verbose_name="Ordonnance")
    
    # Statut et métadonnées
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='VALIDEE')
    remarques = models.TextField(blank=True)
    date_echeance = models.DateField(null=True, blank=True, verbose_name="Date d'échéance (crédit)")
    
    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ['-date_vente']
        indexes = [
            models.Index(fields=['-date_vente']),
            models.Index(fields=['numero_facture']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"Vente #{self.numero_facture or self.id} - {self.date_vente.strftime('%d/%m/%Y %H:%M')} - {self.montant_total} FCFA"
    
    def save(self, *args, **kwargs):
        # Générer un numéro de facture automatiquement
        if not self.numero_facture:
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_vente = Vente.objects.filter(
                numero_facture__startswith=f'FAC-{date_str}'
            ).order_by('-numero_facture').first()
            
            if last_vente:
                last_num = int(last_vente.numero_facture.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.numero_facture = f'FAC-{date_str}-{new_num:04d}'
        
        super().save(*args, **kwargs)
    
    def calculer_total(self):
        """Calcule le montant total de la vente"""
        total = sum(item.sous_total for item in self.items.all())
        self.montant_total = total - self.remise
        self.montant_restant = self.montant_total - self.montant_paye
        self.save()
        return total
    
    def est_soldee(self):
        """Vérifie si la vente est complètement payée"""
        return self.montant_restant <= 0
    
    def peut_etre_annulee(self):
        """Vérifie si la vente peut être annulée"""
        from datetime import timedelta
        # Peut être annulée dans les 24h
        return timezone.now() - self.date_vente < timedelta(days=1)


class ItemVente(models.Model):
    """Détails des articles dans une vente avec traçabilité du lot"""
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='items')
    medicament = models.ForeignKey(Medicament, on_delete=models.PROTECT, related_name='ventes')
    lot = models.ForeignKey('LotMedicament', on_delete=models.SET_NULL, null=True, blank=True,
                           related_name='ventes', verbose_name="Lot")
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)
    remise_ligne = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                      verbose_name="Remise sur la ligne")
    
    class Meta:
        verbose_name = "Article de vente"
        verbose_name_plural = "Articles de vente"
    
    def __str__(self):
        return f"{self.medicament.nom} x{self.quantite}"
    
    def save(self, *args, **kwargs):
        """Calcule le sous-total"""
        self.sous_total = (self.quantite * self.prix_unitaire) - self.remise_ligne
        super().save(*args, **kwargs)


class Fournisseur(models.Model):
    """Modèle pour les fournisseurs"""
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    contact_personne = models.CharField(max_length=100, blank=True, help_text="Nom de la personne de contact")
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Commande(models.Model):
    """Modèle pour les commandes aux fournisseurs"""
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT, related_name='commandes')
    date_commande = models.DateTimeField(default=timezone.now)
    date_livraison_prevue = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarques = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"Commande #{self.id} - {self.fournisseur.nom} - {self.get_statut_display()}"


class LotMedicament(models.Model):
    """Gestion des lots de médicaments (FEFO - First Expired First Out)"""
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='lots')
    numero_lot = models.CharField(max_length=100, verbose_name="Numéro de lot")
    date_fabrication = models.DateField(verbose_name="Date de fabrication")
    date_expiration = models.DateField(verbose_name="Date d'expiration")
    date_reception = models.DateField(default=timezone.now, verbose_name="Date de réception")
    
    # Quantités
    quantite_initiale = models.IntegerField(verbose_name="Quantité initiale")
    quantite = models.IntegerField(verbose_name="Quantité actuelle")
    
    # Prix
    prix_achat_unitaire = models.DecimalField(max_digits=10, decimal_places=2,
                                             verbose_name="Prix d'achat unitaire")
    prix_vente_unitaire = models.DecimalField(max_digits=10, decimal_places=2,
                                             verbose_name="Prix de vente unitaire")
    
    # Fournisseur et commande
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True,
                                   related_name='lots', verbose_name="Fournisseur")
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='lots', verbose_name="Commande d'origine")
    
    # Statut
    actif = models.BooleanField(default=True, verbose_name="Lot actif")
    note = models.TextField(blank=True, verbose_name="Note")
    
    class Meta:
        verbose_name = "Lot de médicament"
        verbose_name_plural = "Lots de médicaments"
        ordering = ['date_expiration', 'date_reception']  # FEFO
        unique_together = ['medicament', 'numero_lot', 'fournisseur']
        indexes = [
            models.Index(fields=['date_expiration']),
            models.Index(fields=['numero_lot']),
        ]
    
    def __str__(self):
        return f"{self.medicament.nom} - Lot {self.numero_lot} (Exp: {self.date_expiration.strftime('%d/%m/%Y')})"
    
    def est_expire(self):
        """Vérifie si le lot est expiré"""
        return self.date_expiration < timezone.now().date()
    
    def jours_avant_expiration(self):
        """Calcule le nombre de jours avant expiration"""
        delta = self.date_expiration - timezone.now().date()
        return delta.days
    
    def valeur_stock(self):
        """Calcule la valeur du stock restant"""
        return self.quantite * self.prix_achat_unitaire
    
    def marge_realisable(self):
        """Calcule la marge potentielle sur ce lot"""
        return (self.prix_vente_unitaire - self.prix_achat_unitaire) * self.quantite


class MouvementStock(models.Model):
    """Traçabilité complète des mouvements de stock"""
    TYPE_MOUVEMENT_CHOICES = [
        ('ENTREE', 'Entrée (réception commande)'),
        ('SORTIE', 'Sortie (vente)'),
        ('RETOUR_CLIENT', 'Retour client'),
        ('RETOUR_FOURNISSEUR', 'Retour fournisseur'),
        ('PEREMPTION', 'Destruction médicament périmé'),
        ('CASSE', 'Casse/Perte'),
        ('INVENTAIRE_PLUS', 'Ajustement inventaire (+)'),
        ('INVENTAIRE_MOINS', 'Ajustement inventaire (-)'),
        ('TRANSFERT_SORTIE', 'Transfert vers autre pharmacie'),
        ('TRANSFERT_ENTREE', 'Réception depuis autre pharmacie'),
        ('ECHANTILLON', 'Échantillon gratuit'),
        ('USAGE_INTERNE', 'Usage interne'),
    ]
    
    # Références
    lot = models.ForeignKey(LotMedicament, on_delete=models.CASCADE, related_name='mouvements')
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='mouvements')
    
    # Type et quantité
    type_mouvement = models.CharField(max_length=30, choices=TYPE_MOUVEMENT_CHOICES)
    quantite = models.IntegerField(verbose_name="Quantité")
    quantite_avant = models.IntegerField(verbose_name="Stock avant mouvement")
    quantite_apres = models.IntegerField(verbose_name="Stock après mouvement")
    
    # Date et utilisateur
    date_mouvement = models.DateTimeField(auto_now_add=True, verbose_name="Date du mouvement")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mouvements_stock')
    
    # Coût et valeur
    cout_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Coût unitaire")
    valeur_totale = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valeur totale")
    
    # Références documents
    vente = models.ForeignKey(Vente, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='mouvements_stock')
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='mouvements_stock')
    reference_document = models.CharField(max_length=100, blank=True,
                                         verbose_name="Référence document",
                                         help_text="N° facture, bon de livraison, etc.")
    
    remarque = models.TextField(blank=True, verbose_name="Remarque")
    
    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date_mouvement']
        indexes = [
            models.Index(fields=['-date_mouvement']),
            models.Index(fields=['type_mouvement']),
        ]
    
    def __str__(self):
        return f"{self.get_type_mouvement_display()} - {self.medicament.nom} ({self.quantite})"
    
    def save(self, *args, **kwargs):
        # Calculer la valeur totale
        self.valeur_totale = self.quantite * self.cout_unitaire
        super().save(*args, **kwargs)


class Inventaire(models.Model):
    """Inventaire périodique du stock"""
    STATUT_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('VALIDE', 'Validé'),
        ('ANNULE', 'Annulé'),
    ]
    
    reference = models.CharField(max_length=50, unique=True, verbose_name="Référence")
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    
    responsable = models.ForeignKey(User, on_delete=models.PROTECT, related_name='inventaires_responsable',
                                   verbose_name="Responsable")
    valideur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='inventaires_valides', verbose_name="Validé par")
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_COURS')
    
    # Statistiques
    nombre_articles = models.IntegerField(default=0, verbose_name="Nombre d'articles")
    valeur_theorique = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                          verbose_name="Valeur théorique")
    valeur_reelle = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       verbose_name="Valeur réelle")
    ecart_valeur = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                      verbose_name="Écart de valeur")
    
    remarques = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"Inventaire {self.reference} - {self.get_statut_display()}"
    
    def calculer_statistiques(self):
        """Calcule les statistiques de l'inventaire"""
        lignes = self.lignes.all()
        self.nombre_articles = lignes.count()
        self.valeur_theorique = sum(l.valeur_theorique for l in lignes)
        self.valeur_reelle = sum(l.valeur_reelle for l in lignes)
        self.ecart_valeur = self.valeur_reelle - self.valeur_theorique
        self.save()


class LigneInventaire(models.Model):
    """Ligne d'inventaire pour chaque lot"""
    inventaire = models.ForeignKey(Inventaire, on_delete=models.CASCADE, related_name='lignes')
    lot = models.ForeignKey(LotMedicament, on_delete=models.CASCADE, related_name='inventaires')
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, related_name='inventaires')
    
    # Quantités
    quantite_theorique = models.IntegerField(verbose_name="Quantité théorique (système)")
    quantite_reelle = models.IntegerField(verbose_name="Quantité réelle (comptée)")
    ecart = models.IntegerField(verbose_name="Écart")
    
    # Valeurs
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    valeur_theorique = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valeur théorique")
    valeur_reelle = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valeur réelle")
    ecart_valeur = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Écart de valeur")
    
    # Métadonnées
    date_comptage = models.DateTimeField(auto_now_add=True, verbose_name="Date du comptage")
    compteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                related_name='lignes_inventaire', verbose_name="Compté par")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    ajustement_effectue = models.BooleanField(default=False, verbose_name="Ajustement effectué")
    
    class Meta:
        verbose_name = "Ligne d'inventaire"
        verbose_name_plural = "Lignes d'inventaire"
        unique_together = ['inventaire', 'lot']
    
    def __str__(self):
        return f"{self.medicament.nom} - Lot {self.lot.numero_lot}"
    
    def save(self, *args, **kwargs):
        # Calculer les écarts
        self.ecart = self.quantite_reelle - self.quantite_theorique
        self.valeur_theorique = self.quantite_theorique * self.prix_unitaire
        self.valeur_reelle = self.quantite_reelle * self.prix_unitaire
        self.ecart_valeur = self.valeur_reelle - self.valeur_theorique
        super().save(*args, **kwargs)


class Medecin(models.Model):
    """Modèle pour les médecins prescripteurs"""
    SPECIALITE_CHOICES = [
        ('GENERALISTE', 'Médecin généraliste'),
        ('PEDIATRE', 'Pédiatre'),
        ('CARDIOLOGUE', 'Cardiologue'),
        ('DERMATOLOGUE', 'Dermatologue'),
        ('GYNECOLOGUE', 'Gynécologue'),
        ('ORL', 'ORL'),
        ('OPHTALMOLOGUE', 'Ophtalmologue'),
        ('PSYCHIATRE', 'Psychiatre'),
        ('CHIRURGIEN', 'Chirurgien'),
        ('AUTRE', 'Autre spécialité'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    specialite = models.CharField(max_length=30, choices=SPECIALITE_CHOICES, default='GENERALISTE')
    numero_ordre = models.CharField(max_length=50, unique=True, verbose_name="N° Ordre des médecins")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    adresse_cabinet = models.TextField(blank=True, verbose_name="Adresse du cabinet")
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_ajout = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"
        ordering = ['nom', 'prenom']
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['numero_ordre']),
        ]
    
    def __str__(self):
        return f"Dr. {self.nom} {self.prenom} - {self.get_specialite_display()}"


class Prescription(models.Model):
    """Ordonnances médicales"""
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('PARTIELLE', 'Partiellement délivrée'),
        ('COMPLETE', 'Complètement délivrée'),
        ('EXPIREE', 'Expirée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    numero_ordonnance = models.CharField(max_length=50, unique=True, verbose_name="N° Ordonnance")
    medecin = models.ForeignKey(Medecin, on_delete=models.PROTECT, related_name='prescriptions')
    patient = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='prescriptions',
                               verbose_name="Patient")
    
    date_prescription = models.DateField(verbose_name="Date de prescription")
    date_validite = models.DateField(verbose_name="Date de validité",
                                    help_text="Les ordonnances ont une durée de validité limitée")
    date_reception = models.DateTimeField(auto_now_add=True, verbose_name="Date de réception")
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    
    # Fichier scanné
    fichier_scan = models.FileField(upload_to='ordonnances/', blank=True, null=True,
                                    verbose_name="Scan de l'ordonnance")
    
    # Métadonnées
    receptionniste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                      related_name='prescriptions_receptionnees',
                                      verbose_name="Réceptionné par")
    remarques = models.TextField(blank=True, verbose_name="Remarques")
    
    # Traçabilité réglementaire
    conserve_jusqu_au = models.DateField(null=True, blank=True,
                                        verbose_name="À conserver jusqu'au",
                                        help_text="Les ordonnances doivent être conservées légalement")
    
    class Meta:
        verbose_name = "Prescription/Ordonnance"
        verbose_name_plural = "Prescriptions/Ordonnances"
        ordering = ['-date_prescription']
        indexes = [
            models.Index(fields=['numero_ordonnance']),
            models.Index(fields=['-date_prescription']),
        ]
    
    def __str__(self):
        return f"Ordonnance {self.numero_ordonnance} - {self.patient}"
    
    def save(self, *args, **kwargs):
        # Conservation légale : 3 ans par défaut
        if not self.conserve_jusqu_au:
            from datetime import timedelta
            self.conserve_jusqu_au = self.date_prescription + timedelta(days=1095)
        super().save(*args, **kwargs)
    
    def est_valide(self):
        """Vérifie si l'ordonnance est encore valide"""
        return self.date_validite >= timezone.now().date()
    
    def peut_etre_delivree(self):
        """Vérifie si l'ordonnance peut être délivrée"""
        return self.est_valide() and self.statut in ['EN_ATTENTE', 'PARTIELLE']


class LignePrescription(models.Model):
    """Lignes de l'ordonnance (médicaments prescrits)"""
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='lignes')
    medicament = models.ForeignKey(Medicament, on_delete=models.PROTECT, related_name='prescriptions')
    
    posologie = models.TextField(verbose_name="Posologie",
                                 help_text="Ex: 1 comprimé 3 fois par jour pendant 7 jours")
    quantite_prescrite = models.IntegerField(verbose_name="Quantité prescrite")
    quantite_delivree = models.IntegerField(default=0, verbose_name="Quantité délivrée")
    
    substitution_autorisee = models.BooleanField(default=True,
                                                 verbose_name="Substitution autorisée (générique)")
    
    remarques = models.TextField(blank=True, verbose_name="Remarques")
    
    class Meta:
        verbose_name = "Ligne de prescription"
        verbose_name_plural = "Lignes de prescription"
    
    def __str__(self):
        return f"{self.medicament.nom} - {self.quantite_prescrite} unités"
    
    def est_completement_delivree(self):
        """Vérifie si la ligne est complètement délivrée"""
        return self.quantite_delivree >= self.quantite_prescrite
    
    def quantite_restante(self):
        """Calcule la quantité restant à délivrer"""
        return max(0, self.quantite_prescrite - self.quantite_delivree)


class Assurance(models.Model):
    """Compagnies d'assurance pour tiers-payant"""
    nom = models.CharField(max_length=200, verbose_name="Nom de l'assurance")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    
    # Contacts
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    contact_principal = models.CharField(max_length=200, blank=True,
                                        verbose_name="Nom du contact principal")
    
    # Conditions
    taux_remboursement_defaut = models.DecimalField(max_digits=5, decimal_places=2, default=80.00,
                                                    verbose_name="Taux de remboursement par défaut (%)")
    plafond_annuel = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        verbose_name="Plafond annuel par assuré")
    delai_paiement = models.IntegerField(default=30, verbose_name="Délai de paiement (jours)")
    
    # Convention
    date_debut_convention = models.DateField(null=True, blank=True,
                                            verbose_name="Date début convention")
    date_fin_convention = models.DateField(null=True, blank=True,
                                          verbose_name="Date fin convention")
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Assurance"
        verbose_name_plural = "Assurances"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.code})"
    
    def convention_valide(self):
        """Vérifie si la convention est valide"""
        if not self.date_fin_convention:
            return True
        return self.date_fin_convention >= timezone.now().date()


class VenteAssurance(models.Model):
    """Dossier de remboursement tiers-payant"""
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente de soumission'),
        ('SOUMIS', 'Soumis à l\'assurance'),
        ('ACCEPTE', 'Accepté'),
        ('ACCEPTE_PARTIEL', 'Accepté partiellement'),
        ('REFUSE', 'Refusé'),
        ('PAYE', 'Payé'),
        ('LITIGE', 'En litige'),
    ]
    
    vente = models.OneToOneField(Vente, on_delete=models.CASCADE, related_name='dossier_assurance')
    assurance = models.ForeignKey(Assurance, on_delete=models.PROTECT, related_name='dossiers')
    
    numero_dossier = models.CharField(max_length=50, unique=True, verbose_name="N° Dossier")
    numero_assure = models.CharField(max_length=50, verbose_name="N° Assuré")
    
    # Montants
    montant_total = models.DecimalField(max_digits=10, decimal_places=2,
                                       verbose_name="Montant total")
    montant_assurance = models.DecimalField(max_digits=10, decimal_places=2,
                                           verbose_name="Part assurance")
    montant_patient = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name="Part patient")
    montant_rembourse = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="Montant remboursé")
    
    # Dates
    date_soumission = models.DateField(null=True, blank=True, verbose_name="Date de soumission")
    date_reponse = models.DateField(null=True, blank=True, verbose_name="Date de réponse")
    date_paiement = models.DateField(null=True, blank=True, verbose_name="Date de paiement")
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    
    # Documents
    fichier_facture = models.FileField(upload_to='factures_assurance/', blank=True,
                                      verbose_name="Facture")
    fichier_reponse = models.FileField(upload_to='reponses_assurance/', blank=True,
                                      verbose_name="Réponse assurance")
    
    remarques = models.TextField(blank=True, verbose_name="Remarques")
    motif_refus = models.TextField(blank=True, verbose_name="Motif de refus")
    
    class Meta:
        verbose_name = "Dossier assurance"
        verbose_name_plural = "Dossiers assurance"
        ordering = ['-date_soumission']
        indexes = [
            models.Index(fields=['numero_dossier']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"Dossier {self.numero_dossier} - {self.assurance.nom}"
    
    def calculer_montants(self):
        """Calcule la répartition assurance/patient"""
        taux = self.assurance.taux_remboursement_defaut
        self.montant_assurance = (self.montant_total * taux) / 100
        self.montant_patient = self.montant_total - self.montant_assurance
        self.save()


class Caisse(models.Model):
    """Caisses de la pharmacie"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Numéro de caisse")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    localisation = models.CharField(max_length=100, blank=True, verbose_name="Localisation")
    
    actif = models.BooleanField(default=True, verbose_name="Active")
    date_installation = models.DateField(default=timezone.now, verbose_name="Date d'installation")
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Caisse"
        verbose_name_plural = "Caisses"
        ordering = ['numero']
    
    def __str__(self):
        return f"Caisse {self.numero} - {self.nom}"
    
    def session_active(self):
        """Retourne la session active de la caisse"""
        return self.sessions.filter(date_fermeture__isnull=True).first()


class SessionCaisse(models.Model):
    """Session de caisse (ouverture/fermeture)"""
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE, related_name='sessions')
    caissier = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sessions_caisse',
                                verbose_name="Caissier")
    
    # Dates
    date_ouverture = models.DateTimeField(verbose_name="Date/Heure d'ouverture")
    date_fermeture = models.DateTimeField(null=True, blank=True,
                                         verbose_name="Date/Heure de fermeture")
    
    # Fonds
    fond_caisse_ouverture = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                               verbose_name="Fond de caisse à l'ouverture")
    fond_caisse_fermeture = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                               verbose_name="Fond de caisse à la fermeture")
    
    # Totaux par méthode de paiement
    total_especes = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                       verbose_name="Total espèces")
    total_cb = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                  verbose_name="Total carte bancaire")
    total_mobile_money = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                            verbose_name="Total Mobile Money")
    total_cheque = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                      verbose_name="Total chèques")
    
    # Statistiques
    nombre_transactions = models.IntegerField(default=0, verbose_name="Nombre de transactions")
    montant_total_ventes = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                              verbose_name="Montant total des ventes")
    
    # Écarts
    ecart_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                      verbose_name="Écart de caisse (manquant/excédent)")
    
    # Validation
    validee_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='sessions_caisse_validees',
                                   verbose_name="Validée par")
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    
    remarques = models.TextField(blank=True, verbose_name="Remarques")
    
    class Meta:
        verbose_name = "Session de caisse"
        verbose_name_plural = "Sessions de caisse"
        ordering = ['-date_ouverture']
        indexes = [
            models.Index(fields=['-date_ouverture']),
            models.Index(fields=['caissier']),
        ]
    
    def __str__(self):
        statut = "Ouverte" if not self.date_fermeture else "Fermée"
        return f"Session {self.caisse.numero} - {self.date_ouverture.strftime('%d/%m/%Y %H:%M')} ({statut})"
    
    def calculer_totaux(self):
        """Calcule les totaux de la session"""
        ventes = self.ventes.filter(statut='VALIDEE')
        
        self.nombre_transactions = ventes.count()
        self.montant_total_ventes = ventes.aggregate(
            total=Coalesce(Sum('montant_total'), 0)
        )['total']
        
        self.total_especes = ventes.filter(methode_paiement='ESPECE').aggregate(
            total=Coalesce(Sum('montant_paye'), 0)
        )['total']
        
        self.total_cb = ventes.filter(methode_paiement='CARTE').aggregate(
            total=Coalesce(Sum('montant_paye'), 0)
        )['total']
        
        self.total_mobile_money = ventes.filter(methode_paiement='MOBILE').aggregate(
            total=Coalesce(Sum('montant_paye'), 0)
        )['total']
        
        self.total_cheque = ventes.filter(methode_paiement='CHEQUE').aggregate(
            total=Coalesce(Sum('montant_paye'), 0)
        )['total']
        
        self.save()
    
    def calculer_ecart(self):
        """Calcule l'écart de caisse"""
        attendu = (self.fond_caisse_ouverture + self.total_especes)
        self.ecart_caisse = self.fond_caisse_fermeture - attendu
        self.save()
        return self.ecart_caisse


class ActivityLog(models.Model):
    """Modèle pour enregistrer les activités des utilisateurs"""
    ACTION_CHOICES = [
        ('CREATE', 'Création'),
        ('UPDATE', 'Modification'),
        ('DELETE', 'Suppression'),
        ('VIEW', 'Consultation'),
        ('LOGIN', 'Connexion'),
        ('LOGOUT', 'Déconnexion'),
        ('VENTE', 'Vente effectuée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, blank=True, help_text="Nom du modèle concerné")
    object_id = models.IntegerField(null=True, blank=True, help_text="ID de l'objet concerné")
    description = models.TextField(help_text="Description de l'action")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"


class Investissement(models.Model):
    """Modèle pour les investissements de l'administrateur dans les stocks des utilisateurs"""
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('TERMINE', 'Terminé'),
        ('ANNULE', 'Annulé'),
    ]
    
    administrateur = models.ForeignKey(User, on_delete=models.PROTECT, related_name='investissements_effectues', 
                                       help_text="Administrateur qui effectue l'investissement")
    utilisateur = models.ForeignKey(User, on_delete=models.PROTECT, related_name='investissements_recus',
                                    help_text="Utilisateur qui reçoit l'investissement")
    montant = models.DecimalField(max_digits=12, decimal_places=2, help_text="Montant investi en FCFA")
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=10.0, 
                                       help_text="Taux d'intérêt annuel en pourcentage")
    duree_jours = models.IntegerField(help_text="Durée de l'investissement en jours")
    date_investissement = models.DateTimeField(default=timezone.now)
    date_echeance = models.DateField(help_text="Date d'échéance de l'investissement")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF')
    description = models.TextField(blank=True, help_text="Description ou motif de l'investissement")
    
    # Calculs automatiques
    interets_calcules = models.DecimalField(max_digits=12, decimal_places=2, default=0, 
                                           help_text="Intérêts calculés selon le taux et la durée")
    montant_total_attendu = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                                help_text="Montant total attendu (capital + intérêts)")
    
    class Meta:
        verbose_name = "Investissement"
        verbose_name_plural = "Investissements"
        ordering = ['-date_investissement']
    
    def __str__(self):
        return f"Investissement #{self.id} - {self.montant} FCFA pour {self.utilisateur.username}"
    
    def save(self, *args, **kwargs):
        """Calcule automatiquement les intérêts et la date d'échéance"""
        from datetime import timedelta
        
        # Calculer les intérêts: (montant * taux * durée) / 365 / 100
        self.interets_calcules = (float(self.montant) * float(self.taux_interet) * self.duree_jours) / 365 / 100
        self.montant_total_attendu = float(self.montant) + self.interets_calcules
        
        # Calculer la date d'échéance
        if not self.date_echeance:
            self.date_echeance = self.date_debut + timedelta(days=self.duree_jours)
        
        super().save(*args, **kwargs)


class CarteEmploye(models.Model):
    """Carte professionnelle d'employé avec QR code"""
    POSTES_CHOICES = [
        ('PHARMACIEN', 'Pharmacien(ne)'),
        ('ASSISTANT', 'Assistant(e) Pharmacien'),
        ('PREPARATEUR', 'Préparateur(trice)'),
        ('VENDEUR', 'Vendeur(euse)'),
        ('GESTIONNAIRE', 'Gestionnaire de Stock'),
        ('CAISSIER', 'Caissier(ère)'),
        ('RESPONSABLE', 'Responsable'),
        ('DIRECTEUR', 'Directeur(trice)'),
        ('STAGIAIRE', 'Stagiaire'),
        ('AUTRE', 'Autre'),
    ]
    
    utilisateur = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='carte_employe',
        verbose_name="Employé"
    )
    poste = models.CharField(
        max_length=50, 
        choices=POSTES_CHOICES,
        verbose_name="Poste/Fonction"
    )
    matricule = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="Matricule",
        help_text="Numéro unique d'identification de l'employé"
    )
    photo = models.ImageField(
        upload_to='photos_employes/',
        blank=True,
        null=True,
        verbose_name="Photo",
        help_text="Photo professionnelle de l'employé"
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    email_professionnel = models.EmailField(
        blank=True,
        verbose_name="Email professionnel"
    )
    adresse = models.TextField(
        blank=True,
        verbose_name="Adresse"
    )
    date_embauche = models.DateField(
        default=timezone.now,
        verbose_name="Date d'embauche"
    )
    date_creation_carte = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création de la carte"
    )
    date_expiration_carte = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date d'expiration de la carte"
    )
    qr_code = models.ImageField(
        upload_to='qr_codes_employes/',
        blank=True,
        null=True,
        verbose_name="QR Code"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Carte active"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes/Remarques"
    )
    
    class Meta:
        verbose_name = "Carte d'employé"
        verbose_name_plural = "Cartes d'employés"
        ordering = ['-date_creation_carte']
    
    def __str__(self):
        return f"Carte de {self.utilisateur.get_full_name() or self.utilisateur.username} - {self.matricule}"
    
    def generer_qr_code(self):
        """Génère le QR code avec les informations de l'employé"""
        # Créer les données à encoder
        nom_complet = self.utilisateur.get_full_name() or self.utilisateur.username
        
        # Formatter la date d'embauche
        date_embauche_str = 'N/A'
        if self.date_embauche:
            if isinstance(self.date_embauche, str):
                date_embauche_str = self.date_embauche
            else:
                date_embauche_str = self.date_embauche.strftime('%d/%m/%Y')
        
        # Formatter la date d'expiration
        date_expiration_str = 'Indéterminée'
        if self.date_expiration_carte:
            if isinstance(self.date_expiration_carte, str):
                date_expiration_str = self.date_expiration_carte
            else:
                date_expiration_str = self.date_expiration_carte.strftime('%d/%m/%Y')
        
        data = f"""
PHARMACARE - Carte d'Employé
━━━━━━━━━━━━━━━━━━━━━━
Nom: {nom_complet}
Matricule: {self.matricule}
Poste: {self.get_poste_display()}
Téléphone: {self.telephone or 'N/A'}
Email: {self.email_professionnel or self.utilisateur.email}
Date d'embauche: {date_embauche_str}
Carte valide jusqu'au: {date_expiration_str}
━━━━━━━━━━━━━━━━━━━━━━
Vérifié par PharmaCare
        """.strip()
        
        # Générer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Créer l'image
        img = qr.make_image(fill_color="#2E7D32", back_color="white")
        
        # Sauvegarder dans un buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Sauvegarder dans le modèle
        filename = f'qr_code_{self.matricule}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()
    
    def save(self, *args, **kwargs):
        """Génère automatiquement le QR code et le matricule"""
        from datetime import timedelta
        import random
        import string
        
        # Générer un matricule si vide
        if not self.matricule:
            annee = timezone.now().year
            random_str = ''.join(random.choices(string.digits, k=4))
            self.matricule = f"PC{annee}{random_str}"
        
        # Définir date d'expiration si vide (1 an par défaut)
        if not self.date_expiration_carte:
            self.date_expiration_carte = timezone.now().date() + timedelta(days=365)
        
        # Copier l'email du user si pas d'email pro
        if not self.email_professionnel and self.utilisateur.email:
            self.email_professionnel = self.utilisateur.email
        
        super().save(*args, **kwargs)
        
        # Générer le QR code après la sauvegarde
        if not self.qr_code:
            self.generer_qr_code()
            super().save(update_fields=['qr_code'])
    
    def est_expiree(self):
        """Vérifie si la carte est expirée"""
        if not self.date_expiration_carte:
            return False
        return self.date_expiration_carte < timezone.now().date()
    
    def jours_avant_expiration(self):
        """Calcule le nombre de jours avant expiration"""
        if not self.date_expiration_carte:
            return None
        delta = self.date_expiration_carte - timezone.now().date()
        return delta.days
