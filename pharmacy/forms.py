from django import forms
from .models import Medicament, Categorie, Client, Vente, ItemVente


class MedicamentForm(forms.ModelForm):
    """Formulaire pour créer et modifier des médicaments"""
    
    class Meta:
        model = Medicament
        fields = [
            'nom', 'description', 'categorie', 'prix_unitaire', 
            'quantite_stock', 'seuil_alerte', 'date_expiration',
            'numero_lot', 'fabricant', 'code_barre'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du médicament'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description détaillée du médicament'
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prix_unitaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'quantite_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'seuil_alerte': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '10'
            }),
            'date_expiration': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'numero_lot': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de lot'
            }),
            'fabricant': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du fabricant'
            }),
            'code_barre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code-barre (optionnel)'
            }),
        }
        labels = {
            'nom': 'Nom du médicament',
            'description': 'Description',
            'categorie': 'Catégorie',
            'prix_unitaire': 'Prix unitaire (FCFA)',
            'quantite_stock': 'Quantité en stock',
            'seuil_alerte': 'Seuil d\'alerte',
            'date_expiration': 'Date d\'expiration',
            'numero_lot': 'Numéro de lot',
            'fabricant': 'Fabricant',
            'code_barre': 'Code-barre',
        }


class CategorieForm(forms.ModelForm):
    """Formulaire pour créer et modifier des catégories"""
    
    class Meta:
        model = Categorie
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la catégorie'
            }),
        }


class ClientForm(forms.ModelForm):
    """Formulaire pour créer et modifier des clients"""
    
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'telephone', 'email', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du client'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom du client'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+243 XXX XXX XXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemple.com'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Adresse du client'
            }),
        }


class VenteForm(forms.ModelForm):
    """Formulaire pour créer une vente"""
    
    class Meta:
        model = Vente
        fields = ['client', 'methode_paiement', 'remarques']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-select'
            }),
            'methode_paiement': forms.Select(attrs={
                'class': 'form-select'
            }),
            'remarques': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Remarques ou notes sur la vente (optionnel)'
            }),
        }
        labels = {
            'client': 'Client (optionnel)',
            'methode_paiement': 'Méthode de paiement',
            'remarques': 'Remarques',
        }


class ItemVenteForm(forms.ModelForm):
    """Formulaire pour ajouter un médicament à une vente"""
    
    class Meta:
        model = ItemVente
        fields = ['medicament', 'quantite']
        widgets = {
            'medicament': forms.Select(attrs={
                'class': 'form-select medicament-select'
            }),
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
        }

