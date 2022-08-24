from django.contrib import admin

from .models import Produit, ProduitCommande,Commande,Client

admin.site.register(Produit)
admin.site.register(Commande)
admin.site.register(ProduitCommande)
admin.site.register(Client)
