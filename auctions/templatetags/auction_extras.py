from django import template
import os
from auctions.models import *

register = template.Library()

@register.filter
def get_image(prod):
    """
    Returns the file name.
    """
    return os.path.join('auctions/images',os.path.basename(prod.image.name))

@register.filter
def get_bid(prod):
    """
    Return the last bid of a product
    """
    return Bid.objects.filter(product = prod.id).last()