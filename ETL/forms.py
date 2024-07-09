# ETL/forms.py
from django import forms
from .models import AchatModel, AriclesModel, VenteModel, ClientModel

class Achatforms(forms.ModelForm):
    class Meta:
        model = AchatModel
        fields = ['art_id', 'qte', 'date']

class Articlesforms(forms.ModelForm):
    class Meta:
        model = AriclesModel
        fields = '__all__'

class Venteforms(forms.ModelForm):
    class Meta:
        model = VenteModel
        fields = ['art_id', 'qte', 'date']

class Clientforms(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['nom', 'prenom', 'tel', 'adresse', 'ville', 'local', 'machine']
