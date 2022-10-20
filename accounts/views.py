from django.shortcuts import render, redirect, get_object_or_404
# import form objects
from .forms import UserProfileForm, UserForm, RegistrationForm
# import tables from models
from .models import UserProfile, Account
# To authenticate user input 
from django.contrib.auth.decorators import login_required
# when a page is requested, Django creates an HttpResponse object that 
# contains metadata about the request Then Django loads the appropriate view, 
# passing the HttpRequest as the first argument to the view function
from django.http import HttpResponse
import requests
# To authenticate the user we need auth class
from django.contrib import messages, auth
# Super class for CreateView
from django.views.generic import CreateView
# To incorporate LoginMixins
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.storage import FileSystemStorage
# Create your views here.
def register(request):

       if request.method == 'POST':
# Arragnges the data using form object       
              form = RegistrationForm(request.POST)  
# we then validate the information written on the form
              if form.is_valid():
                     first_name = form.cleaned_data['first_name']
                     last_name = form.cleaned_data['last_name']
                     email = form.cleaned_data['email']
                     phone_number = form.cleaned_data['phone_number']
                     password = form.cleaned_data['password']
                     username = email.split('@')[0]

# After passing the validation test we then create a user account in the database   
                     user = Account.objects.create_user(first_name, last_name, email, phone_number, password)
# Then save the user object
                     user.save()
                     return redirect('accounts:login')
       else:
              form = RegistrationForm()
       context = {
              'form':form,
       }
       return render(request, 'accounts/register.html', context)

# Login page is managed by this function
def login(request):
       if request.method == 'POST':
# fetch user input eamil and password information
              email = request.POST['email']
              password = request.POST['password']
# authenticate the user using Django auth class
              user = auth.authenticate(email=email, password=password)
              if user is not None:
                     try: 
                            pass
                     except:
                            pass
                     auth.login(request, user)
                     messages.success(request, 'You are now logged in.')
                     url = request.META.get('HTTP_REFERER')
              else:
                     messages.error(request, 'Invalid login credentials')
       return render(request, 'accounts/login.html')
@login_required(login_url='accounts:login')
def logout(request):
       auth.logout(request)
       messages.success(request, 'You are logged out.')
       return redirect('accounts:login')

@login_required(login_url='accounts:login')
def myProfile(request):
       if request.method == 'POST':
# Arragnges the data using form object       
              #form = UserProfileForm(request.POST, request.FILES)
              profile = UserProfile()  
              current_user = request.user
              account = Account.objects.get(id = current_user.id)
              
              profile.user = account
              profile.address_1 = request.POST.get('address_1')
              profile.address_2 = request.POST.get('address_2')
              profile.postal_code = request.POST.get('postal_code')
              profile.city = request.POST.get('city')
              profile.state = request.POST.get('state')
              profile.country = request.POST.get('country')

              if len(request.FILES) != 0:
                     profile.profile_picture = request.FILES['image']
              profile.save()
              messages.success(request, "Profile created successully!!")
              return redirect('accounts:login')
       else:
              form = UserProfileForm()
              context = {
              'form':form,
       }
       return render(request, 'accounts/my_profile.html', context)

              #upload = request.FILES['upload']
              #fss = FileSystemStorage()
              #file = fss.save(upload.name, upload)
              #file_url = fss.url(file)

              #print("form: ", form)
# we then validate the information written on the form
"""
              if form.is_valid():
                     address_1 = form.cleaned_data['address_1']
                     address_2 = form.cleaned_data['address_2']
                     postal_code = form.cleaned_data['postal_code']
                     city = form.cleaned_data['city']
                     state = form.cleaned_data['state']
                     country = form.cleaned_data['country']
                     #print("profile_picture: ", form.profile_picture)
                     #form.save()
                     print("after form.save()")
"""
# After passing the validation test we then create a user account in the database   
                     #profile = UserProfile.objects.create(user=account, address_1=address_1, postal_code=postal_code, city=city, state=state, country=country)
                     #print("current_user.id: ", current_user.email)
# Then save the user object
                     #profile.save()
                     
              
              #else:
               #      print("Form is not valid")

"""       
class MyProfile(CreateView, LoginRequiredMixin):
       model = UserProfile
       fields = ('address_1', 'address_2', 'profile_picture','postal_code', 'city', 'state', 'country')
       template = "accounts/my_profile.html"
       def form_valid(self, form):
              self.object = form.save(commit=False)
              self.object.user = request.user
              self.object.save()
              return super().form_valid(form)
"""