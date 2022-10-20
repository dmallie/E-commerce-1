from django.contrib import admin
from .models import Product, ProductGallery
#import admin_thumbnails
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
       list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
       prepoluplated_fields = {'slug' : ('product_name',)}
       #inlines = [ProductGalleryInline]

class ProductGalleryInline(admin.TabularInline):
       model = ProductGallery
       extra = 1

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)