# 📦 Hotel App - Transformation en Application Installable

## 🎯 Projet Complet

Ce projet transforme votre site Django en une application installable sur **Android** et **PC Windows/Linux**, avec support PWA, sans modifier le code Django existant.

---

## 📁 Structure du projet AppBuild

```
AppBuild/
├── static/                          # Fichiers PWA
│   ├── manifest.json               # Configuration PWA
│   ├── service-worker.js           # Cache et offline
│   └── icons/                      # Icônes générées automatiquement
│       ├── icon-192x192.png
│       ├── icon-512x512.png
│       └── ...
│
├── templates/                       # Templates modifiés
│   └── base_pwa.html               # Base.html avec support PWA
│
├── electron-app/                    # Application Windows/Linux
│   ├── package.json
│   ├── main.js                     # Point d'entrée Electron
│   ├── preload.js                  # Script de sécurité
│   ├── error.html                  # Page d'erreur
│   └── build/                      # Icônes générées
│       ├── icon.ico
│       └── ...
│
├── android-app/                     # Application Android
│   ├── package.json
│   ├── capacitor.config.json       # Configuration Capacitor
│   └── www/
│       └── index.html              # Page de démarrage
│
├── generate_icons.py                # Génération automatique d'icônes
├── INTEGRATION_DJANGO.md            # Guide d'intégration Django
└── README.md                        # Ce fichier
```

---

## 🚀 Installation Rapide

### 1️⃣ Générer les icônes

```bash
cd AppBuild
python generate_icons.py
```

**Prérequis** : `pip install Pillow`

### 2️⃣ Intégrer la PWA dans Django

Suivez le guide complet dans [INTEGRATION_DJANGO.md](INTEGRATION_DJANGO.md)

**Résumé rapide** :
```bash
# Copier les fichiers
cp AppBuild/static/manifest.json pharmacy/static/
cp AppBuild/static/service-worker.js pharmacy/static/

# Modifier base.html (voir INTEGRATION_DJANGO.md)

# Collecter les fichiers statiques
python manage.py collectstatic
```

### 3️⃣ Tester la PWA

```bash
# Démarrer Django
python manage.py runserver 0.0.0.0:8000

# Sur Android :
# 1. Ouvrir Chrome
# 2. Aller sur http://VOTRE_IP:8000
# 3. Cliquer sur "Installer l'application"
```

---

## 🖥️ Application Windows/Linux (Electron)

### Installation

```bash
cd AppBuild/electron-app
npm install
```

### Développement

```bash
npm start
```

### Build pour production

**Windows** :
```bash
npm run build:win
```
Génère : `dist/Hotel-App-Setup-1.0.0.exe`

**Linux** :
```bash
npm run build:linux
```
Génère : `dist/Hotel-App-1.0.0.AppImage`

**Tous** :
```bash
npm run build:all
```

### Configuration

- URL par défaut : `http://localhost:8000`
- Configurable via : Menu > Fichier > Configurer le serveur

---

## 📱 Application Android (Capacitor)

### Prérequis

- Node.js
- Android Studio
- Java JDK 11+

### Installation

```bash
cd AppBuild/android-app
npm install
npm run add:android
```

### Configuration de l'URL

Éditez `capacitor.config.json` :
```json
{
  "server": {
    "url": "http://VOTRE_IP:8000"
  }
}
```

### Build

**APK Debug** (pour test) :
```bash
npm run build:debug
```
APK : `android/app/build/outputs/apk/debug/app-debug.apk`

**APK Release** (production) :
```bash
npm run build
```
APK : `android/app/build/outputs/apk/release/app-release.apk`

### Installation sur téléphone

**Via USB** :
```bash
adb install android/app/build/outputs/apk/debug/app-debug.apk
```

**Via fichier** :
1. Copier l'APK sur le téléphone
2. Ouvrir et installer
3. Autoriser "Sources inconnues" si nécessaire

---

## 🎨 Icônes

Les icônes sont générées automatiquement par `generate_icons.py` :

- **PWA** : 192x192, 512x512, et autres tailles
- **Electron** : 16x16 à 1024x1024 + .ico pour Windows
- **Android** : Toutes les densités (ldpi, mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi)

**Personnalisation** :
Éditez `generate_icons.py` pour changer :
- `bg_color` : Couleur de fond (ex: `#0f766e`)
- `text` : Lettre affichée (ex: `H` pour Hotel)
- `text_color` : Couleur du texte

