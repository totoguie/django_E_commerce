from multiprocessing import context
from pipes import Template
from urllib import request
from django.shortcuts import render, redirect
from BuyOnline.models import Produit
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView,DeleteView
from django.views.generic import ListView, DetailView
from BuyOnline.models import Commande, Clients
from BuyOnline.views import commande
from .forms import ProduitForm
from django.contrib import messages

'''def connexion(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request,"ERREUR DE CONNEXION VEUILLEZ VERIFIER VOS INFORMATION")
                return render(request,"admin_app/login.html",{'form':form})
    else:
        form = LoginForm()
        return render(request,"admin_app/login.html",{'form':form})'''
    
    
    

def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required(login_url='connexion')
def admin_dashboard(request):
    commande = Commande.objects.filter(statut = "non livré").order_by("-id")
    produit = Produit.objects.all().count()
    clients = Clients.objects.all().count()
    commandes = Commande.objects.all().count()
    context = {
        'commande':commande,
        'commandes':commandes,
        'clients':clients,
        'produit':produit
        }
    return render(request,"admin_app/dashboard.html",context=context)


def CommandeListe(request):
    commande = Commande.objects.all().order_by("-id")
    produit = Produit.objects.all().count()
    clients = Clients.objects.all().count()
    commandes = Commande.objects.all().count()
    context = {
        'commande':commande,
        'commandes':commandes,
        'clients':clients,
        'produit':produit
        }
    return render(request,"admin_app/liste_commande.html",context=context)
    
def commandeLivre(request):
    commande = Commande.objects.filter(statut = "livré").order_by("-id")
    produit = Produit.objects.all().count()
    clients = Clients.objects.all().count()
    commandes = Commande.objects.all().count()
    context = {
        'commande':commande,
        'commandes':commandes,
        'clients':clients,
        'produit':produit
        }
    return render(request,"admin_app/commandeLivre.html",context=context)

def liste_produit(request):
    produits = Produit.objects.all()
    produit = Produit.objects.all().count()
    clients = Clients.objects.all().count()
    commandes = Commande.objects.all().count()
    context = {
        'produits':produits,
        'commandes':commandes,
        'clients':clients,
        'produit':produit
        }
    return render(request,"admin_app/liste_produit.html",context=context)

def ListeClient(request):
    produits = Produit.objects.all()
    produit = Produit.objects.all().count()
    clients = Clients.objects.all().count()
    client = Clients.objects.all()
    commandes = Commande.objects.all().count()
    context = {
        'produits':produits,
        'commandes':commandes,
        'clients':clients,
        'client':client,
        'produit':produit
        }
    return render(request,"admin_app/listeclient.html",context=context)    
    
class DetailtCommande(DetailView):
    template_name = "admin_app/detail_commande.html"
    model = Commande
    context_object_name = "detailcommande"
    
    def post(self,request, *args, **kwargs):
        if self.request.method == "POST":
            commande_id = self.kwargs['pk']
            commande = Commande.objects.get(id=commande_id)
            nouveau_statut = "livré"
            commande.statut = nouveau_statut
            commande.save()
            return redirect("commandeLivre")
        
    
    
    
class AjouterProduit(LoginRequiredMixin,CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = "admin_app/ajout_produit.html"
    success_url = "/admin_app/ajouterproduit/"
    
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

class Modifier(LoginRequiredMixin,UpdateView):
    model = Produit
    form_class =  ProduitForm
    template_name = "admin_app/modifier.html"
    success_url = "/admin_app/dashboard/"

class Supprimer(LoginRequiredMixin,DeleteView):
    model = Produit
    success_url = "/admin_app/dashboard/"
    

    
    
        
        