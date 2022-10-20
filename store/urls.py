from django.urls import path 
from . import views

app_name = 'store'
urlpatterns = [
       path('create_category/', views.create_category, name='create_category'),
       path('add_product/', views.add_product, name='add_product'),
       path('products/<slug:category_slug>/', views.products, name='products'),
       path('products/', views.products, name='all_products'),
       path('products/<slug:category_slug>/<slug:product_slug>/', views.product_details, name="details"),
]