---

## 🔄 Mise à jour automatique

### PWA
- Le Service Worker met à jour automatiquement les fichiers en cache
- Notification de nouvelle version disponible

### Electron
- L'application se connecte directement au serveur Django
- Toute modification du site est visible immédiatement

### Android
- L'application est un WebView du site Django
- Pas besoin de republier l'APK pour les mises à jour du site

---

## ✅ Checklist de déploiement

### PWA
- [ ] Icônes générées
- [ ] manifest.json copié dans Django
- [ ] service-worker.js copié dans Django
- [ ] base.html modifié avec les meta tags PWA
- [ ] `collectstatic` exécuté
- [ ] Test sur Chrome Android

### Electron
- [ ] Icônes générées
- [ ] `npm install` exécuté
- [ ] Test en mode développement (`npm start`)
- [ ] Build Windows/Linux créé
- [ ] Installeur testé

### Android
- [ ] Icônes générées
- [ ] URL configurée dans `capacitor.config.json`
- [ ] `npm install` exécuté
- [ ] Plateforme Android ajoutée
- [ ] APK généré
- [ ] APK installé et testé sur appareil

---

## 🛠️ Résolution de problèmes

### PWA ne s'installe pas
- Vérifier que vous êtes en HTTPS (ou localhost)
- Vérifier le manifest.json dans Chrome DevTools > Application
- Vérifier que le Service Worker est enregistré

### Electron ne se connecte pas
- Vérifier que Django est démarré : `python manage.py runserver`
- Vérifier l'URL configurée
- Tester l'URL dans un navigateur

### Android APK ne se connecte pas
- Vérifier l'URL dans `capacitor.config.json`
- Vérifier que le téléphone est sur le même réseau
- Vérifier ALLOWED_HOSTS dans Django settings.py

### Icônes ne s'affichent pas
- Exécuter `python generate_icons.py`
- Vérifier que Pillow est installé : `pip install Pillow`
- Exécuter `python manage.py collectstatic`

---

## 📊 Comparaison des solutions

| Fonctionnalité | PWA | Electron | Android APK |
|----------------|-----|----------|-------------|
| Installation | Chrome | .exe/AppImage | .apk |
| Taille | ~100KB | ~150MB | ~5MB |
| Plateforme | Web/Android | Windows/Linux | Android |
| Offline | Partiel | Non | Non |
| Auto-update | Oui | Via WebView | Via WebView |
| Distribution | Web | Fichier | Play Store/Fichier |

---

## 🎯 Recommandations

### Pour utilisateurs internes (réseau local)
1. **PWA** : Installation rapide depuis Chrome
2. **Electron** : Application PC complète
3. **Android APK** : App mobile native

### Pour utilisateurs externes (Internet)
1. **PWA** : Meilleure solution (légère, auto-update)
2. **Publier sur Play Store** : APK pour distribution large
3. **Electron** : Pour utilisateurs PC sans accès web

---

## 📞 Support

### Logs et débogage

**PWA** :
- Chrome DevTools > Console
- Application > Service Workers

**Electron** :
- F12 pour DevTools
- Console dans le terminal

**Android** :
```bash
adb logcat | grep Capacitor
```

---

## 📝 Notes importantes

1. **Sécurité** :
   - En production, utilisez HTTPS
   - Configurez correctement ALLOWED_HOSTS dans Django
   - Signez l'APK Android pour le Play Store

2. **Performance** :
   - Le Service Worker met en cache les ressources statiques
   - La première visite peut être lente, puis rapide

3. **Compatibilité** :
   - PWA : Chrome, Edge, Safari (limité)
   - Electron : Windows 10+, Ubuntu 18.04+
   - Android : Android 5.0+ (API 21+)

---

## 🎉 Félicitations !

Votre application Django est maintenant installable sur :
- ✅ Android (via PWA ou APK)
- ✅ Windows (via Electron)
- ✅ Linux (via Electron)

**Le design et la logique restent identiques au site Django !**

---

## 📚 Documentation complète

- [INTEGRATION_DJANGO.md](INTEGRATION_DJANGO.md) - Guide d'intégration PWA dans Django
- [electron-app/README.md](electron-app/README.md) - Guide Electron
- [android-app/README.md](android-app/README.md) - Guide Android Capacitor

---

## 📄 Licence

MIT License - Libre d'utilisation pour votre projet

---

**Créé avec ❤️ pour Hotel App**
