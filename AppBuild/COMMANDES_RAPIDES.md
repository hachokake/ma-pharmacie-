# ⚡ COMMANDES RAPIDES - Hotel App

Toutes les commandes essentielles en un seul endroit !

---

## 🚀 INSTALLATION PWA (RECOMMANDÉ - 30 SECONDES)

### Étape 1 : Copier les fichiers
```powershell
# Windows PowerShell
copy AppBuild\static\manifest.json pharmacy\static\
copy AppBuild\static\service-worker.js pharmacy\static\
```

```bash
# Linux/Mac
cp AppBuild/static/manifest.json pharmacy/static/
cp AppBuild/static/service-worker.js pharmacy/static/
```

### Étape 2 : Modifier base.html
Ajoutez dans `<head>` de `pharmacy/templates/pharmacy/base.html` :
```html
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#0d6efd">
```

### Étape 3 : Démarrer Django
```bash
python manage.py runserver 0.0.0.0:8000
```

### Étape 4 : Trouver votre IP
```powershell
# Windows
ipconfig
# Cherchez "Adresse IPv4"
```

```bash
# Linux/Mac
ifconfig
# ou
ip addr
```

### Étape 5 : Installer sur Android
1. Chrome Android → `http://VOTRE_IP:8000`
2. Cliquer "📲 Installer l'application"
3. ✅ Terminé !

---

## 🎨 GÉNÉRATION DES ICÔNES

### Installation Pillow
```bash
pip install Pillow
```

### Générer toutes les icônes
```bash
cd AppBuild
python generate_icons.py
```

### Personnaliser les icônes
Éditez `generate_icons.py`, ligne 62 :
```python
config = {
    'bg_color': '#0f766e',     # Votre couleur
    'text': 'H',               # Votre lettre
    'text_color': 'white'      # Couleur du texte
}
```

Puis regénérez :
```bash
python generate_icons.py
```

---

## 🖥️ ELECTRON (WINDOWS/LINUX)

### Installation initiale
```bash
cd AppBuild/electron-app
npm install
```

### Développement
```bash
npm start
```

### Build Windows
```bash
npm run build:win
```
Résultat : `dist/Hotel-App-Setup-1.0.0.exe`

### Build Linux
```bash
npm run build:linux
```
Résultat : `dist/Hotel-App-1.0.0.AppImage`

### Build tous les systèmes
```bash
npm run build:all
```

### Configurer l'URL du serveur
Dans l'application : Menu → Fichier → Configurer le serveur

---

## 📱 ANDROID APK

### Installation initiale
```bash
cd AppBuild/android-app
npm install
```

### Configurer l'URL
Éditez `capacitor.config.json` :
```json
{
  "server": {
    "url": "http://192.168.1.100:8000"
  }
}
```
⚠️ Remplacez par votre vraie IP !

### Ajouter la plateforme Android
```bash
npx cap add android
```

### Synchroniser les changements
```bash
npm run sync
```

### Build APK Debug (pour tests)
```bash
npm run build:debug
```
Résultat : `android/app/build/outputs/apk/debug/app-debug.apk`

### Build APK Release (production)
```bash
npm run build
```
Résultat : `android/app/build/outputs/apk/release/app-release.apk`

### Ouvrir dans Android Studio
```bash
npm run open:android
```

### Installer sur téléphone (via USB)
```bash
# Activer le débogage USB sur le téléphone
adb install android/app/build/outputs/apk/debug/app-debug.apk
```

---

## 🛠️ DJANGO

### Démarrer le serveur (réseau local)
```bash
python manage.py runserver 0.0.0.0:8000
```

### Collecter les fichiers statiques
```bash
python manage.py collectstatic
```

### Créer un superuser
```bash
python manage.py createsuperuser
```

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔍 VÉRIFICATIONS

### Vérifier le manifest PWA
```bash
# Dans le navigateur
http://localhost:8000/static/manifest.json
```

### Vérifier le service worker
```bash
http://localhost:8000/static/service-worker.js
```

### Vérifier les icônes
```bash
http://localhost:8000/static/icons/icon-192x192.png
```

### Tester la PWA (Chrome DevTools)
1. F12 → Onglet "Application"
2. Vérifier "Manifest"
3. Vérifier "Service Workers"

---

## 📲 INSTALLATION SUR TÉLÉPHONE

### Via fichier APK
1. Copier l'APK sur le téléphone
2. Ouvrir le fichier
3. Autoriser "Sources inconnues"
4. Installer

### Via ADB (USB)
```bash
# Vérifier la connexion
adb devices

# Installer
adb install chemin/vers/app-debug.apk

# Désinstaller
adb uninstall com.hotelapp.pharmacy
```

### Via PWA (Chrome)
1. Chrome → URL du site
2. Menu (⋮) → "Ajouter à l'écran d'accueil"
3. Ou cliquer sur le bouton "Installer l'application"

---

## 🐛 DÉBOGAGE

### Logs Django
```bash
python manage.py runserver
# Les logs s'affichent dans la console
```

### Logs Electron
```bash
# Dans l'application
F12 → Console

# Ou dans le terminal
npm start
```

