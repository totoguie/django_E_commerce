from importlib.resources import path
from django.urls import path
from . import views
from .views import panier, Produit_panier, commande

urlpatterns = [
    path('', views.list_items,name="index"),
    path('inscription/',views.inscription,name="inscription"),
    path('connexion/',views.connexion,name="connexion"),
    path('vetements/',views.Vetements,name="vetements"),
    path('accessoire/',views.Accessoires,name="accessoire"),
    path('contact/',views.contact,name="contact"),
    path('deconnexion/',views.deconnexion,name="lougout"),
    path('produit/<id>/',views.produit,name="produit"),
    path('panier',panier.as_view(),name="panier"),
    path('produit_panier',Produit_panier.as_view(),name="produit_panier"),
    path('commande/',commande.as_view(),name="commande"),
    path('ajout_panier/<id>/', views.ajout_panier, name="ajout_panier"),
    path('supprimer_un_element/<id>/',views.supprimer_un_element,name="supprimer_un_element"),
    path('supprimer_du_panier/<id>/', views.supprimer_du_panier, name="supprimer_du_panier"),

]
