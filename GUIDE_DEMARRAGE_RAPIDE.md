# 🚀 GUIDE DE DÉMARRAGE RAPIDE - PHARMACARE

## ⚡ Installation en 5 minutes

### 1️⃣ Installer les dépendances (2 min)

```bash
pip install python-dotenv djangorestframework django-cors-headers
```

### 2️⃣ Créer les migrations (1 min)

```bash
python manage.py makemigrations
python manage.py migrate
```

**ATTENDU** : Vous verrez de nombreuses migrations créées pour tous les nouveaux modèles :
- LotMedicament
- MouvementStock  
- Prescription, LignePrescription, Medecin
- Assurance, VenteAssurance
- Caisse, SessionCaisse
- Inventaire, LigneInventaire
- Et les modifications sur Medicament, Client, Vente, ItemVente

### 3️⃣ Migrer les données existantes (1 min)

```bash
python manage.py shell < migrate_data.py
```

Ce script va automatiquement :
- ✅ Créer des lots initiaux pour vos médicaments
- ✅ Créer une caisse par défaut
- ✅ Compléter les informations manquantes
- ✅ Afficher les statistiques

### 4️⃣ Démarrer le serveur (10 sec)

```bash
python manage.py runserver
```

### 5️⃣ Accéder aux interfaces (10 sec)

- 🌐 **Application Web** : http://localhost:8000/
- 🔧 **Admin Django** : http://localhost:8000/admin/
- 🔌 **API REST** : http://localhost:8000/api/

---

## 🎯 Test rapide de l'API

### 1. Obtenir un token d'authentification

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -d "username=votre_admin&password=votre_password"
```

**Réponse** : `{"token": "a1b2c3d4e5f6..."}`

### 2. Lister les médicaments

```bash
curl http://localhost:8000/api/medicaments/ \
  -H "Authorization: Token a1b2c3d4e5f6..."
```

### 3. Voir les statistiques du dashboard

```bash
curl http://localhost:8000/api/statistiques/dashboard/ \
  -H "Authorization: Token a1b2c3d4e5f6..."
```

---

## 📱 Utilisation pour application mobile

### Configuration CORS

Le CORS est déjà configuré pour :
- `http://localhost:3000` (React Native)
- `http://localhost:8100` (Ionic)

Pour ajouter d'autres domaines, modifier dans [settings.py](pharmacy_project/settings.py#L145) :

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8100",
    "http://votre-app-mobile.com",  # Ajouter ici
]
```

### Authentification mobile

1. **Login** : Envoyer username/password à `/api/auth/token/`
2. **Stocker** : Sauvegarder le token dans le stockage local
3. **Utiliser** : Ajouter header `Authorization: Token xxx` à chaque requête

---

## 🔑 Créer des tokens pour les utilisateurs existants

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Pour un utilisateur spécifique
user = User.objects.get(username='nom_utilisateur')
token, created = Token.objects.get_or_create(user=user)
print(f"Token pour {user.username}: {token.key}")

# Pour tous les utilisateurs
for user in User.objects.all():
    token, created = Token.objects.get_or_create(user=user)
    print(f"{user.username}: {token.key}")
```

---

## 📊 Tester les nouvelles fonctionnalités

### 1. Gestion des lots (FEFO)

1. Aller dans l'admin : http://localhost:8000/admin/pharmacy/lotmedicament/
2. Voir les lots créés automatiquement
3. Ajouter un nouveau lot avec une date d'expiration différente
4. Lors d'une vente, le système prendra automatiquement le lot qui expire en premier

### 2. Créer une prescription

1. Aller dans : http://localhost:8000/admin/pharmacy/medecin/
2. Créer un médecin
3. Aller dans : http://localhost:8000/admin/pharmacy/prescription/
4. Créer une ordonnance avec des lignes de médicaments

### 3. Ouvrir une session de caisse

Via l'API :

```bash
curl -X POST http://localhost:8000/api/caisses/1/ouvrir_session/ \
  -H "Authorization: Token xxx" \
  -H "Content-Type: application/json" \
  -d '{"fond_ouverture": 50000}'
```

