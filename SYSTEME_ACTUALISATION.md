# 🔄 Système d'Actualisation en Temps Réel - PharmaCare

## 📋 Vue d'ensemble

Votre application **PharmaCare** dispose d'un système complet de mise à jour automatique qui **synchronise instantanément** toutes les modifications que vous faites dans VSCode avec toutes les plateformes.

---

## ✅ Comment ça fonctionne ?

### 🎯 Principe de Base

Toutes les applications (PWA, Electron, Android) **pointent vers votre serveur Django**. Elles affichent le site web via:
- **PWA**: Navigateur Chrome avec cache intelligent
- **Electron**: Fenêtre intégrée qui charge votre site Django
- **Android APK**: WebView qui affiche votre site Django

**Résultat**: Quand vous modifiez votre code Django dans VSCode, **toutes les applications voient instantanément les changements** !

---

## 📱 Par Plateforme

### 1. **PWA (Android/Chrome)**

#### ✨ Fonctionnalités
- ✅ **Service Worker intelligent** avec cache automatique
- ✅ **Détection automatique** des mises à jour toutes les heures
- ✅ **Notification visuelle** quand une mise à jour est disponible
- ✅ **Rechargement automatique** après confirmation
- ✅ **Versioning automatique** basé sur timestamp

#### 🔄 Processus de mise à jour
```
1. Vous modifiez du code Django dans VSCode
2. Vous sauvegardez (Ctrl+S)
3. Le Service Worker détecte le changement (vérification toutes les heures)
4. Une bannière apparaît: "Mise à jour disponible !"
5. L'utilisateur clique → Rechargement automatique
6. Nouvelle version active !
```

#### ⚡ Mise à jour manuelle
L'utilisateur peut forcer la mise à jour:
- **Méthode 1**: Recharger la page (tirer vers le bas sur mobile)
- **Méthode 2**: Cliquer sur la notification de mise à jour
- **Méthode 3**: Vider le cache Chrome

#### 📍 Fichiers concernés
- `pharmacy/static/service-worker.js` - Gestion du cache et mises à jour
- `pharmacy/templates/pharmacy/base.html` - Détection et notification

---

### 2. **Electron (Windows/Linux)**

#### ✨ Fonctionnalités
- ✅ **Rechargement automatique** toutes les 30 secondes
- ✅ **Menu "Recharger"** (Ctrl+R) pour forcer la mise à jour
- ✅ **Vérification des mises à jour** dans le menu Aide
- ✅ **Synchronisation continue** avec le serveur Django

#### 🔄 Processus de mise à jour
```
1. Vous modifiez du code Django dans VSCode
2. Vous sauvegardez (Ctrl+S)
3. L'application Electron recharge automatiquement après 30 secondes
4. Nouvelle version affichée !
```

#### ⚡ Mise à jour manuelle
L'utilisateur peut forcer la mise à jour:
- **Méthode 1**: Menu Fichier → Recharger (Ctrl+R)
- **Méthode 2**: Menu Aide → Vérifier les mises à jour
- **Méthode 3**: Redémarrer l'application

#### ⚙️ Configuration
Le rechargement automatique peut être désactivé dans `main.js` (ligne ~119):
```javascript
let autoReloadInterval = setInterval(() => {
    mainWindow.webContents.reload();
}, 30000); // Modifier ici (en millisecondes)
```

#### 📍 Fichiers concernés
- `AppBuild/electron-app/main.js` - Rechargement automatique

---

### 3. **Android APK (Capacitor)**

#### ✨ Fonctionnalités
- ✅ **Connexion directe** au serveur Django
- ✅ **Affichage temps réel** via WebView
- ✅ **Pas de cache** (affiche toujours la dernière version)
- ✅ **Synchronisation instantanée**

#### 🔄 Processus de mise à jour
```
1. Vous modifiez du code Django dans VSCode
2. Vous sauvegardez (Ctrl+S)
3. L'utilisateur recharge l'app (tirer vers le bas)
4. Nouvelle version affichée instantanément !
```

