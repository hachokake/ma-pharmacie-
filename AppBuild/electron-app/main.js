const { app, BrowserWindow, Menu, ipcMain, dialog } = require('electron');
const path = require('path');
const Store = require('electron-store');

// Configuration de l'application
const store = new Store();
let mainWindow;

// URL du serveur Django (configurable)
const DJANGO_URL = store.get('serverUrl', 'http://localhost:8000');

function createWindow() {
  // Créer la fenêtre principale
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 768,
    icon: path.join(__dirname, 'build', 'icon.ico'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
      allowRunningInsecureContent: false
    },
    backgroundColor: '#f0f8f5',
    show: false,
    autoHideMenuBar: true,
    title: 'PharmaCare - Gestion de Pharmacie'
  });

  // Menu personnalisé
  const menuTemplate = [
    {
      label: 'Fichier',
      submenu: [
        {
          label: 'Recharger',
          accelerator: 'CmdOrCtrl+R',
          click: () => mainWindow.reload()
        },
        {
          label: 'Configurer le serveur',
          click: () => showServerConfigDialog()
        },
        { type: 'separator' },
        {
          label: 'Quitter',
          accelerator: 'CmdOrCtrl+Q',
          click: () => app.quit()
        }
      ]
    },
    {
      label: 'Affichage',
      submenu: [
        {
          label: 'Plein écran',
          accelerator: 'F11',
          click: () => {
            const isFullScreen = mainWindow.isFullScreen();
            mainWindow.setFullScreen(!isFullScreen);
          }
        },
        {
          label: 'Zoom +',
          accelerator: 'CmdOrCtrl+Plus',
          click: () => {
            const currentZoom = mainWindow.webContents.getZoomLevel();
            mainWindow.webContents.setZoomLevel(currentZoom + 0.5);
          }
        },
        {
          label: 'Zoom -',
          accelerator: 'CmdOrCtrl+-',
          click: () => {
            const currentZoom = mainWindow.webContents.getZoomLevel();
            mainWindow.webContents.setZoomLevel(currentZoom - 0.5);
          }
        },
        {
          label: 'Réinitialiser le zoom',
          accelerator: 'CmdOrCtrl+0',
          click: () => mainWindow.webContents.setZoomLevel(0)
        },
        { type: 'separator' },
        {
          label: 'Outils de développement',
          accelerator: 'F12',
          click: () => mainWindow.webContents.toggleDevTools()
        }
      ]
    },
    {
      label: 'Aide',
      submenu: [
        {
          label: 'À propos',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'À propos de PharmaCare',
              message: 'PharmaCare - Gestion de Pharmacie',
              detail: `Version: 1.0.0\nElectron: ${process.versions.electron}\nChrome: ${process.versions.chrome}\nNode.js: ${process.versions.node}\n\nMise à jour automatique: Active`,
              buttons: ['OK']
            });
          }
        },
        {
          label: 'Vérifier les mises à jour',
          click: () => checkForUpdates()
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(menuTemplate);
  Menu.setApplicationMenu(menu);

  // Rechargement automatique pour détecter les changements du serveur Django
  // Vérifie toutes les 30 secondes si le serveur a des mises à jour
  let autoReloadInterval = setInterval(() => {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.reload();
      console.log('🔄 Rechargement automatique pour synchronisation');
    }
  }, 30000); // 30 secondes

  // Arrêter l'intervalle quand la fenêtre est fermée
  mainWindow.on('closed', () => {
    if (autoReloadInterval) {
      clearInterval(autoReloadInterval);
      autoReloadInterval = null;
    }
  });

  // Charger l'URL du serveur Django
  const serverUrl = store.get('serverUrl', DJANGO_URL);
  console.log(`📡 Chargement du serveur: ${serverUrl}`);
  
  mainWindow.loadURL(serverUrl).catch(err => {
    console.error('❌ Erreur de chargement:', err);
    // Afficher une page d'erreur personnalisée
    mainWindow.loadFile(path.join(__dirname, 'error.html'));
  });

  // Afficher la fenêtre quand elle est prête
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    console.log('✅ Fenêtre affichée');
  });

  // Gérer les liens externes (ouvrir dans le navigateur)
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    require('electron').shell.openExternal(url);
    return { action: 'deny' };
  });

  // Gérer la fermeture
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Détecter les erreurs de chargement
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error(`❌ Échec de chargement: ${errorDescription} (${errorCode})`);
    
    if (errorCode === -102 || errorCode === -6) { // ERR_CONNECTION_REFUSED ou ERR_CONNECTION_CLOSED
      showServerErrorDialog();
    }
  });
}

// Dialogue de configuration du serveur
async function showServerConfigDialog() {
  const result = await dialog.showMessageBox(mainWindow, {
    type: 'question',
    title: 'Configuration du serveur',
    message: 'Entrez l\'URL du serveur Django',
    detail: `URL actuelle: ${store.get('serverUrl', DJANGO_URL)}\n\nExemples:\n- http://localhost:8000\n- http://192.168.1.100:8000\n- https://monsite.com`,
    buttons: ['Annuler', 'Configurer'],
    defaultId: 1
  });

  if (result.response === 1) {
    // Ouvrir une boîte de dialogue pour entrer l'URL
    const { response } = await dialog.showMessageBox(mainWindow, {
      type: 'info',
      message: 'Entrez la nouvelle URL dans la console',
      buttons: ['OK']
    });
    
    // Alternative: utiliser un prompt simple
    mainWindow.webContents.executeJavaScript(`
      prompt('Entrez l\'URL du serveur Django:', '${store.get('serverUrl', DJANGO_URL)}')
    `).then(url => {
      if (url) {
        store.set('serverUrl', url);
        console.log(`✅ Nouvelle URL configurée: ${url}`);
        mainWindow.reload();
      }
    });
  }
}

// Dialogue d'erreur serveur
async function showServerErrorDialog() {
  const result = await dialog.showMessageBox(mainWindow, {
    type: 'error',
    title: 'Erreur de connexion',
    message: 'Impossible de se connecter au serveur Django',
    detail: `URL: ${store.get('serverUrl', DJANGO_URL)}\n\nAssurez-vous que:\n1. Le serveur Django est démarré\n2. L'URL est correcte\n3. Aucun pare-feu ne bloque la connexion`,
    buttons: ['Réessayer', 'Configurer le serveur', 'Quitter'],
    defaultId: 0
  });

  if (result.response === 0) {
    mainWindow.reload();
  } else if (result.response === 1) {
    showServerConfigDialog();
  } else {
    app.quit();
  }
}

// Vérifier les mises à jour (recharge la page pour synchroniser avec Django)
function checkForUpdates() {
  mainWindow.webContents.reload();
  dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: 'Mises à jour',
    message: 'Synchronisation avec le serveur',
    detail: 'PharmaCare v1.0.0\n\nL\'application se synchronise automatiquement avec votre serveur Django.\nToutes les modifications que vous faites dans VSCode sont immédiatement disponibles après rechargement.',
    buttons: ['OK']
  });
}

// IPC Handlers
ipcMain.handle('get-server-url', () => {
  return store.get('serverUrl', DJANGO_URL);
});

ipcMain.handle('set-server-url', (event, url) => {
  store.set('serverUrl', url);
  return true;
});

// Événements de l'application
app.whenReady().then(() => {
  console.log('🚀 Application Electron démarrée');
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Gérer les erreurs non capturées
process.on('uncaughtException', (error) => {
  console.error('❌ Erreur non capturée:', error);
});

console.log('📦 Application PharmaCare initialisée - Synchronisation automatique active');
