from multiprocessing import context
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import  ProduitCommande, Produit, Commande, Client
from django.views.generic import ListView,DetailView, View
from django.utils import timezone
from .forms import ClientForm

def list_items(request):  
    produits =Produit.objects.all()
    context = {
        'produits':produits
    }
    
    return render(request, "BuyOnline/index.html",context=context)

def produit(request,id):
    produit = Produit.objects.get(id=id)
    context = {
        'produit':produit
    }
    return render(request,"BuyOnline/produit.html",context=context)

class Produit_panier(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            commande = Commande.objects.get(user=self.request.user, ordered=False)
            context= {
                'commande':commande
            }
            return render(self.request, "BuyOnline/panier.html",context=context)
        except ObjectDoesNotExist:
          messages.error(self.request, "Vous n'avez pas de commande") 
          return redirect("/") 

@login_required
def ajout_panier(request,id):
    produit = get_object_or_404(Produit, id=id)
    produit_commande, created = ProduitCommande.objects.get_or_create(
        produit=produit,
        user = request.user,
        ordered = False
        )
    commande_qs = Commande.objects.filter(user=request.user, ordered=False)
    if commande_qs.exists():
        commande = commande_qs[0]
        if commande.produits.filter(produit__id=produit.id).exists():
            produit_commande.quantite += 1
            produit_commande.save()
            messages.info(request, "La quantité de ce produit a été mise à jour") 
        else:
            commande.produits.add(produit_commande)
            messages.info(request, "Ce produit a été ajouter à votre panier")
            return redirect("panier") 
    else:
        commande = Commande.objects.create(user=request.user , ordered_date=timezone.now())
        commande.produits.add(produit_commande)
        messages.info(request, "Ce produit a été ajouter à votre panier")
    return redirect("panier")   

@login_required
def supprimer_du_panier(request,id):
    produit = get_object_or_404(Produit, id=id)
    commande_qs = Commande.objects.filter(
        user=request.user, 
        ordered=False
        )
    if commande_qs.exists():
        commande = commande_qs[0]
        if commande.produits.filter(produit__id=produit.id).exists():
            produit_commande =ProduitCommande.objects.filter(
                produit = produit,
                user = request.user,
                ordered=False
            )[0]
            messages.info(request, "Ce produit a été supprimer de votre panier")
            commande.produits.remove(produit_commande)
            return redirect("panier")
        else:
            messages.info(request, "Ce produit n'existe pas dans votre panier")
            return redirect("panier")    
    else:
        messages.info(request, "Vous n'avez aucune commande")
        return redirect("panier")

@login_required
def supprimer_un_element(request,id):
    produit = get_object_or_404(Produit, id=id)
    commande_qs = Commande.objects.filter(
        user=request.user, 
        ordered=False
        )
    if commande_qs.exists():
        commande = commande_qs[0]
        if commande.produits.filter(produit__id=produit.id).exists():
            produit_commande =ProduitCommande.objects.filter(
                produit = produit,
                user = request.user,
                ordered=False
            )[0]
            if produit_commande.quantite > 1:
                produit_commande.quantite -= 1
                produit_commande.save()
            else:
                commande.produits.remove(produit_commande)
            messages.info(request, "La quantite de ce  produit a été reduite de votre panier")
            return redirect("panier")
        else:
            messages.info(request, "Ce produit n'existe pas dans votre panier")
            return redirect("panier")    
    else:
        messages.info(request, "Vous n'avez aucune commande")
        return redirect("panier")
    
@login_required
def ajouter_un_element(request,id):
    produit = get_object_or_404(Produit, id=id)
    commande_qs = Commande.objects.filter(
        user=request.user, 
        ordered=False
        )
    if commande_qs.exists():
        commande = commande_qs[0]
        if commande.produits.filter(produit__id=produit.id).exists():
            produit_commande =ProduitCommande.objects.filter(
                produit = produit,
                user = request.user,
                ordered=False
            )[0]
            produit_commande.quantite += 1
            produit_commande.save()
            messages.info(request, "La quantite de ce  produit a été reduite de votre panier")
            return redirect("panier")
        else:
            messages.info(request, "Ce produit n'existe pas dans votre panier")
            return redirect("panier")    
    else:
        messages.info(request, "Vous n'avez aucune commande")
        return redirect("panier")    


class panier(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try: 
           commande = Commande.objects.get(user=self.request.user, ordered=False)
           context = {
               'object':commande
           }
           return render (self.request, 'BuyOnline/panier.html',context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucun produit commande")
            return redirect("")

class commande(View):
    def get(self, *args, **kwargs):
        
        forms = ClientForm()
            
        context = {
               
            'forms':forms
        }
        return render (self.request, 'BuyOnline/commande.html',context=context)
      
        
    def post(self, *args, **kwargs):
        form = ClientForm(self.request.POST )
        try: 
           commande = Commande.objects.get(user=self.request.user, ordered=False)
           if form.is_valid():
               nom = form.cleaned_data.get('nom')
               prenom = form.cleaned_data.get('prenom')
               mail = form.cleaned_data.get('mail')
               telephone = form.cleaned_data.get('telephon')
               localisation = form.cleaned_data.get('Localisation')
               client = Client(
                   user = self.request.user,
                   nom = nom,
                   prenom = prenom,
                   mail = mail,
                   telephone = telephone,
                   Localisation = localisation
               )
               client.save()
               commande.client = client
               commande.save()
               return redirect('index')
           messages.warning(self.request,"Commande echoue")
           return redirect("commande")
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucun produit commande")
            return redirect("")
        
        