#### ⚡ Mise à jour manuelle
L'utilisateur peut forcer la mise à jour:
- **Méthode 1**: Tirer vers le bas pour rafraîchir
- **Méthode 2**: Redémarrer l'application
- **Méthode 3**: Vider les données de l'app dans les paramètres Android

#### 📍 Fichiers concernés
- `AppBuild/android-app/capacitor.config.json` - URL du serveur

---

## 🚀 Workflow de Développement

### Scénario typique

```
┌─────────────────────────────────────────────────────────────┐
│  1. DÉVELOPPEMENT (VSCode)                                  │
├─────────────────────────────────────────────────────────────┤
│  → Vous modifiez pharmacy/views.py                          │
│  → Vous ajoutez un template pharmacy/templates/...          │
│  → Vous modifiez le CSS dans base.html                      │
│  → Vous sauvegardez (Ctrl+S)                                │
│  → Django recharge automatiquement (runserver)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. SYNCHRONISATION AUTOMATIQUE                             │
├─────────────────────────────────────────────────────────────┤
│  PWA:      Détection dans 0-60 minutes (vérif auto)        │
│  Electron: Détection dans 0-30 secondes (reload auto)      │
│  Android:  Instantané (au prochain rechargement)           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. UTILISATEURS VOIENT LES CHANGEMENTS                     │
├─────────────────────────────────────────────────────────────┤
│  ✅ Nouvelles fonctionnalités disponibles                   │
│  ✅ Bugs corrigés                                           │
│  ✅ Design mis à jour                                       │
│  ✅ Aucune réinstallation nécessaire !                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration Avancée

### 🔧 Modifier la fréquence de mise à jour PWA

Dans `pharmacy/templates/pharmacy/base.html` (ligne ~656):

```javascript
setInterval(() => {
    registration.update();
}, 60 * 60 * 1000); // Par défaut: 1 heure (3600000 ms)
```

**Exemples**:
- Toutes les 5 minutes: `5 * 60 * 1000`
- Toutes les 30 minutes: `30 * 60 * 1000`
- Toutes les 2 heures: `2 * 60 * 60 * 1000`

### 🔧 Modifier la fréquence de rechargement Electron

Dans `AppBuild/electron-app/main.js` (ligne ~123):

```javascript
let autoReloadInterval = setInterval(() => {
    mainWindow.webContents.reload();
}, 30000); // Par défaut: 30 secondes (30000 ms)
```

**Exemples**:
- Toutes les 10 secondes: `10000`
- Toutes les minutes: `60000`
- Désactiver: Commenter tout le bloc setInterval

### 🔧 Modifier le versioning PWA

Dans `pharmacy/static/service-worker.js` (ligne ~3):

```javascript
const VERSION = '2026-01-19-v2'; // Changez cette valeur pour forcer une mise à jour
```

**Important**: Changez cette version à chaque déploiement majeur pour **forcer** le rechargement du cache.

---

## 🎯 Tests de Mise à Jour

### Test 1: PWA
```bash
1. Modifiez pharmacy/templates/pharmacy/dashboard.html
2. Ajoutez un texte visible: <h1>TEST MAJ</h1>
3. Sauvegardez
4. Sur Android, attendez 5 minutes OU rechargez la page
5. Vérifiez que "TEST MAJ" apparaît
```

### Test 2: Electron
```bash
1. Modifiez pharmacy/templates/pharmacy/dashboard.html
2. Ajoutez un texte visible: <h1>TEST ELECTRON</h1>
3. Sauvegardez
4. Attendez 30 secondes (ou Ctrl+R)
5. Vérifiez que "TEST ELECTRON" apparaît
```

### Test 3: Android APK
```bash
1. Modifiez pharmacy/templates/pharmacy/dashboard.html
2. Ajoutez un texte visible: <h1>TEST APK</h1>
3. Sauvegardez
4. Sur Android, tirez vers le bas pour rafraîchir
5. Vérifiez que "TEST APK" apparaît
```

---

## 📊 Tableau Comparatif

| Plateforme | Délai de mise à jour | Automatique | Manuel | Cache |
|------------|----------------------|-------------|--------|-------|
| **PWA** | 0-60 min | ✅ Oui | ✅ Oui (recharge) | ✅ Intelligent |
| **Electron** | 0-30 sec | ✅ Oui | ✅ Oui (Ctrl+R) | ❌ Non |
| **Android APK** | Instantané | ⚠️ Semi | ✅ Oui (swipe) | ❌ Non |

---

## 💡 Bonnes Pratiques

### ✅ À FAIRE
1. **Testez localement** avant de déployer
2. **Modifiez le VERSION** dans service-worker.js pour les maj importantes
3. **Informez les utilisateurs** des nouvelles fonctionnalités via une popup
4. **Gardez le serveur Django en ligne** (les apps en dépendent)
5. **Utilisez HTTPS** en production pour la PWA

### ❌ À ÉVITER
1. Ne modifiez pas directement les fichiers dans AppBuild/ sans les copier
2. Ne désactivez pas le Service Worker (perte du mode offline)
3. N'utilisez pas de cache côté serveur qui empêcherait les mises à jour
4. Ne changez pas l'URL du serveur sans prévenir les utilisateurs

---

## 🔥 Cas d'Usage Réels

### Exemple 1: Correction de Bug
```
09:00 - Bug signalé dans le formulaire de vente
09:05 - Vous corrigez dans pharmacy/forms.py
09:06 - Vous sauvegardez
09:06 - Django recharge
09:36 - Electron met à jour (30 sec après)
10:06 - PWA détecte la mise à jour (1h après)
10:07 - Utilisateur clique "Mettre à jour"
10:07 - Bug corrigé pour tous !
```

### Exemple 2: Nouvelle Fonctionnalité
```
14:00 - Vous ajoutez une page de statistiques
14:10 - Vous créez pharmacy/templates/pharmacy/stats.html
14:15 - Vous ajoutez la route dans pharmacy/urls.py
14:15 - Vous sauvegardez
14:16 - Toutes les apps peuvent accéder à /stats/ !
```

### Exemple 3: Changement de Design
```
16:00 - Vous modifiez le CSS dans base.html
16:01 - Vous changez la couleur du header
16:01 - Vous sauvegardez
16:31 - Electron affiche le nouveau design (30 sec)
17:01 - PWA propose la mise à jour (1h)
17:02 - Tout le monde voit le nouveau design !
```

---

## 🆘 Dépannage

### Problème: La PWA ne se met pas à jour
**Solutions**:
1. Changez `VERSION` dans service-worker.js
2. Videz le cache Chrome (Paramètres → Confidentialité)
3. Désinstallez et réinstallez la PWA
4. Vérifiez que le serveur Django est accessible

### Problème: Electron ne recharge pas
**Solutions**:
1. Vérifiez que le serveur Django est démarré
2. Appuyez sur Ctrl+R pour forcer le rechargement
3. Redémarrez l'application Electron
4. Vérifiez l'URL du serveur dans le menu Fichier

### Problème: Android APK ne se synchronise pas
**Solutions**:
1. Vérifiez la connexion Internet
2. Vérifiez l'URL dans capacitor.config.json
3. Tirez vers le bas pour rafraîchir
4. Redémarrez l'application
5. Videz les données de l'app dans les paramètres Android

---

## 📚 Résumé

🎉 **Votre système est COMPLET** ! 

Toutes les modifications que vous faites dans VSCode sont **automatiquement synchronisées** avec:
- ✅ PWA sur Android (mise à jour toutes les heures)
- ✅ Application Electron sur PC (mise à jour toutes les 30 secondes)
- ✅ APK Android (mise à jour instantanée au rechargement)

**Aucune compilation ou redistribution nécessaire** pour la plupart des changements ! 🚀

---

**Date de création**: 19 janvier 2026  
**Version du système**: 2.0  
**Application**: PharmaCare - Gestion de Pharmacie
