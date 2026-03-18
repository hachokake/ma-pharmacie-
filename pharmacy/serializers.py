"""
Serializers pour l'API REST de la pharmacie
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Medicament, Categorie, Client, Vente, ItemVente, Fournisseur,
    Commande, LotMedicament, MouvementStock, Prescription, LignePrescription,
    Medecin, Assurance, VenteAssurance, Caisse, SessionCaisse,
    Inventaire, LigneInventaire, ActivityLog, CarteEmploye
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id']


class CategorieSerializer(serializers.ModelSerializer):
    """Serializer pour les catégories"""
    class Meta:
        model = Categorie
        fields = '__all__'


class MedicamentSerializer(serializers.ModelSerializer):
    """Serializer pour les médicaments"""
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    est_en_rupture = serializers.BooleanField(read_only=True)
    necessite_alerte = serializers.BooleanField(read_only=True)
    est_expire = serializers.BooleanField(read_only=True)
    marge_actuelle = serializers.SerializerMethodField()
    
    class Meta:
        model = Medicament
        fields = '__all__'
        read_only_fields = ['date_ajout', 'date_modification', 'quantite_stock']
    
    def get_marge_actuelle(self, obj):
        return obj.calculer_marge_actuelle()


class MedicamentListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des médicaments"""
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    
    class Meta:
        model = Medicament
        fields = ['id', 'nom', 'dci', 'forme_galenique', 'dosage', 'prix_unitaire', 
                 'quantite_stock', 'seuil_alerte', 'categorie_nom', 'classification']


class LotMedicamentSerializer(serializers.ModelSerializer):
    """Serializer pour les lots de médicaments"""
    medicament_nom = serializers.CharField(source='medicament.nom', read_only=True)
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    est_expire = serializers.BooleanField(read_only=True)
    jours_avant_expiration = serializers.IntegerField(read_only=True)
    valeur_stock = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = LotMedicament
        fields = '__all__'


class MouvementStockSerializer(serializers.ModelSerializer):
    """Serializer pour les mouvements de stock"""
    medicament_nom = serializers.CharField(source='medicament.nom', read_only=True)
    lot_numero = serializers.CharField(source='lot.numero_lot', read_only=True)
    utilisateur_username = serializers.CharField(source='utilisateur.username', read_only=True)
    type_mouvement_display = serializers.CharField(source='get_type_mouvement_display', read_only=True)
    
    class Meta:
        model = MouvementStock
        fields = '__all__'
        read_only_fields = ['date_mouvement', 'valeur_totale']


class ClientSerializer(serializers.ModelSerializer):
    """Serializer pour les clients"""
    assurance_nom = serializers.CharField(source='assurance.nom', read_only=True)
    a_des_impaye = serializers.BooleanField(read_only=True)
    credit_disponible = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = '__all__'
    
    def get_credit_disponible(self, obj):
        return obj.get_credit_disponible()


class ItemVenteSerializer(serializers.ModelSerializer):
    """Serializer pour les items de vente"""
    medicament_nom = serializers.CharField(source='medicament.nom', read_only=True)
    lot_numero = serializers.CharField(source='lot.numero_lot', read_only=True)
    
    class Meta:
        model = ItemVente
        fields = '__all__'
        read_only_fields = ['sous_total']


class VenteSerializer(serializers.ModelSerializer):
    """Serializer pour les ventes"""
    items = ItemVenteSerializer(many=True, read_only=True)
    client_nom = serializers.SerializerMethodField()
    vendeur_username = serializers.CharField(source='vendeur.username', read_only=True)
    caisse_numero = serializers.CharField(source='caisse.numero', read_only=True)
    est_soldee = serializers.BooleanField(read_only=True)
    type_vente_display = serializers.CharField(source='get_type_vente_display', read_only=True)
    methode_paiement_display = serializers.CharField(source='get_methode_paiement_display', read_only=True)
    
    class Meta:
        model = Vente
        fields = '__all__'
        read_only_fields = ['numero_facture', 'montant_total', 'date_vente']
    
    def get_client_nom(self, obj):
        if obj.client:
            return f"{obj.client.nom} {obj.client.prenom}"
        return None


class VenteListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des ventes"""
    client_nom = serializers.SerializerMethodField()
    vendeur_username = serializers.CharField(source='vendeur.username', read_only=True)
    
    class Meta:
        model = Vente
        fields = ['id', 'numero_facture', 'date_vente', 'client_nom', 'montant_total', 
                 'montant_paye', 'montant_restant', 'methode_paiement', 'vendeur_username', 'statut']
    
    def get_client_nom(self, obj):
        if obj.client:
            return f"{obj.client.nom} {obj.client.prenom}"
        return "Client non spécifié"


class FournisseurSerializer(serializers.ModelSerializer):
    """Serializer pour les fournisseurs"""
    class Meta:
        model = Fournisseur
        fields = '__all__'


class CommandeSerializer(serializers.ModelSerializer):
    """Serializer pour les commandes"""
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Commande
        fields = '__all__'


class MedecinSerializer(serializers.ModelSerializer):
    """Serializer pour les médecins"""
    specialite_display = serializers.CharField(source='get_specialite_display', read_only=True)
    
    class Meta:
        model = Medecin
        fields = '__all__'


class LignePrescriptionSerializer(serializers.ModelSerializer):
    """Serializer pour les lignes de prescription"""
    medicament_nom = serializers.CharField(source='medicament.nom', read_only=True)
    quantite_restante = serializers.IntegerField(read_only=True)
    est_completement_delivree = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = LignePrescription
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    """Serializer pour les prescriptions"""
    lignes = LignePrescriptionSerializer(many=True, read_only=True)
    medecin_nom = serializers.SerializerMethodField()
    patient_nom = serializers.SerializerMethodField()
    receptionniste_username = serializers.CharField(source='receptionniste.username', read_only=True)
    est_valide = serializers.BooleanField(read_only=True)
    peut_etre_delivree = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['numero_ordonnance', 'date_reception']
    
    def get_medecin_nom(self, obj):
        return f"Dr. {obj.medecin.nom} {obj.medecin.prenom}"
    
    def get_patient_nom(self, obj):
        return f"{obj.patient.nom} {obj.patient.prenom}"


class AssuranceSerializer(serializers.ModelSerializer):
    """Serializer pour les assurances"""
    convention_valide = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Assurance
        fields = '__all__'


class VenteAssuranceSerializer(serializers.ModelSerializer):
    """Serializer pour les dossiers assurance"""
    vente_numero = serializers.CharField(source='vente.numero_facture', read_only=True)
    assurance_nom = serializers.CharField(source='assurance.nom', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = VenteAssurance
        fields = '__all__'
        read_only_fields = ['numero_dossier']


class CaisseSerializer(serializers.ModelSerializer):
    """Serializer pour les caisses"""
    session_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Caisse
        fields = '__all__'
    
    def get_session_active(self, obj):
        session = obj.session_active()
        if session:
            return SessionCaisseSerializer(session).data
        return None


class SessionCaisseSerializer(serializers.ModelSerializer):
    """Serializer pour les sessions de caisse"""
    caisse_numero = serializers.CharField(source='caisse.numero', read_only=True)
    caissier_username = serializers.CharField(source='caissier.username', read_only=True)
    validee_par_username = serializers.CharField(source='validee_par.username', read_only=True)
    
    class Meta:
        model = SessionCaisse
        fields = '__all__'
        read_only_fields = ['date_ouverture', 'nombre_transactions', 'montant_total_ventes']


class InventaireSerializer(serializers.ModelSerializer):
    """Serializer pour les inventaires"""
    responsable_username = serializers.CharField(source='responsable.username', read_only=True)
    valideur_username = serializers.CharField(source='valideur.username', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Inventaire
        fields = '__all__'
        read_only_fields = ['reference', 'nombre_articles', 'valeur_theorique', 
                          'valeur_reelle', 'ecart_valeur']


class LigneInventaireSerializer(serializers.ModelSerializer):
    """Serializer pour les lignes d'inventaire"""
    medicament_nom = serializers.CharField(source='medicament.nom', read_only=True)
    lot_numero = serializers.CharField(source='lot.numero_lot', read_only=True)
    compteur_username = serializers.CharField(source='compteur.username', read_only=True)
    
    class Meta:
        model = LigneInventaire
        fields = '__all__'
        read_only_fields = ['ecart', 'valeur_theorique', 'valeur_reelle', 
                          'ecart_valeur', 'date_comptage']


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer pour les logs d'activité"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = '__all__'
        read_only_fields = ['timestamp']


class CarteEmployeSerializer(serializers.ModelSerializer):
    """Serializer pour les cartes d'employés"""
    utilisateur_nom = serializers.SerializerMethodField()
    poste_display = serializers.CharField(source='get_poste_display', read_only=True)
    est_expiree = serializers.BooleanField(read_only=True)
    jours_avant_expiration = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CarteEmploye
        fields = '__all__'
        read_only_fields = ['qr_code', 'date_creation_carte']
    
    def get_utilisateur_nom(self, obj):
        return obj.utilisateur.get_full_name() or obj.utilisateur.username


# Serializers pour la création de ventes avec items
class CreerVenteSerializer(serializers.Serializer):
    """Serializer pour créer une vente avec ses items"""
    client_id = serializers.IntegerField(required=False, allow_null=True)
    methode_paiement = serializers.ChoiceField(choices=Vente.METHODE_PAIEMENT_CHOICES)
    type_vente = serializers.ChoiceField(choices=Vente.TYPE_VENTE_CHOICES, default='COMPTANT')
    caisse_id = serializers.IntegerField(required=False, allow_null=True)
    prescription_id = serializers.IntegerField(required=False, allow_null=True)
    remarques = serializers.CharField(required=False, allow_blank=True)
    remise = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.Field()),
        write_only=True
    )
    
    def validate_items(self, value):
        """Valide les items de la vente"""
        if not value:
            raise serializers.ValidationError("Au moins un item est requis")
        
        for item in value:
            if 'medicament_id' not in item:
                raise serializers.ValidationError("medicament_id est requis pour chaque item")
            if 'quantite' not in item:
                raise serializers.ValidationError("quantite est requise pour chaque item")
            
            try:
                item['quantite'] = int(item['quantite'])
                if item['quantite'] <= 0:
                    raise serializers.ValidationError("La quantité doit être supérieure à 0")
            except ValueError:
                raise serializers.ValidationError("La quantité doit être un nombre entier")
        
        return value


# Serializers pour les statistiques
class StatistiquesVentesSerializer(serializers.Serializer):
    """Serializer pour les statistiques de ventes"""
    periode = serializers.DictField()
    totaux = serializers.DictField()
    par_methode_paiement = serializers.DictField()
    par_vendeur = serializers.ListField()
    nombre_ventes = serializers.IntegerField()


class StatistiquesStockSerializer(serializers.Serializer):
    """Serializer pour les statistiques de stock"""
    valeur_achat = serializers.DecimalField(max_digits=15, decimal_places=2)
    valeur_vente = serializers.DecimalField(max_digits=15, decimal_places=2)
    marge_potentielle = serializers.DecimalField(max_digits=15, decimal_places=2)
    taux_marge = serializers.DecimalField(max_digits=5, decimal_places=2)
