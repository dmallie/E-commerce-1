from django.urls import path 
from . import views

app_name = 'carts'
urlpatterns = [
       path('', views.cart, name="cart"),
       path('cart_index/<int:product_id>/', views.add_cart, name='add_cart'),
       path('return_cart_item/<int:product_id>/<int:cart_item_id>/', views.subtract_cart, name='subtract_item'),
       path('add_cart_item/<int:product_id>/<int:cart_item_id>/', views.add_item_to_cart, name='add_item'),
       path('delete_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_from_cart, name='delete_cart_item'),
]