from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_product", views.new_product, name="new_product"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
]
