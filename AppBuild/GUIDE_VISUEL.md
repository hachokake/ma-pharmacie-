# 🎯 Guide de Démarrage Visuel - Hotel App

## 📱 Installation PWA sur Android (la plus simple !)

### Étape 1 : Démarrer le serveur Django
```bash
python manage.py runserver 0.0.0.0:8000
```

### Étape 2 : Trouver votre IP locale
**Windows** :
```bash
ipconfig
# Cherchez "Adresse IPv4" (ex: 192.168.1.100)
```

**Linux/Mac** :
```bash
ifconfig
# Cherchez "inet" (ex: 192.168.1.100)
```

### Étape 3 : Sur votre téléphone Android
1. Ouvrez **Chrome** (navigateur Google)
2. Allez sur : `http://VOTRE_IP:8000`
   - Exemple : `http://192.168.1.100:8000`
3. Le site s'affiche normalement
4. Un bouton apparaît : **"📲 Installer l'application"**
5. Cliquez dessus
6. Confirmez l'installation
7. ✅ **L'icône apparaît sur votre écran d'accueil !**

**Avantages** :
- ✅ Aucune compilation nécessaire
- ✅ Installation en 30 secondes
- ✅ Mises à jour automatiques du site
- ✅ Fonctionne comme une app native

---

## 🖥️ Installation Windows (Electron)

### Étape 1 : Installer Node.js
Téléchargez depuis : https://nodejs.org/
Installez la version LTS (recommandée)

### Étape 2 : Installer les dépendances
```bash
cd AppBuild\electron-app
npm install
```

### Étape 3 : Tester en mode développement
```bash
npm start
```

L'application se lance et se connecte automatiquement à `http://localhost:8000`

### Étape 4 : Créer l'installeur Windows
```bash
npm run build:win
```

**Fichiers générés** :
- `dist/Hotel-App-Setup-1.0.0.exe` → Installeur complet
- `dist/Hotel-App-1.0.0.exe` → Version portable (sans installation)

### Étape 5 : Distribuer
- Copiez le fichier `.exe` sur une clé USB ou partagez-le
- Double-cliquez pour installer
- L'application apparaît dans le menu Démarrer

---

## 📲 Installation Android (APK Complet)

### Prérequis
1. **Android Studio** : https://developer.android.com/studio
2. **Java JDK 11+** (inclus avec Android Studio)
3. **Node.js** : https://nodejs.org/

### Étape 1 : Installer les dépendances
```bash
cd AppBuild\android-app
npm install
```

### Étape 2 : Configurer l'URL du serveur
Éditez `capacitor.config.json` :
```json
{
  "server": {
    "url": "http://192.168.1.100:8000"
  }
}
```
⚠️ **Important** : Remplacez par votre vraie IP !

### Étape 3 : Ajouter la plateforme Android
```bash
npx cap add android
```

### Étape 4 : Générer l'APK

**Version Debug (pour tests)** :
```bash
npm run build:debug
```
APK généré : `android/app/build/outputs/apk/debug/app-debug.apk`

**Version Release (production)** :
```bash
npm run build
```
APK généré : `android/app/build/outputs/apk/release/app-release.apk`

### Étape 5 : Installer sur le téléphone

**Méthode 1 : Via USB (ADB)**
```bash
adb install android/app/build/outputs/apk/debug/app-debug.apk
```

**Méthode 2 : Via fichier**
1. Copiez l'APK sur votre téléphone
2. Ouvrez le fichier
3. Autorisez "Sources inconnues"
4. Installez

---

## 🚀 Quelle méthode choisir ?

### Pour utilisateurs finaux (réseau local)
🥇 **PWA** (Recommandé)
- Installation en 30 secondes
- Pas de compilation
- Mises à jour automatiques
- Fonctionne comme une app native

### Pour distribution professionnelle
🥈 **APK Android**
- Installation via Play Store possible
- Icône personnalisée
- Notifications push possibles

🥉 **Electron Windows**
- Application PC complète
- Installation classique

---

## 📊 Comparaison Rapide

