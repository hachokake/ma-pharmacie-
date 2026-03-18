# 🏥 PharmaCare - Système de Gestion de Pharmacie Professionnel

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![API](https://img.shields.io/badge/API-REST-orange.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

Application web professionnelle de gestion de pharmacie développée avec Django, incluant une API REST complète pour applications mobiles.

## ✨ Fonctionnalités Principales

### 📊 Tableau de bord professionnel
- Vue d'ensemble des statistiques clés en temps réel
- Valeur totale du stock (achat/vente/marge)
- Alertes intelligentes (ruptures, stock faible, péremptions)
- Statistiques de ventes (jour/mois/période personnalisée)
- Top médicaments les plus vendus
- Analyse de rotation du stock

### 💊 Gestion pharmaceutique complète
- **Médicaments** avec DCI, classification réglementaire, forme galénique, dosage
- **Gestion multi-lots** avec FEFO automatique (First Expired First Out)
- **Traçabilité totale** : 12 types de mouvements de stock
- **Prescriptions/Ordonnances** avec médecins prescripteurs
- Classification : Vente libre, Ordonnance, Stupéfiants (Listes I-IV)
- Alertes péremption automatiques
- Code-barres, CIP, N° AMM

### 🛒 Ventes avancées
- **3 types de ventes** : Comptant, Crédit, Tiers-payant (assurance)
- Numéro de facture automatique
- Prélèvement stock FEFO automatique
- Gestion des créances clients
- Remises et réductions
- Sessions de caisse avec contrôle d'écart
- Annulation de vente avec remise en stock

### 👥 Gestion clients et assurances
- Dossier client complet (assurance, crédit autorisé)
- **Tiers-payant** : Dossiers de remboursement assurance
- Plafonds de crédit personnalisés
- Historique des achats et impayés
- Taux de couverture assurance

### 📦 Stock et inventaire
- **Inventaires automatisés** avec ajustement auto du stock
- Valorisation du stock en temps réel
- Gestion des péremptions
- Rapports de rotation (top ventes, stagnants)
- Mouvements : Entrées, Sorties, Retours, Péremptions, Transferts

### 🔌 API REST complète
- **50+ endpoints** pour application mobile
- Authentification par token
- CRUD complet sur tous les modèles
- Statistiques et rapports
- Filtrage, recherche, pagination
- CORS configuré

### 💼 Gestion administrative
- Médecins (10 spécialités)
- Fournisseurs et commandes
- Cartes d'employés avec QR code
- Logs d'activité complets
- Interface admin Django optimisée

## 🚀 Installation Rapide (5 minutes)

### 1. Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installer les dépendances

```bash
pip install python-dotenv djangorestframework django-cors-headers
pip install -r requirements.txt
```

### 3. Effectuer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Migrer les données existantes

```bash
python manage.py shell < migrate_data.py
```

### 5. Créer un superutilisateur (si premier lancement)

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

L'application sera accessible à : http://127.0.0.1:8000/

## 📚 Documentation

- **[Guide de démarrage rapide](GUIDE_DEMARRAGE_RAPIDE.md)** - Démarrage en 5 minutes
- **[Résumé exécutif](RESUME_EXECUTIF.md)** - Vue d'ensemble pour décideurs
- **[Améliorations implémentées](AMELIORATIONS_IMPLEMENTEES.md)** - Documentation technique complète
- **[Guide administrateur](SETUP_ADMIN.md)** - Configuration complète

## 🔧 Configuration

Le fichier `.env` contient les variables d'environnement :

```env
SECRET_KEY=votre-clé-secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Pour la production, voir `.env.example` et `requirements_production.txt`

## 🔌 API REST

### Authentification

```bash
# Obtenir un token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "votre_password"}'

# Utiliser le token
curl http://127.0.0.1:8000/api/medicaments/ \
  -H "Authorization: Token votre_token_ici"
```

### Endpoints principaux

- **Médicaments** : `/api/medicaments/`
  - Actions : `en_rupture/`, `alerte_stock/`, `expires/`, `lots/`, `historique_mouvements/`
  
- **Ventes** : `/api/ventes/`
  - Actions : `statistiques/`, `annuler/`, `par_client/`
  
- **Prescriptions** : `/api/prescriptions/`
  - Conservation automatique 3 ans (Stupéfiants 10 ans)
  
- **Inventaires** : `/api/inventaires/`
  - Actions : `creer_inventaire/`, `valider/`
  
- **Caisse** : `/api/caisses/`
  - Actions : `ouvrir_session/`, `fermer_session/`, `session_active/`
  
- **Statistiques** : `/api/statistiques/`
  - Actions : `dashboard/`, `ventes/`, `rotation_stock/`

Voir [GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md) pour exemples complets.

## 📱 Applications mobiles

### Android (Capacitor)
```bash
cd AppBuild/android-app
npm install
npm run build
npx cap sync
npx cap open android
```

### Electron (Desktop)
```bash
cd AppBuild/electron-app
npm install
npm start
```

## 🏗️ Architecture

```
pharmacy_project/
├── pharmacy/               # Application principale
│   ├── models.py          # 15+ modèles de données
│   ├── services.py        # Logique métier (680 lignes)
│   ├── serializers.py     # Sérializers API (460 lignes)
│   ├── api_views.py       # Vues API (550 lignes)
│   ├── views.py           # Vues web
│   ├── admin.py           # Interface admin
│   └── urls.py            # Routes
├── pharmacy_project/      # Configuration Django
│   ├── settings.py        # Config sécurisée
│   └── urls.py            # Routes principales
├── migrate_data.py        # Script de migration
└── .env                   # Variables d'environnement
```

## 🔐 Sécurité

- ✅ SECRET_KEY en variable d'environnement
- ✅ Authentification par token API
- ✅ CORS configuré
- ✅ HTTPS ready (SECURE_SSL_REDIRECT)
- ✅ Protection CSRF
- ✅ Cookies sécurisés
- ✅ Logs d'activité complets

## 📊 Modèles de données

### Principaux modèles
1. **Medicament** - Informations pharmaceutiques complètes (DCI, classification, forme galénique)
2. **LotMedicament** - Gestion multi-lots avec FEFO automatique
3. **MouvementStock** - Traçabilité complète (12 types de mouvements)
4. **Vente** / **ItemVente** - Ventes avec suivi des lots et FEFO
5. **Prescription** / **LignePrescription** - Ordonnances avec conservation réglementaire
6. **Medecin** - Prescripteurs avec 10 spécialités
7. **Client** - Dossiers clients avec assurance et crédit
8. **Assurance** / **VenteAssurance** - Tiers-payant et remboursements
9. **Caisse** / **SessionCaisse** - Gestion caisse avec écarts
10. **Inventaire** / **LigneInventaire** - Inventaires automatisés
11. **Fournisseur** / **Commande** - Gestion approvisionnements
12. **Categorie** - Classification produits
13. **CarteEmploye** - Badges avec QR code
14. **Investissement** - Suivi financier
15. **ActivityLog** - Traçabilité des actions utilisateurs

Voir [AMELIORATIONS_IMPLEMENTEES.md](AMELIORATIONS_IMPLEMENTEES.md) pour détails complets.

## 🎯 Utilisation

### 1. Interface Web
- Connectez-vous avec vos identifiants
- Accédez au tableau de bord pour vue d'ensemble
- Gérez médicaments, ventes, clients depuis le menu principal

### 2. Interface Admin Django
- Accès : http://127.0.0.1:8000/admin/
- Gestion complète de tous les modèles
- Filtres intelligents et recherche avancée
- Exports et génération de rapports

### 3. API REST Mobile
- Authentifiez-vous pour obtenir un token
- Utilisez le token dans l'en-tête Authorization
- Consultez `/api/` pour liste complète des endpoints

## 🆕 Nouveautés Version 2.0

### ✨ Modèles étendus (15+ nouveaux)
- **LotMedicament** avec FEFO automatique
- **Prescription** avec conservation réglementaire (3/10 ans)
- **Assurance** et tiers-payant complet
- **SessionCaisse** avec contrôle d'écarts
- **Inventaires** automatisés avec ajustements
- **MouvementStock** (12 types de mouvements traçables)

### 🏗️ Architecture professionnelle
- Couche service métier ([services.py](pharmacy/services.py) - 680 lignes)
- API REST complète (50+ endpoints)
- Sérializers optimisés (list vs detail)
- Transactions atomiques (@transaction.atomic)
- Gestion d'erreurs robuste

### 🔐 Sécurité renforcée
- Variables d'environnement (.env)
- Authentification token pour API
- Logging complet des actions
- Configuration production/développement séparée
- Headers de sécurité (HTTPS, CSRF, Cookies sécurisés)

### 📈 Fonctionnalités avancées
- **Ventes multiples** : Comptant, Crédit, Tiers-payant
- **Prélèvement FEFO** automatique lors des ventes
- **Rapports statistiques** : Dashboard, rotation stock, analyses
- **Rotation du stock** : Top ventes, produits stagnants
- **Valorisation temps réel** : PA, PV, marges calculées

## 🚨 Points d'attention

### Migration de données existantes
⚠️ **IMPORTANT** : Si vous avez déjà des données dans le système :

1. **Sauvegardez** votre base de données actuelle :
   ```bash
   copy db.sqlite3 db.sqlite3.backup
   ```

2. **Effectuez les migrations** :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Exécutez le script de migration** :
   ```bash
   python manage.py shell < migrate_data.py
   ```

4. **Vérifiez dans l'admin** :
   - Lots créés pour chaque médicament
   - Valeurs de stock cohérentes
   - Aucune erreur dans les logs

### Informations à compléter
Après la migration, complétez dans l'interface admin Django :

- **Médicaments** :
  - DCI (Dénomination Commune Internationale)
  - Classification réglementaire (Vente libre/Ordonnance/Stupéfiant)
  - Forme galénique et dosage
  - Marges (marge_pourcentage ou marge_montant)

- **Médecins** : Créez les médecins prescripteurs si vous gérez des prescriptions

- **Assurances** : Créez les organismes d'assurance si vous gérez le tiers-payant

- **Caisse** : Une caisse par défaut est créée automatiquement

## 🛠️ Technologies utilisées

- **Backend** : Django 5.2.6, Python 3.8+
- **API** : Django REST Framework 3.14+
- **Base de données** : SQLite (développement), PostgreSQL ready
- **Frontend Web** : HTML5, CSS3, JavaScript
- **Mobile** : Capacitor (Android), Electron (Desktop)
- **Sécurité** : python-dotenv, django-cors-headers, Token Authentication
- **Images** : Pillow, qrcode
- **Architecture** : Service Layer Pattern, REST API

## 📞 Support et dépannage

### En cas de problème :

1. **Consultez la documentation** :
   - [GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md) pour démarrage rapide
   - [AMELIORATIONS_IMPLEMENTEES.md](AMELIORATIONS_IMPLEMENTEES.md) pour détails techniques
   - [RESUME_EXECUTIF.md](RESUME_EXECUTIF.md) pour vue d'ensemble

2. **Vérifiez les logs** :
   - Fichier : `logs/django.log`
   - Console du serveur de développement
   - Interface admin Django : "Activity logs"

3. **Interface admin** :
   - http://127.0.0.1:8000/admin/
   - Permet corrections manuelles et visualisation des données

4. **Commandes utiles** :
   ```bash
   # Vérifier les migrations en attente
   python manage.py showmigrations
   
   # Créer un rapport de l'état du système
   python manage.py check
   
   # Vider le cache
   python manage.py clear_cache
   
   # Shell Django pour tests
   python manage.py shell
   ```

## 📜 Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Crédits et remerciements

Développé avec ❤️ pour offrir une solution de gestion pharmaceutique professionnelle, conforme aux réglementations et adaptée aux besoins réels des pharmacies.

### Conformité réglementaire
✅ Conservation des ordonnances (3 ans / 10 ans stupéfiants)  
✅ Traçabilité complète des mouvements de stock  
✅ Classification des médicaments selon listes réglementaires  
✅ Gestion FEFO (First Expired First Out)  
✅ Suivi des lots et numéros de série  
✅ Logs d'activité pour audits  

---

**Version** : 2.0.0  
**Dernière mise à jour** : Janvier 2025  
**Statut** : ✅ Production Ready  
**Support Python** : 3.8 - 3.12  
**Framework** : Django 5.2  

---

### 🚀 Prochaines étapes recommandées

1. **Installation immédiate** :
   - Suivez le guide d'installation ci-dessus (5 minutes)
   - Exécutez le script de migration de données
   - Créez votre premier superutilisateur

2. **Configuration** :
   - Complétez les informations des médicaments (DCI, classification)
   - Ajoutez médecins et assurances si nécessaire
   - Ouvrez votre première session de caisse

3. **Formation** :
   - Consultez [GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md)
   - Testez l'API avec les exemples fournis
   - Explorez l'interface admin Django

4. **Production** (optionnel) :
   - Migrez vers PostgreSQL pour performance accrue
   - Configurez HTTPS et nom de domaine
   - Utilisez `requirements_production.txt`
   - Configurez les sauvegardes automatiques

Pour toute assistance, consultez d'abord la documentation complète fournie dans ce projet.
