from django.urls import path 
from . import views

app_name = 'store'
urlpatterns = [
       path('create_category/', views.create_category, name='create_category'),
       path('add_product/', views.add_product, name='add_product'),
       path('add_variation/', views.add_variations, name='add_variation'),
       path('products/<slug:category_slug>/', views.products, name='products'),
       path('products/', views.products, name='all_products'),
       path('search/', views.search, name='search'),
       path('products/<slug:category_slug>/<slug:product_slug>/', views.product_details, name="details"),
]