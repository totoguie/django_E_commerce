from django.forms import ModelForm
from .models import Clients
from django import forms

class ClientForm(ModelForm):
    class Meta:
        model= Clients
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
            'telephone':forms.NumberInput(attrs={
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
        

class RegisterForm(forms.Form):
    username = forms.CharField(label="nom d'utilisation",widget=forms.TextInput(attrs={'class':'form-control mb-2','id':'form3Example3','placeholder':"Nom d'utilisateur"}))
    password = forms.CharField(label="mot de passe",widget=forms.PasswordInput(attrs={'class':'form-control','id':'form3Example4','placeholder':"Mot de passe"}))
    
class LoginForm(forms.Form):
    username = forms.CharField(label="nom d'utilisation",widget=forms.TextInput(attrs={'class':'form-control mb-2','id':'form3Example3','placeholder':"Nom d'utilisateur"}))
    password = forms.CharField(label="mot de passe",widget=forms.PasswordInput(attrs={'class':'form-control','id':'form3Example4','placeholder':"Mot de passe"}))
     