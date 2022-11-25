from django.db import models
from accounts.models import Account, UserProfile 
from carts.models import CartItem

# Create your models here.
class Payment(models.Model):
       user                 = models.ForeignKey(Account, on_delete=models.CASCADE)
       payement_id          = models.CharField(max_length=100)
       payment_method       = models.CharField(max_length=100)
       amount_paid          = models.CharField(max_length=30)
       status               = models.CharField(max_length=50)
       created_at           = models.DateTimeField(auto_now_add=True)

       def __str__(self):
              return self.payement_id

class Order(models.Model):
       STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
       )
       user = models.ForeignKey(Account, on_delete=models.CASCADE)
       user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
       payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
       order_no = models.CharField(max_length=100)
       order_total = models.FloatField()
       tax = models.FloatField()
       status = models.CharField(max_length=100)
       ip = models.CharField(blank = True, max_length=30)
       is_ordered = models.BooleanField(default=False)
       created_at  = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now = True)

       def full_name(self):
              return f'{self.user.first_name} {self.user.last_name}'
              # return self.user.full_name

       def full_address(self):
              return f'{self.user_profile.address_1} {self.user_profile.address_2}'

       def __str__(self):
              return self.order_no

class OrderProduct(models.Model):
       order = models.ForeignKey(Order, on_delete=models.CASCADE)
       payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
       user = models.ForeignKey(Account, on_delete=models.CASCADE)
       products = models.ForeignKey(CartItem, on_delete=models.CASCADE)
       ordered = models.BooleanField(default=False)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now = True)