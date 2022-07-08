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
    min_bid = Bid.objects.filter(product = prod.id).last()
    if not min_bid:
        min_bid = prod.first_price
    else:
        min_bid = min_bid.bid_price
    return min_bid