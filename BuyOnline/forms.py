from django.forms import ModelForm
from .models import Client
from django import forms

class ClientForm(ModelForm):
    class Meta:
        model= Client
        fields=['nom' ,'prenom','mail','telephone','Localisation']
        widgets={
            'nom':forms.TextInput(attrs={
                'placeholder':"Veuillez entrer votre nom",
                'class':'form-control',
                'id':'firstName'
            }),
            'prenom':forms.TextInput(attrs={
                'placeholder':"Veuillez entrer votre prenom",
                'class':'form-control',
                'id':'lastName'
            }),
            'mail':forms.TextInput(attrs={
                'placeholder':"Veuillez entrer votre mail",
                'class':'form-control',
                'id':'email'
            }),
            'telephone':forms.TextInput(attrs={
                'placeholder':"Veuillez entrer votre numero de telephone",
                'class':'form-control',
                'id':'address'
            }),
            'localisation':forms.TextInput(attrs={
                'placeholder':"Veuillez entrer votre mail",
                'class':'form-control',
                'id':'address2'
            }),
        }