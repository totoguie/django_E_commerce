from atexit import register
from django import template
from BuyOnline.models import Commande

register = template.Library()

@register.filter
def element_panier(user):
    if user.is_authenticated:
        qs = Commande.objects.filter(user=user , statut = "non livré")
        if qs.exists():
            return qs[0].produits.count()
    return 0 