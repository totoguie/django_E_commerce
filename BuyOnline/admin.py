from django.contrib import admin

from .models import Produit,Commande,ProduitCommande,Clients

admin.site.register(Produit)
admin.site.register(Commande)
admin.site.register(ProduitCommande)
admin.site.register(Clients)
