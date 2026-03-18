from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Categorie, Medicament, Client, Vente, ItemVente, Fournisseur, Commande, 
    Investissement, LotMedicament, MouvementStock, Medecin, Prescription, 
    LignePrescription, Assurance, VenteAssurance, Caisse, SessionCaisse,
    Inventaire, LigneInventaire, ActivityLog, CarteEmploye
)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    search_fields = ['nom']


@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ['nom', 'dci', 'forme_galenique', 'dosage', 'classification', 'prix_unitaire', 
                   'quantite_stock', 'seuil_alerte', 'categorie', 'actif']
    list_filter = ['classification', 'forme_galenique', 'categorie', 'actif', 'prescription_obligatoire']
    search_fields = ['nom', 'dci', 'code_barre', 'fabricant', 'code_cip']
    list_editable = ['prix_unitaire', 'actif']
    readonly_fields = ['quantite_stock', 'date_ajout', 'date_modification', 'created_by']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'dci', 'description', 'categorie', 'actif')
        }),
        ('Classification pharmaceutique', {
            'fields': ('classification', 'liste_stupefiant', 'prescription_obligatoire')
        }),
        ('Forme et dosage', {
            'fields': ('forme_galenique', 'dosage')
        }),
        ('Prix et marges', {
            'fields': ('prix_achat_ht', 'prix_unitaire', 'tva_taux', 'marge_min', 'marge_max')
        }),
        ('Stock', {
            'fields': ('quantite_stock', 'seuil_alerte')
        }),
        ('Détails produit', {
            'fields': ('date_expiration', 'numero_lot', 'fabricant', 'pays_origine', 
                      'numero_amm', 'code_barre', 'code_cip')
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'date_ajout', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def get_list_display_links(self, request, list_display):
        return ['nom']


@admin.register(LotMedicament)
class LotMedicamentAdmin(admin.ModelAdmin):
    list_display = ['medicament', 'numero_lot', 'quantite', 'date_expiration', 'fournisseur', 
                   'statut_expiration', 'actif']
    list_filter = ['actif', 'date_expiration', 'fournisseur']
    search_fields = ['numero_lot', 'medicament__nom']
    readonly_fields = ['date_reception']
    date_hierarchy = 'date_expiration'
    
    def statut_expiration(self, obj):
        if obj.est_expire():
            return format_html('<span style="color: red;">Expiré</span>')
        jours = obj.jours_avant_expiration()
        if jours <= 30:
            return format_html('<span style="color: orange;">{} jours</span>', jours)
        return format_html('<span style="color: green;">{} jours</span>', jours)
    statut_expiration.short_description = 'Expiration'


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ['date_mouvement', 'type_mouvement', 'medicament', 'lot', 'quantite', 
                   'utilisateur', 'valeur_totale']
    list_filter = ['type_mouvement', 'date_mouvement']
    search_fields = ['medicament__nom', 'reference_document']
    readonly_fields = ['date_mouvement', 'valeur_totale', 'quantite_avant', 'quantite_apres']
    date_hierarchy = 'date_mouvement'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone', 'email', 'assurance', 'credit_autorise', 
                   'actif', 'date_inscription']
    list_filter = ['actif', 'credit_autorise', 'assurance', 'date_inscription']
    search_fields = ['nom', 'prenom', 'telephone', 'email', 'numero_assure']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance', 'telephone', 'email', 'adresse', 
                      'numero_carte_identite')
        }),
        ('Assurance', {
            'fields': ('assurance', 'numero_assure', 'taux_couverture')
        }),
        ('Crédit', {
            'fields': ('credit_autorise', 'plafond_credit')
        }),
        ('Statut', {
            'fields': ('actif', 'notes')
        }),
    )


class ItemVenteInline(admin.TabularInline):
    model = ItemVente
    extra = 1
    fields = ['medicament', 'lot', 'quantite', 'prix_unitaire', 'remise_ligne', 'sous_total']
    readonly_fields = ['sous_total']


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ['numero_facture', 'date_vente', 'client', 'montant_total', 'montant_paye', 
                   'montant_restant', 'type_vente', 'methode_paiement', 'vendeur', 'statut']
    list_filter = ['statut', 'type_vente', 'methode_paiement', 'date_vente']
    search_fields = ['numero_facture', 'client__nom', 'client__prenom']
    date_hierarchy = 'date_vente'
    inlines = [ItemVenteInline]
    readonly_fields = ['numero_facture', 'montant_total', 'montant_restant']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('numero_facture', 'client', 'vendeur', 'caisse', 'session_caisse', 'statut')
        }),
        ('Type et paiement', {
            'fields': ('type_vente', 'methode_paiement', 'prescription')
        }),
        ('Montants', {
            'fields': ('montant_total', 'montant_paye', 'montant_restant', 'remise')
        }),
        ('Détails', {
            'fields': ('date_echeance', 'remarques')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.vendeur:
            obj.vendeur = request.user
        super().save_model(request, obj, form, change)


@admin.register(ItemVente)
class ItemVenteAdmin(admin.ModelAdmin):
    list_display = ['vente', 'medicament', 'lot', 'quantite', 'prix_unitaire', 'sous_total']
    list_filter = ['vente__date_vente']
    search_fields = ['medicament__nom', 'vente__numero_facture']


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'telephone', 'email', 'contact_personne']
    search_fields = ['nom', 'telephone', 'email']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'fournisseur', 'date_commande', 'date_livraison_prevue', 'statut', 'montant_total']
    list_filter = ['statut', 'date_commande']
    search_fields = ['fournisseur__nom']
    date_hierarchy = 'date_commande'


