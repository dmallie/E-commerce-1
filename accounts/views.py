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
#
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
                     # user.save()
# Verify the User through email verification method
                     verification_context = {
                            'domain': get_current_site(request),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                     }
                     print("verification_context: ", verification_context)
# prepare the messae
                     message = render_to_string('accounts/account_verification_email.html', verification_context)
# get the subject
                     subject = 'using the link below please activate your account'
# the destination address of the email
                     to_email = email
# prepare the verification email 
                     verification_email = EmailMessage(subject, message, to = [to_email])
# send the verification email
                     verification_email.send()

                     return redirect('/accounts/login/?command=verification&email='+email)
       else:
              form = RegistrationForm()
       context = {
              'form':form,
       }
       return render(request, 'accounts/register.html', context)
# This will activate the user account
def activate(request, uidb64, token):
       try:
              uid = urlsafe_base64_decode(uidb64).decode()
              user = Account._default_manager.get(pk=uid)
       except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
              user = None
       if user is not None and default_token_generator.check_token(user, token):
              user.is_active = True 
              user.save()
              messages.success(request, 'Congratulations! Your accout is activated.')
              return redirect('accounts:login')
       else:
              message.error(request, 'Activation link has expired')
              return redirect('accounts:register')

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
# To display dashboard page
@login_required(login_url='accounts:login')
def dashboard(request):
       pass

def forgot_password(request):
       if request.method == 'POST':
              email = request.POST.get('email')
# check whether the email exists in our database
              if Account.objects.filter(email=email).exists():
# get user object from database                     
                     user = Account.objects.get(email__iexact = email)
                     # user_id = Account.objects.filter(email = user_email).values_list('id')[0][0]
                     # print('user_id: ', user_id)
                     # user = Account.objects.get(pk = user_id)
                     # print("user: ", user)
# prepare information necessary to send password reset email
                     subject = 'Link to reset your password'
                     to_email = email 
                     message_content = {
                            'domain': get_current_site(request),
                            'user' : user,
                            'token' : default_token_generator.make_token(user),
                            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                     }
                     message = render_to_string('accounts/password_resetting.html', message_content) 
                     email_message = EmailMessage(subject, message, to=[to_email])
                     email_message.send()

                     messages.success(request, 'Link to reset the password has been sent to ur email')
                     return redirect('accounts:login')
              else:
                     messages.error(request, 'Email address is not in our database')
                     return redirect('accounts:forgot_password')
       return render(request, 'accounts/forgot_password.html')
##########################################################################################
##### validatet the resetpassword link #####################
def validate_reset_link(request, uidb64, token):
       try:
# decode uidb64 to uid
              uid = urlsafe_base64_decode(uidb64).decode()
              print("uid: ", uid)
# get user object using uid 
              # user = Account._default_manager.get(pk = uid)
              user = Account.objects.get(pk = uid)
              print("user: ", user)
# if the above doesn't work and the following error happends then user is None
       except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
              user = None
# if user is not None and if the token matches that means link is valid and redirect page to reset password page
       print("token boolean value: ", default_token_generator.check_token(user, token))
       if user is not None and default_token_generator.check_token(user, token):
              request.session['uid'] = uid     
              messages.success(request, 'Please reset your password')
              return redirect('accounts:reset_password')
       else:
# The link is invalid prompt an error message abotu the invalidity of the link and go to login page 
              messages.error(request, 'This link has been expired. Please request a new link.')
              return redirect('accounts:login')

############################################################################################
######### Reset Password  ##################################################################
def reset_password(request):
       if request.method == 'POST':
              password_1 = request.POST.get('password_1')
              password_2 = request.POST.get('password_2')

              if password_1 == password_2:
                     uid = request.session.get('uid')
                     user = Account.objects.get(pk = uid)
                     user.set_password(password_1)
                     user.save()
                     messages.success(request, 'You successfully has reset your password')
                     return redirect('accounts:login')
              else:
                     messages.error(request, 'Passwords do not match, Please retype again')
                     return redirect('accounts:reset_password')
       return render(request, 'accounts/reset_password.html')


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