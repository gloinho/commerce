from django import template
import os

register = template.Library()

@register.filter
def get_image(prod):
    """
    Returns the file name.
    """
    return os.path.basename(prod.image.name)
