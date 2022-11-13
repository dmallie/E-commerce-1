from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
       path('register/', views.register, name = 'register'),
       path('login/', views.login, name='login'),
       path('logout/', views.logout, name='logout'),
       path('my_profile/', views.myProfile, name='profile'),
       path('activate/<uidb64>/<token>/', views.activate, name='activate'),
       path('forgot_password/', views.forgot_password, name='forgot_password'),
       path('validate_reset_link/<uidb64>/<token>/', views.validate_reset_link, name='validate_reset_link'),
       path('reset_password/', views.reset_password, name='reset_password'),
]