# 📱 Application Android avec Capacitor

## Prérequis

1. **Node.js** : https://nodejs.org/
2. **Android Studio** : https://developer.android.com/studio
3. **Java JDK 11+** : Inclus avec Android Studio

## Installation

### 1. Installer les dépendances
```bash
cd android-app
npm install
```

### 2. Initialiser Capacitor (première fois uniquement)
```bash
npm run init
```

### 3. Ajouter la plateforme Android
```bash
npm run add:android
```

### 4. Configurer l'URL du serveur

Éditez `capacitor.config.json` et modifiez l'URL :
```json
{
  "server": {
    "url": "http://VOTRE_IP:8000"
  }
}
```

**Important** : Remplacez `VOTRE_IP` par :
- Votre IP locale (ex: `192.168.1.100`) pour réseau local
- Votre IP publique ou domaine pour accès externe

## Build

### APK Debug (pour test)
```bash
npm run build:debug
```
APK généré : `android/app/build/outputs/apk/debug/app-debug.apk`

### APK Release (pour production)
```bash
npm run build
```
APK généré : `android/app/build/outputs/apk/release/app-release.apk`

## Installation sur Android

### Via USB (ADB)
```bash
adb install android/app/build/outputs/apk/debug/app-debug.apk
```

### Via fichier
1. Copier l'APK sur votre téléphone
2. Ouvrir le fichier et installer
3. Autoriser "Sources inconnues" si demandé

## Développement

### Synchroniser les changements
```bash
npm run sync
```

### Ouvrir dans Android Studio
```bash
npm run open:android
```

## Mise à jour automatique

L'application se connecte directement au serveur Django. Toute modification du site sera visible automatiquement dans l'app.

## Débogage

### Voir les logs Android
```bash
adb logcat | grep Capacitor
```

### Inspecter le WebView
1. Activer le débogage dans `capacitor.config.json` :
   ```json
   "android": {
     "webContentsDebuggingEnabled": true
   }
   ```
2. Ouvrir Chrome : `chrome://inspect`
3. Sélectionner votre appareil

## Icônes

Les icônes sont automatiquement générées par le script `generate_icons.py` dans les dossiers Android appropriés.

## Notes

- L'application fonctionne comme un wrapper WebView du site Django
- Assurez-vous que le serveur Django accepte les connexions depuis votre IP
- Pour production, utilisez HTTPS pour plus de sécurité
