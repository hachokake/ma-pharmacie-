"""
ViewSets pour l'API REST de la pharmacie
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, F
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    Medicament, Categorie, Client, Vente, ItemVente, Fournisseur,
    Commande, LotMedicament, MouvementStock, Prescription, LignePrescription,
    Medecin, Assurance, VenteAssurance, Caisse, SessionCaisse,
    Inventaire, LigneInventaire, ActivityLog, CarteEmploye
)
from .serializers import *
from .services import (
    StockService, VenteService, PrescriptionService, 
    InventaireService, CaisseService, RapportService
)


class MedicamentViewSet(viewsets.ModelViewSet):
    """ViewSet pour les médicaments"""
    queryset = Medicament.objects.all().select_related('categorie', 'created_by')
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'dci', 'code_barre', 'fabricant']
    ordering_fields = ['nom', 'prix_unitaire', 'quantite_stock', 'date_expiration']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MedicamentListSerializer
        return MedicamentSerializer
    
    @action(detail=False, methods=['get'])
    def en_rupture(self, request):
        """Retourne les médicaments en rupture de stock"""
        medicaments = self.queryset.filter(quantite_stock__lte=0)
        serializer = self.get_serializer(medicaments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def alerte_stock(self, request):
        """Retourne les médicaments dont le stock est critique"""
        medicaments = self.queryset.filter(
            quantite_stock__lte=F('seuil_alerte'),
            quantite_stock__gt=0
        )
        serializer = self.get_serializer(medicaments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expires(self, request):
        """Retourne les médicaments expirés"""
        medicaments = self.queryset.filter(date_expiration__lt=timezone.now().date())
        serializer = self.get_serializer(medicaments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def lots(self, request, pk=None):
        """Retourne tous les lots d'un médicament"""
        medicament = self.get_object()
        lots = medicament.lots.filter(actif=True).order_by('date_expiration')
        serializer = LotMedicamentSerializer(lots, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def historique_mouvements(self, request, pk=None):
        """Retourne l'historique des mouvements de stock"""
        medicament = self.get_object()
        mouvements = medicament.mouvements.all().order_by('-date_mouvement')[:50]
        serializer = MouvementStockSerializer(mouvements, many=True)
        return Response(serializer.data)


class CategorieViewSet(viewsets.ModelViewSet):
    """ViewSet pour les catégories"""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['nom']


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet pour les clients"""
    queryset = Client.objects.all().select_related('assurance')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'prenom', 'telephone', 'email']
    ordering_fields = ['nom', 'prenom', 'date_inscription']
    ordering = ['nom', 'prenom']
    
    @action(detail=True, methods=['get'])
    def historique_ventes(self, request, pk=None):
        """Retourne l'historique des ventes d'un client"""
        client = self.get_object()
        ventes = client.ventes.all().order_by('-date_vente')
        serializer = VenteListSerializer(ventes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def impayes(self, request, pk=None):
        """Retourne les ventes impayées d'un client"""
        client = self.get_object()
        ventes = client.ventes.filter(montant_restant__gt=0)
        serializer = VenteListSerializer(ventes, many=True)
        return Response(serializer.data)


class VenteViewSet(viewsets.ModelViewSet):
    """ViewSet pour les ventes"""
    queryset = Vente.objects.all().select_related('client', 'vendeur', 'caisse', 'prescription')
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_facture', 'client__nom', 'client__prenom']
    ordering_fields = ['date_vente', 'montant_total']
    ordering = ['-date_vente']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VenteListSerializer
        elif self.action == 'create':
            return CreerVenteSerializer
        return VenteSerializer
    
    def create(self, request, *args, **kwargs):
        """Crée une nouvelle vente avec ses items"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Préparer les données des items
            items_data = []
            for item in serializer.validated_data['items']:
                medicament = Medicament.objects.get(id=item['medicament_id'])
                items_data.append({
                    'medicament': medicament,
                    'quantite': item['quantite'],
                    'prix': item.get('prix', medicament.prix_unitaire)
                })
            
            # Récupérer les objets liés
            client = None
            if serializer.validated_data.get('client_id'):
                client = Client.objects.get(id=serializer.validated_data['client_id'])
            
            caisse = None
            if serializer.validated_data.get('caisse_id'):
                caisse = Caisse.objects.get(id=serializer.validated_data['caisse_id'])
                session_caisse = caisse.session_active()
            else:
                session_caisse = None
            
            prescription = None
            if serializer.validated_data.get('prescription_id'):
                prescription = Prescription.objects.get(id=serializer.validated_data['prescription_id'])
            
            # Créer la vente via le service
            vente = VenteService.creer_vente(
                items_data=items_data,
                client=client,
                vendeur=request.user,
                methode_paiement=serializer.validated_data['methode_paiement'],
                caisse=caisse,
                session_caisse=session_caisse,
                prescription=prescription,
                remarques=serializer.validated_data.get('remarques', '')
            )
            
            # Appliquer la remise si présente
            if serializer.validated_data.get('remise', 0) > 0:
                vente.remise = serializer.validated_data['remise']
                vente.calculer_total()
            
            # Retourner la vente créée
            output_serializer = VenteSerializer(vente)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annule une vente"""
        vente = self.get_object()
        motif = request.data.get('motif', '')
        
        try:
            VenteService.annuler_vente(vente, request.user, motif)
            return Response({'message': 'Vente annulée avec succès'})
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Retourne les statistiques des ventes"""
        date_debut = request.query_params.get('date_debut')
        date_fin = request.query_params.get('date_fin')
        
        if not date_debut or not date_fin:
            date_fin = timezone.now()
            date_debut = date_fin - timedelta(days=30)
        else:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%d')
            date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
        
        stats = RapportService.rapport_ventes_periode(date_debut, date_fin)
        serializer = StatistiquesVentesSerializer(stats)
        return Response(serializer.data)


class LotMedicamentViewSet(viewsets.ModelViewSet):
    """ViewSet pour les lots de médicaments"""
    queryset = LotMedicament.objects.all().select_related('medicament', 'fournisseur', 'commande')
    serializer_class = LotMedicamentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_lot', 'medicament__nom']
    ordering_fields = ['date_expiration', 'date_reception']
    ordering = ['date_expiration']
    
    @action(detail=False, methods=['get'])
    def expires(self, request):
        """Retourne les lots expirés"""
        lots = StockService.get_lots_expires()
        serializer = self.get_serializer(lots, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def proche_expiration(self, request):
        """Retourne les lots proches de l'expiration"""
        jours = int(request.query_params.get('jours', 90))
        lots = StockService.get_lots_proche_expiration(jours)
        serializer = self.get_serializer(lots, many=True)
        return Response(serializer.data)


class MouvementStockViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les mouvements de stock (lecture seule)"""
    queryset = MouvementStock.objects.all().select_related('medicament', 'lot', 'utilisateur', 'vente')
    serializer_class = MouvementStockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['medicament__nom', 'reference_document']
    ordering = ['-date_mouvement']


class MedecinViewSet(viewsets.ModelViewSet):
    """ViewSet pour les médecins"""
    queryset = Medecin.objects.filter(actif=True)
    serializer_class = MedecinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'prenom', 'numero_ordre']
    ordering = ['nom', 'prenom']


class PrescriptionViewSet(viewsets.ModelViewSet):
    """ViewSet pour les prescriptions"""
    queryset = Prescription.objects.all().select_related('medecin', 'patient', 'receptionniste')
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_ordonnance', 'patient__nom', 'patient__prenom', 'medecin__nom']
    ordering = ['-date_prescription']
    
    @action(detail=False, methods=['get'])
    def en_attente(self, request):
        """Retourne les prescriptions en attente"""
        prescriptions = self.queryset.filter(
            statut__in=['EN_ATTENTE', 'PARTIELLE'],
            date_validite__gte=timezone.now().date()
        )
        serializer = self.get_serializer(prescriptions, many=True)
        return Response(serializer.data)


class AssuranceViewSet(viewsets.ModelViewSet):
    """ViewSet pour les assurances"""
    queryset = Assurance.objects.filter(actif=True)
    serializer_class = AssuranceSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['nom']


class CaisseViewSet(viewsets.ModelViewSet):
    """ViewSet pour les caisses"""
    queryset = Caisse.objects.filter(actif=True)
    serializer_class = CaisseSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def ouvrir_session(self, request, pk=None):
        """Ouvre une session de caisse"""
        caisse = self.get_object()
        fond_ouverture = request.data.get('fond_ouverture', 0)
        
        try:
            session = CaisseService.ouvrir_session(caisse, request.user, fond_ouverture)
            serializer = SessionCaisseSerializer(session)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def fermer_session(self, request, pk=None):
        """Ferme la session active de la caisse"""
        caisse = self.get_object()
        session = caisse.session_active()
        
        if not session:
            return Response(
                {'error': 'Aucune session active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        fond_fermeture = request.data.get('fond_fermeture', 0)
        
        try:
            CaisseService.fermer_session(session, fond_fermeture)
            serializer = SessionCaisseSerializer(session)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SessionCaisseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les sessions de caisse (lecture seule)"""
    queryset = SessionCaisse.objects.all().select_related('caisse', 'caissier', 'validee_par')
    serializer_class = SessionCaisseSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-date_ouverture']


class InventaireViewSet(viewsets.ModelViewSet):
    """ViewSet pour les inventaires"""
    queryset = Inventaire.objects.all().select_related('responsable', 'valideur')
    serializer_class = InventaireSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-date_debut']
    
    @action(detail=False, methods=['post'])
    def creer_inventaire(self, request):
        """Crée un nouvel inventaire"""
        inventaire = InventaireService.creer_inventaire(request.user)
        serializer = self.get_serializer(inventaire)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        """Termine un inventaire"""
        inventaire = self.get_object()
        
        if inventaire.statut != 'EN_COURS':
            return Response(
                {'error': 'Cet inventaire n\'est pas en cours'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        inventaire.statut = 'TERMINE'
        inventaire.date_fin = timezone.now()
        inventaire.calculer_statistiques()
        
        serializer = self.get_serializer(inventaire)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """Valide un inventaire et ajuste les stocks"""
        inventaire = self.get_object()
        
        try:
            InventaireService.valider_inventaire(inventaire, request.user)
            serializer = self.get_serializer(inventaire)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class FournisseurViewSet(viewsets.ModelViewSet):
    """ViewSet pour les fournisseurs"""
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['nom']


class CommandeViewSet(viewsets.ModelViewSet):
    """ViewSet pour les commandes"""
    queryset = Commande.objects.all().select_related('fournisseur')
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-date_commande']


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les logs d'activité (lecture seule)"""
    queryset = ActivityLog.objects.all().select_related('user')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-timestamp']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        action = self.request.query_params.get('action')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if action:
            queryset = queryset.filter(action=action)
        
        return queryset


class CarteEmployeViewSet(viewsets.ModelViewSet):
    """ViewSet pour les cartes d'employés"""
    queryset = CarteEmploye.objects.all().select_related('utilisateur')
    serializer_class = CarteEmployeSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-date_creation_carte']
    
    @action(detail=True, methods=['get'])
    def regenerer_qr(self, request, pk=None):
        """Régénère le QR code d'une carte"""
        carte = self.get_object()
        carte.qr_code.delete()
        carte.generer_qr_code()
        carte.save()
        
        serializer = self.get_serializer(carte)
        return Response(serializer.data)


# ViewSet pour les statistiques globales
class StatistiquesViewSet(viewsets.ViewSet):
    """ViewSet pour les statistiques et rapports"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Retourne les statistiques du dashboard"""
        aujourd_hui = timezone.now().date()
        
        # Statistiques des ventes du jour
        ventes_jour = Vente.objects.filter(
            date_vente__date=aujourd_hui,
            statut='VALIDEE'
        )
        
        stats = {
            'ventes_jour': {
                'nombre': ventes_jour.count(),
                'montant_total': sum(v.montant_total for v in ventes_jour),
            },
            'stock': {
                'medicaments_total': Medicament.objects.filter(actif=True).count(),
                'en_rupture': Medicament.objects.filter(quantite_stock__lte=0, actif=True).count(),
                'alerte': Medicament.objects.filter(
                    quantite_stock__lte=F('seuil_alerte'),
                    quantite_stock__gt=0,
                    actif=True
                ).count(),
                'expires': Medicament.objects.filter(
                    date_expiration__lt=aujourd_hui,
                    actif=True
                ).count(),
            },
            'valeur_stock': StockService.calculer_valeur_stock_total(),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def rotation_stock(self, request):
        """Retourne les statistiques de rotation du stock"""
        stats = RapportService.rapport_medicaments_rotation()
        return Response(stats)
