# Système d'Administration Personnalisé - PharmaCare

## 📋 Présentation

Le système d'administration personnalisé vous permet de gérer complètement votre pharmacie avec des fonctionnalités avancées pour les administrateurs :

- **Gestion des utilisateurs** : Créer, modifier, activer/désactiver et supprimer des comptes
- **Suivi des activités** : Journal complet de toutes les actions effectuées par les utilisateurs
- **Statistiques détaillées** : Ventes par utilisateur, activités et performances
- **Contrôle d'accès** : Seuls les administrateurs ont accès à ces fonctionnalités

## 🚀 Accès à l'Administration

### Pour les Administrateurs

1. Connectez-vous avec un compte administrateur
2. Dans le menu de gauche, cliquez sur **"Administration"** (visible uniquement pour les administrateurs)
3. Vous accéderez au tableau de bord d'administration personnalisé

### Créer un Premier Administrateur

Si vous n'avez pas encore de compte administrateur, créez un superutilisateur :

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte avec :
- Nom d'utilisateur
- Email
- Mot de passe

## 📊 Fonctionnalités d'Administration

### 1. Tableau de Bord Admin
**URL** : `/admin-dashboard/`

Le tableau de bord affiche :
- Nombre total d'utilisateurs (actifs, inactifs, administrateurs)
- Statistiques de connexion du jour
- Top 10 des vendeurs avec leurs performances
- Activités récentes de tous les utilisateurs
- Statistiques globales (médicaments, ventes, clients)

### 2. Gestion des Utilisateurs
**URL** : `/admin-users/`

Fonctionnalités :
- **Liste complète** de tous les utilisateurs avec leurs statistiques
- **Filtres** : Par nom, statut (actif/inactif), type (admin/utilisateur)
- **Recherche** : Par nom d'utilisateur, nom complet ou email
- Visualisation du nombre de ventes et montant total par utilisateur
- Nombre d'activités enregistrées par utilisateur

### 3. Détails d'un Utilisateur
**URL** : `/admin-users/<user_id>/`

Pour chaque utilisateur, vous pouvez :
- Voir toutes les informations du compte
- Consulter les statistiques de ventes
- Voir l'historique complet des activités (50 dernières)
- Voir les 10 dernières ventes effectuées

**Actions disponibles** :
- ✅ **Activer/Désactiver** le compte
- 🛡️ **Promouvoir en administrateur** (réservé aux super-administrateurs)
- 🗑️ **Supprimer** le compte (réservé aux super-administrateurs)

> **Note** : Vous ne pouvez pas modifier votre propre compte pour des raisons de sécurité.

### 4. Journal d'Activités
**URL** : `/admin-activities/`

Consultez toutes les activités des utilisateurs :
- **Actions trackées** :
  - 🔑 Connexion/Déconnexion
  - ➕ Création d'éléments
  - ✏️ Modification
  - ❌ Suppression
  - 🛒 Ventes effectuées
  - 👁️ Consultations

**Filtres disponibles** :
- Par utilisateur
- Par type d'action
- Par plage de dates
- Affichage de l'adresse IP

### 5. Stock par Utilisateur
**URL** : `/admin-stock-by-user/`

Visualisez les performances de chaque utilisateur :
- Nombre de ventes effectuées
- Nombre de médicaments vendus
- Montant total des ventes
- Lien direct vers les détails de chaque utilisateur

## 🔐 Niveaux d'Accès

### Utilisateur Normal
- Accès au tableau de bord personnel
- Gestion des médicaments
- Création de ventes
- Consultation des stocks

### Administrateur (is_staff=True)
- Toutes les fonctionnalités utilisateur
- Accès au panneau d'administration personnalisé
- Gestion des utilisateurs (activation/désactivation)
- Consultation des activités
- Visualisation des statistiques globales

### Super-Administrateur (is_superuser=True)
- Toutes les fonctionnalités administrateur
- Promotion/rétrogradation d'administrateurs
- Suppression d'utilisateurs
- Accès à l'admin Django natif

## 📝 Journal des Activités

Le système enregistre automatiquement toutes les actions importantes :

