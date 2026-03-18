# 🚀 Guide d'intégration des fichiers PWA dans Django

## Étape 1 : Copier les fichiers statiques

### 1.1 Copier les fichiers PWA
```bash
# Depuis la racine du projet
cp AppBuild/static/manifest.json pharmacy/static/
cp AppBuild/static/service-worker.js pharmacy/static/
```

### 1.2 Créer le dossier icons
```bash
mkdir -p pharmacy/static/icons
```

## Étape 2 : Générer les icônes

```bash
cd AppBuild
python generate_icons.py
```

Cela va créer automatiquement :
- `static/icons/icon-192x192.png`
- `static/icons/icon-512x512.png`
- Toutes les autres tailles nécessaires

## Étape 3 : Modifier settings.py

Ajoutez à votre `pharmacy_project/settings.py` :

```python
# Configuration pour accepter les connexions depuis le réseau local
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '10.79.9.100',  # Votre IP locale
    '192.168.*',    # Tout votre réseau local
    '*',            # Pour développement uniquement
]

# Configuration des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'pharmacy', 'static'),
]
```

## Étape 4 : Modifier urls.py

Ajoutez à votre `pharmacy_project/urls.py` :

```python
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pharmacy.urls')),
    
    # Routes PWA
    path('manifest.json', TemplateView.as_view(
        template_name='manifest.json',
        content_type='application/json'
    )),
    path('service-worker.js', TemplateView.as_view(
        template_name='service-worker.js',
        content_type='application/javascript'
    )),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## Étape 5 : Modifier base.html

### Option A : Remplacer complètement
```bash
cp AppBuild/templates/base_pwa.html pharmacy/templates/pharmacy/base.html
```

### Option B : Ajouter manuellement

Ajoutez dans le `<head>` de votre `base.html` existant :

```html
<!-- PWA Meta Tags -->
<meta name="description" content="Application de gestion de pharmacie professionnelle">
<meta name="theme-color" content="#0d6efd">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Hotel App">

<!-- PWA Manifest -->
<link rel="manifest" href="{% static 'manifest.json' %}">

<!-- PWA Icons -->
<link rel="icon" type="image/png" sizes="192x192" href="{% static 'icons/icon-192x192.png' %}">
<link rel="icon" type="image/png" sizes="512x512" href="{% static 'icons/icon-512x512.png' %}">
<link rel="apple-touch-icon" href="{% static 'icons/icon-192x192.png' %}">
```

Et avant la fermeture du `</body>` :

```html
<!-- Bouton d'installation PWA -->
<button id="installButton" class="install-button">
    📲 Installer l'application
</button>

<!-- Script PWA -->
<script src="{% static 'pwa-install.js' %}"></script>
```

## Étape 6 : Créer pwa-install.js

Copiez le contenu du script PWA depuis `AppBuild/templates/base_pwa.html` vers un nouveau fichier `pharmacy/static/pwa-install.js`

## Étape 7 : Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

## Étape 8 : Tester

### 8.1 Démarrer le serveur
```bash
python manage.py runserver 0.0.0.0:8000
```

### 8.2 Accéder depuis votre téléphone
- Ouvrez Chrome sur Android
- Allez sur `http://VOTRE_IP:8000`
- Vous devriez voir le bouton "Installer l'application"

### 8.3 Installer la PWA
- Cliquez sur "Installer l'application"
- L'application sera ajoutée à votre écran d'accueil

## Vérification

✅ Le manifest.json est accessible : `http://localhost:8000/manifest.json`
✅ Le service worker est accessible : `http://localhost:8000/service-worker.js`
✅ Les icônes sont accessibles : `http://localhost:8000/static/icons/icon-192x192.png`
✅ Le bouton d'installation apparaît
✅ L'application peut être installée sur Android

## Résolution de problèmes

### Le bouton d'installation n'apparaît pas
- Vérifiez que vous êtes en HTTPS (ou localhost)
- Vérifiez que le manifest.json est valide
- Vérifiez que le service worker est enregistré (Console > Application)

### Les icônes ne s'affichent pas
- Exécutez `python manage.py collectstatic`
- Vérifiez les chemins dans manifest.json

### Erreur CORS
Ajoutez à `settings.py` :
```python
CORS_ALLOW_ALL_ORIGINS = True  # Pour développement
```
