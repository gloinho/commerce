
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms



def index(request):
    """
    Show all active listings
    """
    return render(request, "auctions/index.html", {
        'listings': Product.objects.all()
    })
    
def closed_listings(request):
    """
    Show all closed listings
    """
    return render(request, "auctions/closed_listings.html", {
        'listings': Product.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product', 'first_price', 'image', 'category','description']
        exclude = ('listed_by',)
        widgets = {
            'product': forms.TextInput(attrs={"class":"form-control",
                                              "id":"productname",
                                              "placeholder":"Enter the product's name"}),
            'first_price': forms.NumberInput(attrs={"min":"0", 
                                                    "value":"0", 
                                                    "step":".01", 
                                                    "class":"form-control", 
                                                    "id":"price", 
                                                    "placeholder":"Enter the inicial price"}),
            'image': forms.URLInput(attrs={"class":"form-control", 
                                                     "id":"image",
                                                     'placeholder':'Enter image URL'}),
            'category': forms.Select(attrs={"id":"category", "class":"custom-select"}),
            'description': forms.Textarea(attrs={"id":"description", 
                                                 "class":"form-control", 
                                                 "placeholder":"Product Description"}),
        }
        
def new_product(request):
    """
    Register a new product
    """
    user = request.user
    if request.method == 'POST':
    # FILES will only contain data if the request method was POST and 
    # the <form> that posted to the request had enctype="multipart/form-data". 
    # Otherwise, FILES will be a blank dictionary-like object.
        form = ProductForm(request.POST) 
        if form.is_valid():
            product = form.save(commit=False)
            product.listed_by = user
            form.save()
        else:
            print(form.errors)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/new_product.html', {'form': ProductForm})

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_price']
        labels = {'bid_price':''}
        widgets = {'bid_price': forms.NumberInput(attrs={'min':0, 
                                                         'class': 'form-control',
                                                         'aria-describedby':'bidplaced',})}
        exclude = ('product', 'user')
                       
def on_watchlist(request, id):
    """
    Checks if the user logged has a watchlist and if the product is on his
    watchlist.
    """
    user = request.user
    try:
        watchlist = user.watchlist
        watchlist.product.get(pk=id)
        return True
    except:
        return False
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment':''}
        widgets = {'comment': forms.TextInput(attrs={
                                                "id":"comment",
                                                 "class":"form-control",
                                                 "placeholder":"Comment on this listing." }),}
        
def add_comment(request, id):
    user = request.user
    listing = Product.objects.get(pk=int(id))
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.product = listing
            comment.comment = form.cleaned_data['comment']
            comment.save()
        return HttpResponseRedirect(reverse('listing', args=[id]))
    return HttpResponseRedirect(reverse('listing', args=[id]))      
    
def listing(request, id):
    listing = Product.objects.get(id=int(id))
    how_many_bids = listing.productbid.all().count()
    min_bid = Bid.objects.filter(product = listing.id).last()
    was_user_last_bidder = False
    user = request.user
    try:
        if listing.productbid.all().last().user == user:
            was_user_last_bidder = True
    except:
        was_user_last_bidder = False
        
    try:
        comments = Comment.objects.filter(product=listing)
    except:
        comments = None
        
    if not min_bid:
        min_bid = listing.first_price
    else:
        min_bid = min_bid.bid_price
        
    context = {'bidform': BidForm,
                'listing': listing,
                'onwatchlist': on_watchlist(request, id),
                'commentform': CommentForm,
                'comments':comments,
                'howmanybids':how_many_bids,
                'wasuserlastbidder':was_user_last_bidder}
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.product = listing
            bid.user = user
            bid_price = form.cleaned_data['bid_price']
            if bid_price <= min_bid:
                message = f'Your bid (${bid_price}) is invalid. Needs to be greater than ${min_bid}.'
                context['message'] = message
                return render(request, 'auctions/listing.html', context) 
            else:
                bid.save()
                return HttpResponseRedirect(reverse('listing', args=[id]))
        else:
            return HttpResponse('error')
    return render(request, 'auctions/listing.html', context) 
    
def watchlist(request, id):
    user = request.user
    if not on_watchlist(request, id):
        try:
            watchlist = Watchlist.objects.create(user=user)
        except:
            watchlist = user.watchlist
    watchlist = user.watchlist
    if request.method == 'POST': 
        if 'add_to_watchlist' in request.POST:
            watchlist.product.add((id))
            watchlist.save()
        elif 'remove_from_watchlist' in request.POST:
            watchlist.product.remove(id)
            watchlist.save()
        return HttpResponseRedirect(reverse('listing', args=[id]))
    return HttpResponseRedirect(reverse('listing', args=[id]))
        
def close_listing(request, id):
    listing = Product.objects.get(pk=int(id))
    if request.method == 'POST':
        listing.is_active = False
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=[id]))
    return HttpResponseRedirect(reverse('listing', args=[id]))
        
def user_watchlist(request, user):
    user = request.user
    try:
        watchlist = Watchlist.objects.get(user=user).product.all()
    except:
        watchlist = None
    return render(request, 'auctions/watchlist.html',{'listings':watchlist})
        
def categories(request):
    categories = {}
    for category in Product.CATEGORY_CHOICES:
        category = category[0]
        categories[category] = Product.objects.filter(category=category).count()
    return render(request, 'auctions/categories.html', {'categories': categories})         

def category(request, category):
    listings = Product.objects.filter(category=category)
    return render(request, 'auctions/category.html', {'listings': listings,
                                                      'category': category})


    