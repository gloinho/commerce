from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms
from .models import User
import os


def index(request):
    return render(request, "auctions/index.html", {
        'products': Product.objects.all()
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
            'image': forms.ClearableFileInput(attrs={"class":"custom-file-input", 
                                                     "id":"image",}),
            'category': forms.Select(attrs={"id":"category", "class":"custom-select"}),
            'description': forms.Textarea(attrs={"id":"description", 
                                                 "class":"form-control", 
                                                 "placeholder":"Product Description"}),
        }
        
def new_product(request):
    if request.method == 'POST':
    # FILES will only contain data if the request method was POST and 
    # the <form> that posted to the request had enctype="multipart/form-data". 
    # Otherwise, FILES will be a blank dictionary-like object.
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/new_product.html', {'form': ProductForm})

