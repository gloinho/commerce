from django.contrib import admin
from .models import *

# Register your models here.
class BidAdmin(admin.ModelAdmin):
    list_display = ("id","user", "product", "bid_price")
    list_display_links = ("id", "user")
    list_filter = ['product']

    
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","product","first_price","listed_by","is_active","register_date")
    list_display_links = ("id","product")
    list_filter = ('listed_by','is_active')
    
class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ('product',)
    
admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist, WatchlistAdmin)