#!/usr/bin/env python
"""
Script de démarrage rapide pour Hotel App
Configure et lance l'environnement complet
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Affiche la bannière de démarrage"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         🏥 HOTEL APP - DÉMARRAGE RAPIDE 🏥               ║
║     Application de Gestion de Pharmacie Professionnelle  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Vérifie les dépendances nécessaires"""
    print("\n🔍 Vérification des dépendances...\n")
    
    dependencies = {
        'Python': sys.version_info >= (3, 8),
        'pip': True,
    }
    
    # Vérifier Node.js
    try:
        subprocess.run(['node', '--version'], capture_output=True, check=True)
        dependencies['Node.js'] = True
    except:
        dependencies['Node.js'] = False
    
    # Vérifier npm
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
        dependencies['npm'] = True
    except:
        dependencies['npm'] = False
    
    # Afficher les résultats
    all_ok = True
    for dep, status in dependencies.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {dep}")
        if not status:
            all_ok = False
    
    return all_ok

def install_python_packages():
    """Installe les packages Python nécessaires"""
    print("\n📦 Installation des packages Python...\n")
    
    packages = [
        'Django>=4.2',
        'Pillow',
    ]
    
    for package in packages:
        print(f"  Installing {package}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', package, '-q'])
    
    print("\n✅ Packages Python installés\n")

def generate_icons():
    """Génère les icônes pour toutes les plateformes"""
    print("\n🎨 Génération des icônes...\n")
    
    script_path = os.path.join('AppBuild', 'generate_icons.py')
    
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print("⚠️  Script generate_icons.py non trouvé")

def setup_pwa():
    """Configure la PWA dans Django"""
    print("\n📱 Configuration PWA...\n")
    
    # Créer les dossiers nécessaires
    static_dir = os.path.join('pharmacy', 'static')
    icons_dir = os.path.join(static_dir, 'icons')
    
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(icons_dir, exist_ok=True)
    
    print("✅ Dossiers créés")
    
    # Copier les fichiers PWA
    import shutil
    
    files_to_copy = [
        ('AppBuild/static/manifest.json', 'pharmacy/static/manifest.json'),
        ('AppBuild/static/service-worker.js', 'pharmacy/static/service-worker.js'),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"✅ Copié: {os.path.basename(src)}")
        else:
            print(f"⚠️  Non trouvé: {src}")

def start_django():
    """Démarre le serveur Django"""
    print("\n🚀 Démarrage du serveur Django...\n")
    print("=" * 60)
    print("Serveur disponible sur :")
    print("  • Local : http://localhost:8000")
    print("  • Réseau: http://[VOTRE_IP]:8000")
    print("\nPour installer sur Android :")
    print("  1. Ouvrez Chrome sur votre téléphone")
    print("  2. Allez sur http://[VOTRE_IP]:8000")
    print("  3. Cliquez sur 'Installer l'application'")
    print("=" * 60)
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur\n")
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\n\n👋 Serveur arrêté\n")

def show_menu():
    """Affiche le menu principal"""
    print("\n" + "=" * 60)
    print("MENU PRINCIPAL")
    print("=" * 60)
    print("\n1. 🚀 Démarrage complet (recommandé)")
    print("2. 🎨 Générer les icônes uniquement")
    print("3. 📱 Configurer la PWA")
    print("4. 🖥️  Installer Electron (Windows/Linux)")
    print("5. 📲 Installer Android (Capacitor)")
    print("6. 🌐 Démarrer Django uniquement")
    print("7. 📚 Afficher la documentation")
    print("8. ❌ Quitter")
    print("\n" + "=" * 60)
    
    choice = input("\nChoisissez une option (1-8) : ").strip()
    return choice

def install_electron():
    """Installe les dépendances Electron"""
    print("\n🖥️  Installation Electron...\n")
    
    electron_dir = os.path.join('AppBuild', 'electron-app')
    
    if os.path.exists(electron_dir):
        os.chdir(electron_dir)
        print("📦 Installation des dépendances npm...")
        subprocess.run(['npm', 'install'])
        os.chdir('../..')
        print("\n✅ Electron installé")
        print("\nPour démarrer :")
        print(f"  cd {electron_dir}")
        print("  npm start")
    else:
        print("❌ Dossier electron-app non trouvé")

def install_android():
    """Installe les dépendances Android"""
    print("\n📲 Installation Android (Capacitor)...\n")
    
    android_dir = os.path.join('AppBuild', 'android-app')
    
    if os.path.exists(android_dir):
        os.chdir(android_dir)
        print("📦 Installation des dépendances npm...")
        subprocess.run(['npm', 'install'])
        print("\n📱 Ajout de la plateforme Android...")
        subprocess.run(['npx', 'cap', 'add', 'android'])
        os.chdir('../..')
        print("\n✅ Android installé")
        print("\nPour générer l'APK :")
        print(f"  cd {android_dir}")
        print("  npm run build:debug")
    else:
        print("❌ Dossier android-app non trouvé")

def show_documentation():
    """Affiche les liens vers la documentation"""
    print("\n📚 Documentation disponible :\n")
    print("  • README.md                    - Vue d'ensemble complète")
    print("  • INTEGRATION_DJANGO.md        - Intégration PWA dans Django")
    print("  • electron-app/README.md       - Guide Electron")
    print("  • android-app/README.md        - Guide Android")
    print("\n💡 Consultez ces fichiers pour plus de détails\n")

def full_setup():
    """Installation complète"""
    print("\n🚀 INSTALLATION COMPLÈTE\n")
    
    if not check_dependencies():
        print("\n⚠️  Certaines dépendances sont manquantes.")
        print("Veuillez installer Node.js depuis https://nodejs.org/")
        return
    
    install_python_packages()
    generate_icons()
    setup_pwa()
    
    print("\n" + "=" * 60)
    print("✅ INSTALLATION TERMINÉE !")
    print("=" * 60)
    print("\nProchaines étapes :")
    print("  1. Démarrer Django : python quick_start.py (option 6)")
    print("  2. Installer Electron : option 4")
    print("  3. Installer Android : option 5")
    print("\n")

def main():
    """Point d'entrée principal"""
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            full_setup()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '2':
            generate_icons()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '3':
            setup_pwa()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '4':
            install_electron()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '5':
            install_android()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '6':
            start_django()
        elif choice == '7':
            show_documentation()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '8':
            print("\n👋 Au revoir !\n")
            break
        else:
            print("\n❌ Option invalide. Choisissez entre 1 et 8.\n")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu\n")
        sys.exit(0)
