from django.db import models
from category.models import Category 
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
# Create your models here.
class Product(models.Model):
       product_name  = models.CharField(max_length=60, unique=True)
       slug          = models.SlugField(max_length=50, unique=True)
       description   = models.TextField()
       price         = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0.00)
       image         = models.ImageField(upload_to = "photos/products", blank=True)
       stock         = models.IntegerField()
       is_available  = models.BooleanField(default = True)
       category      = models.ForeignKey(Category, on_delete=models.CASCADE)
       created_date  = models.DateField(auto_now_add=True) # updates the value with the time and date of creation of record.
       modified_date = models.DateField(auto_now = True) # updates the value of field to current time and date every time the Model.save() is called.

       def __str__(self):
              return self.product_name
       
       def get_url(self):
              return reverse('store:details', args=[self.category.slug, self.slug])

class ProductGallery(models.Model):
       product       = models.ForeignKey(Product, on_delete = models.CASCADE) 
       image         = models.ImageField(upload_to = 'store/products', blank=True, max_length=255)

       def __str__(self):
              return self.product.product_name 
       
       class Meta:
              verbose_name         = 'productgallery'
              verbose_name_plural  = 'product gallery'