@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'specialite', 'numero_ordre', 'telephone', 'actif']
    list_filter = ['specialite', 'actif']
    search_fields = ['nom', 'prenom', 'numero_ordre']


class LignePrescriptionInline(admin.TabularInline):
    model = LignePrescription
    extra = 1
    fields = ['medicament', 'posologie', 'quantite_prescrite', 'quantite_delivree', 
             'substitution_autorisee']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['numero_ordonnance', 'patient', 'medecin', 'date_prescription', 
                   'date_validite', 'statut']
    list_filter = ['statut', 'date_prescription', 'medecin__specialite']
    search_fields = ['numero_ordonnance', 'patient__nom', 'medecin__nom']
    date_hierarchy = 'date_prescription'
    inlines = [LignePrescriptionInline]
    readonly_fields = ['numero_ordonnance', 'date_reception', 'conserve_jusqu_au']


@admin.register(Assurance)
class AssuranceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'taux_remboursement_defaut', 'plafond_annuel', 
                   'delai_paiement', 'actif']
    list_filter = ['actif']
    search_fields = ['nom', 'code']


@admin.register(VenteAssurance)
class VenteAssuranceAdmin(admin.ModelAdmin):
    list_display = ['numero_dossier', 'vente', 'assurance', 'montant_total', 'montant_assurance', 
                   'montant_patient', 'statut']
    list_filter = ['statut', 'assurance']
    search_fields = ['numero_dossier', 'numero_assure', 'vente__numero_facture']
    readonly_fields = ['numero_dossier']


@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nom', 'localisation', 'actif', 'date_installation']
    list_filter = ['actif']
    search_fields = ['numero', 'nom']


@admin.register(SessionCaisse)
class SessionCaisseAdmin(admin.ModelAdmin):
    list_display = ['caisse', 'caissier', 'date_ouverture', 'date_fermeture', 
                   'montant_total_ventes', 'nombre_transactions', 'ecart_caisse']
    list_filter = ['caisse', 'date_ouverture']
    search_fields = ['caisse__numero', 'caissier__username']
    date_hierarchy = 'date_ouverture'
    readonly_fields = ['nombre_transactions', 'montant_total_ventes', 'total_especes', 
                      'total_cb', 'total_mobile_money', 'total_cheque', 'ecart_caisse']


class LigneInventaireInline(admin.TabularInline):
    model = LigneInventaire
    extra = 0
    fields = ['medicament', 'lot', 'quantite_theorique', 'quantite_reelle', 'ecart', 
             'commentaire', 'ajustement_effectue']
    readonly_fields = ['ecart']


@admin.register(Inventaire)
class InventaireAdmin(admin.ModelAdmin):
    list_display = ['reference', 'date_debut', 'date_fin', 'responsable', 'statut', 
                   'nombre_articles', 'ecart_valeur']
    list_filter = ['statut', 'date_debut']
    search_fields = ['reference', 'responsable__username']
    date_hierarchy = 'date_debut'
    inlines = [LigneInventaireInline]
    readonly_fields = ['reference', 'nombre_articles', 'valeur_theorique', 'valeur_reelle', 
                      'ecart_valeur']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'model_name', 'description', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'description', 'model_name']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp', 'user', 'action', 'model_name', 'object_id', 
                      'description', 'ip_address']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(CarteEmploye)
class CarteEmployeAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'matricule', 'poste', 'date_embauche', 
                   'date_expiration_carte', 'actif']
    list_filter = ['actif', 'poste', 'date_embauche']
    search_fields = ['matricule', 'utilisateur__username', 'utilisateur__first_name', 
                    'utilisateur__last_name']
    readonly_fields = ['qr_code', 'date_creation_carte']


@admin.register(Investissement)
class InvestissementAdmin(admin.ModelAdmin):
    list_display = ['id', 'administrateur', 'utilisateur', 'montant', 'taux_interet', 'duree_jours', 
                    'date_investissement', 'date_echeance', 'statut', 'interets_calcules', 'montant_total_attendu']
    list_filter = ['statut', 'date_investissement', 'date_echeance']
    search_fields = ['administrateur__username', 'utilisateur__username']
    date_hierarchy = 'date_investissement'
    readonly_fields = ['interets_calcules', 'montant_total_attendu', 'date_investissement']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('administrateur', 'utilisateur', 'statut', 'description')
        }),
        ('Détails financiers', {
            'fields': ('montant', 'taux_interet', 'duree_jours')
        }),
        ('Dates', {
            'fields': ('date_investissement', 'date_echeance')
        }),
        ('Calculs automatiques', {
            'fields': ('interets_calcules', 'montant_total_attendu'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.administrateur_id:
            obj.administrateur = request.user
        super().save_model(request, obj, form, change)


# Configuration du site admin
admin.site.site_header = "PharmaCare - Administration"
admin.site.site_title = "PharmaCare Admin"
admin.site.index_title = "Gestion de la Pharmacie"
