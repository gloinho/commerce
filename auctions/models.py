from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Register a user.
    """
    ...
    

class Product(models.Model):
    """
    Register a product.
    """

    CATEGORY_CHOICES=[
        ("Men's Fashion","Men's Fashion"),
        ('Home and Kitchen','Home and Kitchen'),
        ('Collectible','Collectible'),
        ('Eletronics','Eletronics'),
        ('Office','Office'),
        ('Arts and Crafts','Arts and Crafts'),
        ('Sports and Outdoors','Sports and Outdoors'),
        ('Tools','Tools'),
        ('No Category','No Category'),
    ]
    product = models.CharField(max_length=64)
    first_price = models.DecimalField(max_digits=10, decimal_places=2)
    register_date = models.DateTimeField(auto_now_add=True)
    image = models.URLField()
    category = models.CharField(max_length=19, choices=CATEGORY_CHOICES, default='No Category')
    description = models.CharField(max_length=500, blank=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listedby')
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return f'{self.product}'
    
class Bid(models.Model):
    """
    Register the price of the bid, the product bidded and the user who bids.
    One-to-Many relationship with product and user
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productbid' )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userbid')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self) -> str:
        return f'{self.user} made a R$: {self.bid_price} bid on {self.product}'
    
class Comment(models.Model):
    """
    Register a comment on a auction listing
    """
    comment = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productcomment')
    comment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}'s comment"

class Watchlist(models.Model):
    """
    Add a listing to a user's watchlist.
    """
    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE, related_name='watchlist')
    product = models.ManyToManyField(Product,related_name='watchlisted')
    
    def __str__(self) -> str:
        return f"{self.user.username}'s watchlist."
    # >>> a.watchlist.product.set((1,))
    # >>> a.watchlist.product.all()