from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  ProduitCommande, Produit, Commande, Clients
from django.views.generic import ListView,DetailView, View
from django.utils import timezone
from .forms import ClientForm, LoginForm, RegisterForm
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404, redirect

def list_items(request): 
    if request.method == "GET":
        produits =Produit.objects.all()
        name = request.GET.get('recherche')
        if name is not None:
            produits = Produit.objects.filter(titre__icontains=name)
            context ={
               'produits':produits
            }
            return render(request, "BuyOnline/index.html",context=context)
     
    liste_produits =Produit.objects.all()
    
    paginator = Paginator(liste_produits, 12)
    
    page = request.GET.get('page')
    
    produits = paginator.get_page(page)
    
    context = {
        'produits':produits
    }
    return render(request, "BuyOnline/index.html",context=context)

def Vetements(request):
    if request.method == "GET":
        vetement =Produit.objects.filter(category="Vetement")
        name = request.GET.get('recherche')
        if name is not None:
            vetement = Produit.objects.filter(titre__icontains=name)
            context ={
               'vetement':vetement
            }
            return render(request, "BuyOnline\index.html",context=context)
     
    liste_vetements =Produit.objects.filter(category="Vetement")
    
    paginator = Paginator(liste_vetements, 12)
    
    page = request.GET.get('page')
    
    vetements = paginator.get_page(page)
    
    context = {
        'vetements':vetements
    }
    return render(request, "BuyOnline\vetements.html",context=context)

def Accessoires(request):
    if request.method == "GET":
        accessoire = Produit.objects.filter(category="Accessoire")
        name = request.GET.get('recherche')
        if name is not None:
            accessoire = Produit.objects.filter(titre__icontains=name)
            context ={
               'accessoire':accessoire
            }
            return render(request, "BuyOnline\index.html",context=context)
     
    liste_accessoires =Produit.objects.filter(category="Accessoire")
    
    paginator = Paginator(liste_accessoires, 12)
    
    page = request.GET.get('page')
    
    accessoires = paginator.get_page(page)
    
    context = {
        'accessoires':accessoires
    }
    return render(request, "BuyOnline\accessoire.html",context=context)
    
    

def produit(request,id):
    produit = Produit.objects.get(id=id)
    context = {
        'produit':produit
    }
    return render(request,"BuyOnline\produit.html",context=context)

def inscription(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            my_group = Group.objects.get(name="client")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username,password=password)
            my_group.user_set.add(user)
            if user is not None:
                return redirect("connexion")
            else:
                messages.error(request,"Inscription echoué veuillez verifier vos information")
                return render(request, "inscription.html",{'form':form})
        else:
            return render(request, "BuyOnline\inscription.html",{'form':form})
    form = RegisterForm()
    return render(request,"BuyOnline\inscription.html",{'form':form})

def is_customer(user):
    return user.groups.filter(name='client').exists()

def is_admin(user):
    return user.groups.filter(name='administrateur').exists()
    

def connexion(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password=password)
            if user is not None:
                if is_customer(user):
                    login(request,user)
                    return redirect('index')
                elif is_admin:
                    login(request,user)
                    return redirect("dashboard")
            else:
                messages.error(request,"ERREUR DE CONNEXION VEUILLEZ VERIFIER VOS INFORMATION")
                return render(request,"BuyOnline\connexion.html",{'form':form})
    else:
        form = LoginForm()
        return render(request,"BuyOnline\connexion.html",{'form':form})
    
def deconnexion(request):
    logout(request)
    return redirect('index')

def contact(request):
    return render(request,"BuyOnline\contact.html")
    

class panier(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try: 
            commande = Commande.objects.get(user=self.request.user, statut = "non livré")
            context = {
                'object':commande
            }
            return render (self.request, 'BuyOnline\panier.html',context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucun produit commande")
            return render (self.request, 'BuyOnline\panier.html')

class Produit_panier(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            commande = Commande.objects.get(user=self.request.user, statut = "non livré")
            context= {
                'commande':commande
            }
            return render(self.request, "BuyOnline\panier.html",context=context)
        except ObjectDoesNotExist:
          messages.error(self.request, "Vous n'avez pas de commande") 
          return redirect("/") 

@login_required(login_url='connexion')
def ajout_panier(request,id):
    produit = get_object_or_404(Produit, id=id)
    produit_commande, created = ProduitCommande.objects.get_or_create(
        produit=produit,
        user = request.user,
        statut = "non livré"
        )
    commande_qs = Commande.objects.filter(user=request.user, statut = "non livré")
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

@login_required(login_url='connexion')
def supprimer_du_panier(request,id):
    produit = get_object_or_404(Produit, id=id)
    commande_qs = Commande.objects.filter(
        user=request.user, 
        statut = "non livré"
        )
    if commande_qs.exists():
        commande = commande_qs[0]
        if commande.produits.filter(produit__id=produit.id).exists():
            produit_commande =ProduitCommande.objects.filter(
                produit = produit,
                user = request.user,
                statut = "non livré"
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

@login_required(login_url='connexion')
def supprimer_un_element(request,id):
    produit = get_object_or_404(Produit, id=id)
    commande_qs = Commande.objects.filter(
        user=request.user, 
        statut = "non livré"
        )
    if commande_qs.exists():
        commande = commande_qs[0]
        if commande.produits.filter(produit__id=produit.id).exists():
            produit_commande =ProduitCommande.objects.filter(
                produit = produit,
                user = request.user,
                statut = "non livré"
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
    
@login_required(login_url='connexion')
def ajouter_un_element(request,id):
    produit = get_object_or_404(Produit, id=id)
    commande_qs = Commande.objects.filter(
        user=request.user, 
        statut = "non livré"
        )
    if commande_qs.exists():
        commande = commande_qs[0]
        if commande.produits.filter(produit__id=produit.id).exists():
            produit_commande =ProduitCommande.objects.filter(
                produit = produit,
                user = request.user,
                statut = "non livré"
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

    '''def get(self, *args, **kwargs):
        try: 
           commande = Commande.objects.get(user=self.request.user, statut = "non livré")
           context = {
               'object':commande
           }
           return render (self.request, 'BuyOnline\panier.html',context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucun produit commande")
            return redirect("")'''

class commande(View):
    def get(self, *args, **kwargs):
        try: 
           commande = Commande.objects.get(user=self.request.user, statut = "non livré")
           forms = ClientForm()
           context = {
               'object':commande,
               'forms':forms
           }
           return render (self.request, 'BuyOnline\commande.html',context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucun produit commande")
            return redirect("panier")
        
    def post(self, *args, **kwargs):
        try: 
            form = ClientForm(self.request.POST )
            commande = Commande.objects.get(user=self.request.user, statut = "non livré")
            if form.is_valid():
                nom = form.cleaned_data.get('nom')
                prenom = form.cleaned_data.get('prenom')
                mail = form.cleaned_data.get('mail')
                telephone = form.cleaned_data.get('telephone')
                localisation = form.cleaned_data.get('Localisation')
                client = Clients(
                    user = self.request.user,
                    nom = nom,
                    prenom = prenom,
                    mail = mail,
                    telephone = telephone,
                    Localisation = localisation
                )
                client.save()
                commande.clients = client
                commande.save()
                return redirect('index')
            messages.warning(self.request,"Commande echoue")
            return redirect("commande")
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucun produit commande")
            return redirect("panier") 