from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class AccountManager(BaseUserManager):
# To create a user
       def create_user(self, f_name, l_name, email, p_number, password=None):
# validate the fields
              if not email:
                     raise ValueError("Email Field cannot be blank")
# insert data into the table
              user = self.model(
                     email    = self.normalize_email(email), 
                     last_name     = l_name,
                     first_name    = f_name,
                     phone_number  = p_number,
              )
# create a username from eamil field
              user.username = email.split('@')[0]
# set the password 
              user.set_password(password)
# save the values in the database
# Set is_active for the user to True otherwise the user can never log in
              # user.is_active = True
              user.save(using=self._db)

              return user
# To create a superuser
       def create_superuser(self, f_name, l_name, email, p_number, password=None):
# We first create a user              
              user = self.create_user(f_name, l_name, email, p_number, password)
# we then set the Required FIELDS
              user.is_admin        = True 
              user.is_active       = True 
              user.is_staff        = True 
              user.is_superadmin   = True
# We then save on the database
              user.save(using=self._db)
              return user
# Account class set the fields and methods that best describe the model
# Creates the database
class Account(AbstractBaseUser):
# Set Database Fields
       first_name    = models.CharField(max_length = 50)
       last_name     = models.CharField(max_length = 50)
       username      = models.CharField(max_length = 50, unique = True)
       email         = models.EmailField(max_length = 50, unique=True)
       phone_number  = models.CharField(max_length = 50)
# Set Required FIELDS
       date_joined   = models.DateTimeField(auto_now = True)
       last_login    = models.DateTimeField(auto_now = True)
       is_active     = models.BooleanField(default=False)
       is_admin      = models.BooleanField(default=False)
       is_staff      = models.BooleanField(default=False)
       is_superadmin = models.BooleanField(default=False)
# Set Email to be used as a username during login session
       USERNAME_FIELD = 'email'
# FIELDS NOT to be left blank during signup
       REQUIRED_FIELDS = ['first_name', 'last_name', 'username'] 
# To Create a user
       objects = AccountManager()
# user is defined by its email address
       def __str__(self):
              return self.email 
# To get the full name of the user
       def full_name(self):
              return f'{self.first_name} {self.last_name}'

# To know whether a particular user has admin permission or not
# reurns a boolean
       def has_perm(self, perm, obj = None):
              return self.is_admin
#
       def has_module_perms(self, add_label):
              return True 

class UserProfile(models.Model):
       user          = models.OneToOneField(Account, on_delete = models.CASCADE)
       address_1     = models.CharField(max_length=50)
       address_2     = models.CharField(max_length=50, blank=True)
       profile_picture = models.ImageField(blank=True, upload_to='userprofile/')
       postal_code   = models.IntegerField()
       city          = models.CharField(max_length = 50)
       state         = models.CharField(max_length=50)
       country       = models.CharField(max_length=50)

       def __str__(self):
              return self.user.email

       def full_address(self):
              address_ = f'{self.address_1} {self.address_2} {self.postal_code}\n'
              # address__ = f'{self.city} {self.state} {self.country}'
              return address_ 
