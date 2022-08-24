from msilib.schema import Class
from django.db import models
from django.conf import settings
from django.urls import reverse

class Produit(models.Model):
    category_choice =(
        ('V','Vetement'),
        ('C','Chaussure'),
        ('L','Lingerie'),
        ('A','Accessoire')
    )
    titre = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(choices=category_choice,max_length=2)
    prix = models.FloatField()
    image = models.ImageField()
    
    def __str__(self):
        return self.titre
    
    def get_add_to_cart_url(self):
        return reverse("ajout_panier", kwargs={
            'id': self.id
        })
    
    def get_supprimer_du_panier(self):
        return reverse("supprimer_du_panier", kwargs={
            'id': self.id
        })    

class ProduitCommande(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantite} de {self.produit.titre}"
    
    def prix_total_produit(self):
        return self.quantite * self.produit.prix
    
    def prix_final(self):
        return self.prix_total_produit()
     
class Commande(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produits = models.ManyToManyField(ProduitCommande)
    start_date =models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    clients = models.ForeignKey('Client',on_delete=models.SET_NULL,blank=True,null=True)
    
    def __str__(self):
        return self.user.username
    
    def valeur_commande(self):
        total = 0
        i = 0
        produits = self.produits.all()
        for produit in produits:
            total = total + produit.prix_final()
        return total
    
class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=50)
    mail = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    Localisation = models.CharField(max_length=200)  
    
    def __str__(self):
        return self.nom 
