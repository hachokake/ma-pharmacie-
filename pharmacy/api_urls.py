"""
URLs pour l'API REST de la pharmacie
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .api_views import (
    MedicamentViewSet, CategorieViewSet, ClientViewSet, VenteViewSet,
    LotMedicamentViewSet, MouvementStockViewSet, MedecinViewSet,
    PrescriptionViewSet, AssuranceViewSet, CaisseViewSet, SessionCaisseViewSet,
    InventaireViewSet, FournisseurViewSet, CommandeViewSet,
    ActivityLogViewSet, CarteEmployeViewSet, StatistiquesViewSet
)

# Créer le router
router = DefaultRouter()

# Enregistrer les viewsets
router.register(r'medicaments', MedicamentViewSet, basename='medicament')
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'ventes', VenteViewSet, basename='vente')
router.register(r'lots', LotMedicamentViewSet, basename='lot')
router.register(r'mouvements-stock', MouvementStockViewSet, basename='mouvement-stock')
router.register(r'medecins', MedecinViewSet, basename='medecin')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'assurances', AssuranceViewSet, basename='assurance')
router.register(r'caisses', CaisseViewSet, basename='caisse')
router.register(r'sessions-caisse', SessionCaisseViewSet, basename='session-caisse')
router.register(r'inventaires', InventaireViewSet, basename='inventaire')
router.register(r'fournisseurs', FournisseurViewSet, basename='fournisseur')
router.register(r'commandes', CommandeViewSet, basename='commande')
router.register(r'logs-activite', ActivityLogViewSet, basename='log-activite')
router.register(r'cartes-employes', CarteEmployeViewSet, basename='carte-employe')
router.register(r'statistiques', StatistiquesViewSet, basename='statistiques')

# URLs
urlpatterns = [
    # Authentification par token
    path('auth/token/', obtain_auth_token, name='api-token-auth'),
    
    # Toutes les routes de l'API
    path('', include(router.urls)),
]
