from django.urls import path
from .views import *

urlpatterns = [
    #path("connexion",connexion,name="login"),
    path("deconnexion",deconnexion,name="deconnexion"),
    path("dashboard/",admin_dashboard,name="dashboard"),
    path("detailcommande/<int:pk>",DetailtCommande.as_view(),name="detailcommande"),
    path("listecommande",CommandeListe,name="listecommande"),
    path("commandeLivre",commandeLivre,name="commandeLivre"),
    path("listeproduit",liste_produit,name="listeproduit"),
    path("listeclient",ListeClient,name="listeclient"),
    path("ajouterproduit/",AjouterProduit.as_view(),name="ajouterproduit"),
    path("modifier/<int:pk>",Modifier.as_view(),name="modifier"),
    path("supprimer/<int:pk>",Supprimer.as_view(),name="supprimer"), 
]