### Actions Trackées
- **LOGIN** : Connexion d'un utilisateur (avec IP)
- **LOGOUT** : Déconnexion d'un utilisateur
- **CREATE** : Création d'un nouvel élément
- **UPDATE** : Modification d'un élément existant
- **DELETE** : Suppression d'un élément
- **VENTE** : Enregistrement d'une vente

### Informations Enregistrées
- Utilisateur ayant effectué l'action
- Type d'action
- Description détaillée
- Modèle concerné (Medicament, Vente, etc.)
- ID de l'objet concerné
- Adresse IP de l'utilisateur
- Date et heure précises

## 💡 Exemples d'Utilisation

### Surveiller un Utilisateur
1. Allez dans **Administration → Gestion des Utilisateurs**
2. Cliquez sur l'utilisateur à surveiller
3. Consultez son journal d'activités pour voir toutes ses actions

### Désactiver Temporairement un Compte
1. Allez dans **Administration → Gestion des Utilisateurs**
2. Cliquez sur l'utilisateur concerné
3. Cliquez sur **"Désactiver"**
4. L'utilisateur ne pourra plus se connecter jusqu'à réactivation

### Promouvoir un Utilisateur en Admin
1. Connectez-vous avec un compte super-administrateur
2. Allez dans les détails de l'utilisateur
3. Cliquez sur **"Promouvoir admin"**
4. L'utilisateur aura accès au panneau d'administration

### Consulter les Ventes d'un Utilisateur
1. Allez dans **Administration → Stock par Utilisateur**
2. Vous verrez le classement des vendeurs
3. Cliquez sur **"Détails"** pour voir les ventes détaillées

### Auditer les Activités Suspectes
1. Allez dans **Administration → Journal d'Activités**
2. Filtrez par utilisateur ou type d'action
3. Consultez les adresses IP et heures des actions
4. Détectez les comportements anormaux

## 🎨 Interface Utilisateur

L'interface d'administration utilise :
- **Bootstrap 5** pour un design moderne et responsive
- **Font Awesome** pour les icônes
- **Couleurs thématiques** pour différencier les actions
- **Cartes interactives** avec effets de survol
- **Tableaux triés** pour une navigation facile

## 🔒 Sécurité

### Mesures de Sécurité
- ✅ Vérification des permissions sur chaque page
- ✅ Protection contre l'auto-modification des comptes admin
- ✅ Enregistrement des adresses IP pour audit
- ✅ Confirmations pour les actions critiques (suppression)
- ✅ Séparation des niveaux d'accès (utilisateur/admin/super-admin)

### Recommandations
- Ne partagez jamais les identifiants administrateur
- Changez régulièrement les mots de passe
- Surveillez le journal d'activités régulièrement
- N'accordez les droits admin qu'aux personnes de confiance
- Désactivez les comptes inutilisés

## 📈 Évolutions Futures Possibles

- 📊 Rapports exportables (PDF, Excel)
- 📧 Notifications par email des actions critiques
- 🔔 Alertes en temps réel
- 📅 Planification de tâches automatiques
- 🌐 API REST pour intégration externe
- 📱 Application mobile d'administration
- 🔍 Recherche avancée dans les logs
- 📊 Graphiques de performance

## 🆘 Support

En cas de problème :
1. Vérifiez que vous êtes connecté avec un compte administrateur
2. Consultez les messages d'erreur affichés
3. Vérifiez les logs Django dans le terminal
4. Contactez le support technique si nécessaire

## 📝 Notes Techniques

### Modèle ActivityLog
- Enregistre automatiquement les actions importantes
- Accessible via `ActivityLog.objects.all()`
- Lié à l'utilisateur via ForeignKey
- Stocke l'IP, le timestamp, et la description

### Permissions
- `@login_required` : Nécessite une connexion
- `request.user.is_staff` : Nécessite le statut admin
- `request.user.is_superuser` : Nécessite le statut super-admin

### URLs d'Administration
```python
/admin-dashboard/              # Tableau de bord admin
/admin-users/                  # Liste des utilisateurs
/admin-users/<id>/             # Détails d'un utilisateur
/admin-activities/             # Journal d'activités
/admin-stock-by-user/          # Stock par utilisateur
```

---

**Version** : 1.0  
**Date** : Janvier 2026  
**Développé pour** : PharmaCare - Système de Gestion de Pharmacie
