from django.urls import path
from . import views

urlpatterns = [
    path("search-products", views.search_products, name="search-products"),
]