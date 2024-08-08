from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing, name='listing'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:category_name>/', views.category_listings, name='category_listings'),
    path('my_listings/', views.my_listings, name='my_listings'),
    path('closed_listings/', views.closed_listings, name='closed_listings'),
    
]