### Logs Android
```bash
# Tous les logs
adb logcat

# Logs Capacitor uniquement
adb logcat | grep Capacitor

# Logs de votre app
adb logcat | grep HotelApp
```

### Inspecter le WebView Android
1. Activer le débogage dans `capacitor.config.json` :
   ```json
   "android": {
     "webContentsDebuggingEnabled": true
   }
   ```
2. Chrome PC → `chrome://inspect`
3. Sélectionner votre appareil

---

## 🔄 MISES À JOUR

### PWA
Automatique ! Le Service Worker met à jour automatiquement.

### Forcer la mise à jour PWA
```javascript
// Dans la console du navigateur
navigator.serviceWorker.getRegistrations().then(function(registrations) {
  for(let registration of registrations) {
    registration.update();
  }
});
```

### Vider le cache PWA
```javascript
// Dans la console
caches.keys().then(function(names) {
  for (let name of names) caches.delete(name);
});
```

### Electron
L'application se connecte au serveur Django → mise à jour automatique

### Android APK
L'application charge le site Django → mise à jour automatique

---

## 🧹 NETTOYAGE

### Supprimer les node_modules
```bash
# Electron
rm -rf AppBuild/electron-app/node_modules

# Android
rm -rf AppBuild/android-app/node_modules
```

### Supprimer les builds
```bash
# Electron
rm -rf AppBuild/electron-app/dist

# Android
rm -rf AppBuild/android-app/android/app/build
```

### Réinstaller proprement
```bash
cd AppBuild/electron-app
rm -rf node_modules package-lock.json
npm install

# Ou pour Android
cd AppBuild/android-app
rm -rf node_modules package-lock.json
npm install
```

---

## 📦 DISTRIBUTION

### PWA
Aucune distribution nécessaire ! Les utilisateurs installent depuis le site.

### Electron Windows
1. Build : `npm run build:win`
2. Partager : `dist/Hotel-App-Setup-1.0.0.exe`

### Android APK
1. Build : `npm run build:debug` (ou `build` pour release)
2. Partager : `android/app/build/outputs/apk/debug/app-debug.apk`

---

## 🚀 SCRIPT AUTOMATIQUE

### Menu interactif complet
```bash
cd AppBuild
python quick_start.py
```

Options disponibles :
1. Installation complète
2. Générer les icônes
3. Configurer la PWA
4. Installer Electron
5. Installer Android
6. Démarrer Django
7. Documentation
8. Quitter

---

## ⚙️ CONFIGURATION

### Changer l'URL du serveur

**PWA** : Automatique (URL actuelle)

**Electron** :
- Menu → Fichier → Configurer le serveur
- Ou modifier dans l'app

**Android** :
```json
// capacitor.config.json
{
  "server": {
    "url": "http://NOUVELLE_URL:8000"
  }
}
```

### Changer le nom de l'app

**PWA** : Éditez `manifest.json`
```json
{
  "name": "Nouveau Nom",
  "short_name": "Nom"
}
```

**Electron** : Éditez `package.json`
```json
{
  "name": "nouveau-nom",
  "productName": "Nouveau Nom"
}
```

**Android** : Éditez `capacitor.config.json`
```json
{
  "appName": "Nouveau Nom"
}
```

---

## 📊 VÉRIFIER LES VERSIONS

### Node.js et npm
```bash
node --version
npm --version
```

### Python et pip
```bash
python --version
pip --version
```

### Electron
```bash
cd AppBuild/electron-app
npm list electron
```

### Capacitor
```bash
cd AppBuild/android-app
npm list @capacitor/core
```

---

## 🆘 COMMANDES DE DÉPANNAGE

### PWA ne s'installe pas
```bash
# Vérifier le manifest
curl http://localhost:8000/static/manifest.json

# Vérifier le service worker
curl http://localhost:8000/static/service-worker.js
```

### Electron ne se lance pas
```bash
cd AppBuild/electron-app
rm -rf node_modules package-lock.json
npm install
npm start
```

### Android APK erreur de build
```bash
cd AppBuild/android-app
rm -rf android
npm run add:android
npm run sync
npm run build:debug
```

### Django erreur ALLOWED_HOSTS
Éditez `pharmacy_project/settings.py` :
```python
ALLOWED_HOSTS = ['*']  # Pour développement uniquement
```

---

## 📝 COMMANDES UTILES

### Trouver les processus Django
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### Tuer un processus
```bash
# Windows
taskkill /PID [PID] /F

# Linux/Mac
kill -9 [PID]
```

### Vérifier la connectivité réseau
```bash
# Ping vers le serveur
ping 192.168.1.100

# Test connexion HTTP
curl http://192.168.1.100:8000
```

---

## 🎯 COMMANDES LES PLUS UTILISÉES

```bash
# 1. Générer les icônes (une fois)
python AppBuild/generate_icons.py

# 2. Démarrer Django (à chaque session)
python manage.py runserver 0.0.0.0:8000

# 3. Tester Electron (développement)
cd AppBuild/electron-app && npm start

# 4. Build Electron Windows (distribution)
cd AppBuild/electron-app && npm run build:win

# 5. Build Android APK (distribution)
cd AppBuild/android-app && npm run build:debug
```

---

**Toutes les commandes en un coup d'œil ! ⚡**
