"""
Script pour réinitialiser tous les comptes utilisateurs
Usage: python reset_users.py
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')
django.setup()

from django.contrib.auth.models import User
from pharmacy.models import ActivityLog

def reset_all_users():
    """Supprimer tous les utilisateurs et leurs données associées"""
    print("=" * 60)
    print("RÉINITIALISATION DES COMPTES UTILISATEURS")
    print("=" * 60)
    
    # Compter les utilisateurs actuels
    user_count = User.objects.count()
    print(f"\nUtilisateurs actuels : {user_count}")
    
    if user_count == 0:
        print("Aucun utilisateur à supprimer.")
        return
    
    # Demander confirmation
    print("\n⚠️  ATTENTION : Cette opération va supprimer TOUS les utilisateurs !")
    print("   - Tous les comptes administrateurs")
    print("   - Tous les comptes employés")
    print("   - Toutes les activités liées")
    
    confirmation = input("\nÊtes-vous sûr de vouloir continuer ? (tapez 'OUI' pour confirmer) : ")
    
    if confirmation != 'OUI':
        print("\n❌ Opération annulée.")
        return
    
    try:
        # Supprimer les logs d'activités
        activity_count = ActivityLog.objects.count()
        ActivityLog.objects.all().delete()
        print(f"\n✅ {activity_count} logs d'activités supprimés")
        
        # Supprimer tous les utilisateurs
        User.objects.all().delete()
        print(f"✅ {user_count} utilisateurs supprimés")
        
        print("\n" + "=" * 60)
        print("✅ RÉINITIALISATION TERMINÉE")
        print("=" * 60)
        print("\nVous pouvez maintenant créer un nouveau compte administrateur.")
        print("Accédez à : http://127.0.0.1:8000/create-first-admin/")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la réinitialisation : {e}")
        sys.exit(1)

if __name__ == '__main__':
    reset_all_users()
