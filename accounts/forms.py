from django import forms 
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
# Create Password fields and assign attributes for these fields
       password = forms.CharField(widget = forms.PasswordInput(attrs = {
              'class' : 'form-control',
              'placeholder' : 'Enter Password',
       }))
       confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {
              'class':'form-control',
              'placeholder':'Confirm Password',
       }))
# Time to connect with the model and create fields for those data fields
       class Meta:
              model = Account
              fields = ['first_name', 'last_name', 'email', 
                            'phone_number', 'password']
# Using clean() method we clean the input data/information of password field
       def clean(self):
              cleaned_data = super(RegistrationForm, self).clean()
              password = cleaned_data.get('password')
              confirm_password = cleaned_data.get('confirm_password')
# Then we compare the cleaned data of password with confirm_password
              if password != confirm_password:
                     raise forms.ValidationError(
                            "Password doesn't match"
                     )
# What this __init__ function does is
# it initialises the RegistrationForm
# Like password and confirm_password fields assign a placeholder and same class
       def __init__(self, *args, **kwargs):
              super(RegistrationForm, self).__init__(*args, **kwargs)
              self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
              self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
              self.fields['email'].widget.attrs['placehoder'] = 'Email Address'
              self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'

              for field in self.fields:
                     self.fields[field].widget.attrs['class']='form-control'


class UserForm(forms.ModelForm):
       class Meta:
              model = Account
              fields = ['first_name', 'last_name', 'phone_number']
       def __init__(self, *args, **kwargs):
              super(UserForm, self).__init__(*args, **kwargs)
              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'form-control'
# we create image upload field for the profile_picture field
# using meta class we initialise models and data fields to connect with the model
# Initialise the object using __init__function
class UserProfileForm(forms.ModelForm):
      # profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
       class Meta:
              model = UserProfile
              fields = ('address_1', 'address_2', 'profile_picture',
                            'postal_code', 'city', 'state', 'country')
       """
       def clean(self):
              cleaned_data = super(UserProfileForm, self).clean()
              address_1 =  cleaned_data.get('address_1')
              address_2 = cleaned_data.get('address_2')
              postal_code = cleaned_data.get('postal_code')
              city = cleaned_data.get('city')
              state = cleaned_data.get('state')
              #profile_picture = cleaned_data.get('profile_picture')
              country = cleaned_data.get('country')
"""

       def __init__(self, *args, **kwargs):
              super(UserProfileForm, self).__init__(*args, **kwargs)
              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'form-control'







