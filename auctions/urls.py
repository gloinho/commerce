from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed_listings/", views.closed_listings, name="closed_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_product", views.new_product, name="new_product"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("user_watchlist/<str:user>", views.user_watchlist, name="user_watchlist"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
]
