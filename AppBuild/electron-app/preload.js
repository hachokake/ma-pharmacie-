const { contextBridge, ipcRenderer } = require('electron');

// Exposer des API sécurisées au renderer
contextBridge.exposeInMainWorld('electronAPI', {
  // Récupérer l'URL du serveur
  getServerUrl: () => ipcRenderer.invoke('get-server-url'),
  
  // Définir l'URL du serveur
  setServerUrl: (url) => ipcRenderer.invoke('set-server-url', url),
  
  // Informations de la plateforme
  platform: process.platform,
  versions: process.versions
});

console.log('🔒 Preload script chargé - Context isolation activée');
