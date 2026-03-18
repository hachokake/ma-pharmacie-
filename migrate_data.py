"""
Script de migration et initialisation des données
À exécuter après les migrations Django : python manage.py shell < migrate_data.py
"""

from pharmacy.models import *
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

print("=" * 80)
print("SCRIPT DE MIGRATION DES DONNÉES PHARMACARE")
print("=" * 80)

# 1. Créer les lots initiaux pour les médicaments existants
print("\n1. Création des lots initiaux pour les médicaments...")
medicaments_sans_lots = Medicament.objects.filter(lots__isnull=True, quantite_stock__gt=0)
count_lots = 0

for med in medicaments_sans_lots:
    try:
        # Créer un lot initial avec les données du médicament
        lot = LotMedicament.objects.create(
            medicament=med,
            numero_lot=f"LOT-INIT-{med.id}-{datetime.now().strftime('%Y%m%d')}",
            date_fabrication=timezone.now().date() - timedelta(days=180),  # 6 mois avant
            date_expiration=med.date_expiration,
            date_reception=timezone.now().date(),
            quantite_initiale=med.quantite_stock,
            quantite=med.quantite_stock,
            prix_achat_unitaire=med.prix_achat_ht or Decimal('0'),
            prix_vente_unitaire=med.prix_unitaire,
            actif=True,
            note="Lot initial créé automatiquement lors de la migration"
        )
        
        # Créer un mouvement d'entrée
        MouvementStock.objects.create(
            lot=lot,
            medicament=med,
            type_mouvement='ENTREE',
            quantite=med.quantite_stock,
            quantite_avant=0,
            quantite_apres=med.quantite_stock,
            utilisateur=User.objects.filter(is_staff=True).first(),
            cout_unitaire=med.prix_achat_ht or Decimal('0'),
            reference_document='MIGRATION-INITIALE',
            remarque='Stock initial lors de la migration du système'
        )
        
        count_lots += 1
        print(f"   ✓ Lot créé pour {med.nom} (Qté: {med.quantite_stock})")
    except Exception as e:
        print(f"   ✗ Erreur pour {med.nom}: {e}")

print(f"\n   Total : {count_lots} lots créés")

# 2. Créer une caisse par défaut si aucune n'existe
print("\n2. Vérification de la caisse...")
if not Caisse.objects.exists():
    try:
        caisse = Caisse.objects.create(
            numero="CAISSE-01",
            nom="Caisse Principale",
            localisation="Comptoir principal",
            actif=True
        )
        print(f"   ✓ Caisse créée : {caisse.numero}")
    except Exception as e:
        print(f"   ✗ Erreur lors de la création de la caisse: {e}")
else:
    print(f"   ✓ {Caisse.objects.count()} caisse(s) existante(s)")

# 3. Compléter les informations manquantes des médicaments
print("\n3. Mise à jour des médicaments avec valeurs par défaut...")
medicaments = Medicament.objects.all()
count_updated = 0

for med in medicaments:
    updated = False
    
    # Si pas de DCI, utiliser le nom
    if not med.dci:
        med.dci = med.nom
        updated = True
    
    # Si pas de classification, mettre en vente libre par défaut
    if not med.classification:
        med.classification = 'LIBRE'
        updated = True
    
    # Si pas de forme galénique
    if not med.forme_galenique:
        med.forme_galenique = 'COMPRIME'
        updated = True
    
    # Si pas de prix d'achat
    if not med.prix_achat_ht or med.prix_achat_ht == 0:
        # Estimer à 60% du prix de vente
        med.prix_achat_ht = med.prix_unitaire * Decimal('0.6')
        updated = True
    
    if updated:
        med.save()
        count_updated += 1

print(f"   Total : {count_updated} médicaments mis à jour")

# 4. Statistiques finales
print("\n" + "=" * 80)
print("STATISTIQUES APRÈS MIGRATION")
print("=" * 80)

print(f"\nMédicaments:")
print(f"   - Total: {Medicament.objects.count()}")
print(f"   - Actifs: {Medicament.objects.filter(actif=True).count()}")
print(f"   - En rupture: {Medicament.objects.filter(quantite_stock__lte=0).count()}")
print(f"   - Avec prescription obligatoire: {Medicament.objects.filter(prescription_obligatoire=True).count()}")

print(f"\nLots:")
print(f"   - Total: {LotMedicament.objects.count()}")
print(f"   - Actifs: {LotMedicament.objects.filter(actif=True).count()}")
print(f"   - Expirés: {LotMedicament.objects.filter(date_expiration__lt=timezone.now().date()).count()}")

print(f"\nMouvements de stock:")
print(f"   - Total: {MouvementStock.objects.count()}")

print(f"\nClients:")
print(f"   - Total: {Client.objects.count()}")
print(f"   - Actifs: {Client.objects.filter(actif=True).count()}")
print(f"   - Avec assurance: {Client.objects.filter(assurance__isnull=False).count()}")

print(f"\nVentes:")
print(f"   - Total: {Vente.objects.count()}")
print(f"   - Validées: {Vente.objects.filter(statut='VALIDEE').count()}")

print(f"\nCaisses:")
print(f"   - Total: {Caisse.objects.count()}")
print(f"   - Actives: {Caisse.objects.filter(actif=True).count()}")

print(f"\nMédecins:")
print(f"   - Total: {Medecin.objects.count()}")

print(f"\nPrescriptions:")
print(f"   - Total: {Prescription.objects.count()}")

print(f"\nAssurances:")
print(f"   - Total: {Assurance.objects.count()}")
print(f"   - Actives: {Assurance.objects.filter(actif=True).count()}")

# 5. Calculer la valeur du stock
print(f"\nValeur du stock:")
lots_actifs = LotMedicament.objects.filter(actif=True, quantite__gt=0)
valeur_achat = sum(lot.quantite * lot.prix_achat_unitaire for lot in lots_actifs)
valeur_vente = sum(lot.quantite * lot.prix_vente_unitaire for lot in lots_actifs)
marge = valeur_vente - valeur_achat

print(f"   - Valeur d'achat: {valeur_achat:,.2f} FCFA")
print(f"   - Valeur de vente: {valeur_vente:,.2f} FCFA")
print(f"   - Marge potentielle: {marge:,.2f} FCFA")
if valeur_achat > 0:
    taux_marge = (marge / valeur_achat) * 100
    print(f"   - Taux de marge: {taux_marge:.2f}%")

print("\n" + "=" * 80)
print("MIGRATION TERMINÉE AVEC SUCCÈS !")
print("=" * 80)

print("\n📋 PROCHAINES ÉTAPES:")
print("   1. Vérifier les médicaments dans l'admin Django")
print("   2. Compléter les informations manquantes (DCI, dosages, etc.)")
print("   3. Ajouter les médecins et assurances si nécessaire")
print("   4. Créer des tokens API pour les utilisateurs")
print("   5. Tester les endpoints de l'API")
print("\n✅ Votre système est maintenant opérationnel !")
