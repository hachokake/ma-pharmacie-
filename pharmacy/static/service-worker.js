// Service Worker pour PWA - Gestion de cache et mode offline
const CACHE_NAME = 'hotel-app-v1';
const STATIC_CACHE = 'hotel-static-v1';
const DYNAMIC_CACHE = 'hotel-dynamic-v1';

// Fichiers à mettre en cache lors de l'installation
const STATIC_ASSETS = [
  '/',
  '/static/manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap'
];

// Installation du Service Worker
self.addEventListener('install', (event) => {
  console.log('[SW] Installation en cours...');
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      console.log('[SW] Mise en cache des fichiers statiques');
      return cache.addAll(STATIC_ASSETS.map(url => new Request(url, { mode: 'no-cors' })))
        .catch(err => {
          console.warn('[SW] Erreur lors de la mise en cache:', err);
          // Continue même si certains fichiers ne peuvent pas être mis en cache
        });
    })
  );
  self.skipWaiting();
});

// Activation du Service Worker
self.addEventListener('activate', (event) => {
  console.log('[SW] Activation en cours...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
            console.log('[SW] Suppression ancien cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// Stratégie de cache : Network First avec fallback sur cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  
  // Ignorer les requêtes non-GET
  if (request.method !== 'GET') {
    return;
  }

  // Ignorer les requêtes admin Django
  if (request.url.includes('/admin/')) {
    return;
  }

  event.respondWith(
    fetch(request)
      .then((response) => {
        // Cloner la réponse car elle ne peut être utilisée qu'une fois
        const responseClone = response.clone();
        
        // Mettre en cache uniquement les réponses valides
        if (response.status === 200) {
          caches.open(DYNAMIC_CACHE).then((cache) => {
            cache.put(request, responseClone);
          });
        }
        
        return response;
      })
      .catch(() => {
        // Si le réseau échoue, chercher dans le cache
        return caches.match(request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          
          // Si pas en cache, retourner une page offline pour les pages HTML
          if (request.headers.get('accept').includes('text/html')) {
            return new Response(
              `<!DOCTYPE html>
              <html lang="fr">
              <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Hors ligne - Hotel App</title>
                <style>
                  body {
                    font-family: 'Poppins', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
                    color: white;
                    text-align: center;
                  }
                  .offline-container {
                    max-width: 400px;
                    padding: 30px;
                  }
                  h1 { font-size: 3em; margin-bottom: 20px; }
                  p { font-size: 1.2em; margin-bottom: 20px; }
                  button {
                    background: white;
                    color: #0f766e;
                    border: none;
                    padding: 15px 30px;
                    font-size: 1em;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: 600;
                  }
                  button:hover { opacity: 0.9; }
                </style>
              </head>
              <body>
                <div class="offline-container">
                  <h1>📴</h1>
                  <h2>Mode Hors Ligne</h2>
                  <p>Vous n'êtes pas connecté à Internet. Veuillez vérifier votre connexion.</p>
                  <button onclick="window.location.reload()">Réessayer</button>
                </div>
              </body>
              </html>`,
              {
                headers: { 'Content-Type': 'text/html' }
              }
            );
          }
        });
      })
  );
});

// Gestion des messages du client
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => caches.delete(cacheName))
      );
    }).then(() => {
      console.log('[SW] Cache vidé');
    });
  }
});
