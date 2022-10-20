from django.urls import path
from .views import register, login, logout, myProfile

app_name = 'accounts'
urlpatterns = [
       path('register/', register, name = 'register'),
       path('login/', login, name='login'),
       path('logout/', logout, name='logout'),
       path('my_profile/', myProfile, name='profile'),
]