| Critère | PWA | APK | Electron |
|---------|-----|-----|----------|
| Installation | 30s | 5min | 5min |
| Compilation | ❌ Non | ✅ Oui | ✅ Oui |
| Taille | ~100KB | ~5MB | ~150MB |
| Auto-update | ✅ Oui | ✅ Oui | ✅ Oui |
| Difficulté | ⭐ | ⭐⭐⭐ | ⭐⭐ |

---

## 🎨 Personnalisation des icônes

Les icônes sont générées automatiquement, mais vous pouvez les personnaliser :

### Modifier les couleurs
Éditez `AppBuild/generate_icons.py` :
```python
config = {
    'bg_color': '#0f766e',  # Couleur de fond
    'text': 'H',            # Lettre affichée
    'text_color': 'white'   # Couleur du texte
}
```

### Regénérer les icônes
```bash
cd AppBuild
python generate_icons.py
```

### Utiliser vos propres icônes
Remplacez les fichiers dans :
- `AppBuild/static/icons/` (PWA)
- `AppBuild/electron-app/build/` (Electron)
- `AppBuild/android-app/android/app/src/main/res/` (Android)

---

## 🔧 Configuration du serveur Django

Pour accepter les connexions depuis le réseau local, modifiez `settings.py` :

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.100',  # Votre IP locale
    '*',              # Ou * pour tout accepter (développement uniquement)
]

# Désactiver CSRF pour les tests (UNIQUEMENT EN DÉVELOPPEMENT)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://192.168.1.100:8000',
]
```

---

## ✅ Checklist de test

### PWA
- [ ] Serveur Django démarré : `python manage.py runserver 0.0.0.0:8000`
- [ ] IP locale identifiée
- [ ] Chrome ouvert sur Android
- [ ] Site accessible : `http://VOTRE_IP:8000`
- [ ] Bouton "Installer" visible
- [ ] Application installée sur l'écran d'accueil
- [ ] Application lance le site correctement

### Electron
- [ ] Node.js installé
- [ ] `npm install` exécuté
- [ ] `npm start` lance l'application
- [ ] Application se connecte au serveur Django
- [ ] Build Windows créé : `npm run build:win`
- [ ] Installeur testé

### Android APK
- [ ] Android Studio installé
- [ ] Node.js installé
- [ ] `npm install` exécuté
- [ ] URL configurée dans `capacitor.config.json`
- [ ] Plateforme Android ajoutée
- [ ] APK généré
- [ ] APK installé sur téléphone
- [ ] Application se connecte au serveur

---

## 🆘 Dépannage rapide

### Le bouton PWA "Installer" n'apparaît pas
1. Vérifiez que vous êtes sur **Chrome** (pas Firefox/Safari)
2. Vérifiez que le manifest.json est accessible : `http://VOTRE_IP:8000/static/manifest.json`
3. Ouvrez DevTools > Application > Manifest
4. Vérifiez le Service Worker : DevTools > Application > Service Workers

### Electron ne se connecte pas
1. Vérifiez que Django est démarré : `python manage.py runserver`
2. Testez l'URL dans un navigateur : `http://localhost:8000`
3. Menu Electron : Fichier > Configurer le serveur

### Android APK erreur "ERR_CONNECTION_REFUSED"
1. Vérifiez l'URL dans `capacitor.config.json`
2. Vérifiez que le téléphone est sur le même réseau WiFi
3. Pingez l'IP depuis le téléphone (app "Network Utilities")
4. Vérifiez ALLOWED_HOSTS dans Django

### Icônes ne s'affichent pas
1. Exécutez : `python AppBuild/generate_icons.py`
2. Vérifiez que Pillow est installé : `pip install Pillow`
3. Django : `python manage.py collectstatic`

---

## 🎉 Félicitations !

Vous avez maintenant une application complète installable sur :
- ✅ Android (PWA en 30 secondes)
- ✅ Android (APK native)
- ✅ Windows (Application Electron)
- ✅ Linux (Application Electron)

**Le design et toutes les fonctionnalités de votre site Django sont préservés !**

---

## 📞 Support

Pour plus d'aide, consultez :
- `README.md` - Documentation complète
- `INTEGRATION_DJANGO.md` - Intégration PWA détaillée
- `electron-app/README.md` - Guide Electron
- `android-app/README.md` - Guide Android

**Bon développement ! 🚀**
