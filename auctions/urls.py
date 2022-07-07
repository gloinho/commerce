from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_product", views.new_product, name="new_product"),
    path("listing/<int:id>", views.listing_details, name="listing"),
]
