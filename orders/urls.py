from django.urls import path, include
from . import views

app_name = 'orders'
urlpatterns = [
       path('paypal_payment/', include('paypal.standard.ipn.urls'), name='paypal-ipn'),
       path('place_order/', views.place_order, name = 'place_order'),
       path('paypal/', views.process_payment, name='process_payment'),
       path('done/', views.payment_done, name='payment_done'),
       path('cancelled/', views.payment_cancelled, name='payment_cancelled'),
       path('', views.payments, name='payments'),
]