### 4. Créer une vente via l'API

```bash
curl -X POST http://localhost:8000/api/ventes/ \
  -H "Authorization: Token xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "methode_paiement": "ESPECE",
    "type_vente": "COMPTANT",
    "items": [
      {"medicament_id": 1, "quantite": 2}
    ]
  }'
```

Le système va automatiquement :
- ✅ Vérifier le stock
- ✅ Prélever du lot qui expire en premier (FEFO)
- ✅ Créer les mouvements de stock
- ✅ Générer le numéro de facture
- ✅ Calculer le total

### 5. Créer un inventaire

```bash
curl -X POST http://localhost:8000/api/inventaires/creer_inventaire/ \
  -H "Authorization: Token xxx"
```

Le système crée automatiquement une ligne pour chaque lot actif.

---

## 🐛 Dépannage

### Erreur : "No module named 'dotenv'"

```bash
pip install python-dotenv
```

### Erreur : "No module named 'rest_framework'"

```bash
pip install djangorestframework django-cors-headers
```

### Erreur de migration

```bash
# Supprimer les migrations existantes (ATTENTION : backup avant !)
python manage.py migrate pharmacy zero

# Supprimer les fichiers de migration
# Puis recréer
python manage.py makemigrations
python manage.py migrate
```

### Les lots ne se créent pas automatiquement

```bash
python manage.py shell < migrate_data.py
```

### API retourne 401 Unauthorized

Vérifier que le token est bien envoyé :
```
Authorization: Token votre_token
```

Pas `Bearer`, mais `Token` !

---

## 📚 Documentation complète

Pour plus de détails, voir :
- [AMELIORATIONS_IMPLEMENTEES.md](AMELIORATIONS_IMPLEMENTEES.md) - Documentation complète
- [services.py](pharmacy/services.py) - Logique métier
- [api_views.py](pharmacy/api_views.py) - Endpoints API
- [models.py](pharmacy/models.py) - Structure de données

---

## 🎓 Exemples de requêtes API

### Médicaments en rupture de stock

```bash
curl http://localhost:8000/api/medicaments/en_rupture/ \
  -H "Authorization: Token xxx"
```

### Lots proches de l'expiration (30 jours)

```bash
curl "http://localhost:8000/api/lots/proche_expiration/?jours=30" \
  -H "Authorization: Token xxx"
```

### Statistiques de ventes du mois

```bash
curl "http://localhost:8000/api/ventes/statistiques/?date_debut=2024-01-01&date_fin=2024-01-31" \
  -H "Authorization: Token xxx"
```

### Historique des ventes d'un client

```bash
curl http://localhost:8000/api/clients/1/historique_ventes/ \
  -H "Authorization: Token xxx"
```

### Prescriptions en attente

```bash
curl http://localhost:8000/api/prescriptions/en_attente/ \
  -H "Authorization: Token xxx"
```

---

## ✅ Checklist post-installation

- [ ] Migrations créées et appliquées
- [ ] Script de migration des données exécuté
- [ ] Au moins une caisse créée
- [ ] Tokens créés pour les utilisateurs
- [ ] Test API réussi (obtenir token + lister médicaments)
- [ ] Vérifier les lots dans l'admin
- [ ] Compléter les informations des médicaments (DCI, classification, etc.)
- [ ] Créer un médecin (si prescriptions)
- [ ] Créer une assurance (si tiers-payant)
- [ ] Tester une vente via l'API

---

## 🎉 Félicitations !

Votre système PharmaCare professionnel est opérationnel !

**Principales nouveautés disponibles** :
- ✅ Gestion multi-lots avec FEFO automatique
- ✅ Traçabilité complète (mouvements de stock)
- ✅ Prescriptions et ordonnances
- ✅ Tiers-payant et assurances
- ✅ Inventaires automatisés
- ✅ API REST complète
- ✅ Sessions de caisse
- ✅ Rapports avancés

**Prêt pour la production !** 🚀
