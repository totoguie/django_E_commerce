from tkinter import Widget
from django.forms import ModelForm
from django import forms
from BuyOnline.models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['titre','description','category','prix','image']
        labels = {'titer':'titre','description':'description','categorie':'categorie','prix':'prix','image':'image'}
        Widgets={
            'titre':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':5}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'prix':forms.NumberInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }
    

        


class LoginForm(forms.Form):
    username = forms.CharField(label="nom d'utilisation",widget=forms.TextInput(attrs={'class':'form-control','id':'loginName','placeholder':"Nom d'utilisateur"}))
    password = forms.CharField(label="mot de passe",widget=forms.PasswordInput(attrs={'class':'form-control','id':'loginPassword','placeholder':"Mot de passe"}))
    