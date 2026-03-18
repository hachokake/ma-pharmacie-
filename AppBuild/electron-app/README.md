# 🖥️ Application Electron pour Windows/Linux

## Installation

1. Installer Node.js (si pas déjà fait) : https://nodejs.org/

2. Installer les dépendances :
```bash
cd electron-app
npm install
```

## Développement

Lancer l'application en mode développement :
```bash
npm start
```

## Build pour production

### Windows
```bash
npm run build:win
```
Génère :
- `dist/Hotel-App-Setup-1.0.0.exe` (installeur)
- `dist/Hotel-App-1.0.0.exe` (version portable)

### Linux
```bash
npm run build:linux
```
Génère :
- `dist/Hotel-App-1.0.0.AppImage` (portable)
- `dist/Hotel-App-1.0.0.deb` (Debian/Ubuntu)

### Tous les systèmes
```bash
npm run build:all
```

## Configuration

L'URL du serveur Django peut être configurée :
- Par défaut : `http://localhost:8000`
- Menu : Fichier > Configurer le serveur
- Ou modifier directement dans le fichier de configuration

## Icônes

Les icônes sont automatiquement générées et placées dans `build/`

## Distribution

Les fichiers de distribution se trouvent dans le dossier `dist/` après le build.
