from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
       category_name = models.CharField(max_length=50, unique=True)
       slug          = models.SlugField(max_length=50, unique=True)
       description   = models.TextField(blank=True)
       cat_image     = models.ImageField(blank=True, upload_to="userprofile/categories")

       class Meta:
              db_table = 'categories'
              ordering = ['-category_name']
              verbose_name_plural = 'Categories' 
       def get_url(self):
              return reverse('store:products', args=[self.slug])

       def __str__(self):
              return self.category_name