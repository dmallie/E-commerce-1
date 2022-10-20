from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import Product
from django.shortcuts import render, redirect
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from decimal import *
# Create your views here.
@login_required(login_url = 'accounts:login')
def create_category(request):
       if request.method == 'POST':

# instantiate the database
              category_db = Category()
# Fetch data from form and insert to database
              category_db.category_name = request.POST.get('category_name')
              category_db.slug          = request.POST.get('slug_name')
              category_db.description   = request.POST.get('description')


              if len(request.FILES) != 0:
                     category_db.cat_image = request.FILES['cat_image']
# Commit the inserted data
              category_db.save()
# Proclaim success for creating and saving new category
              messages.success(request, "category successfully created")
# Return the page to home/index page
              return redirect('home')
       else:
              print("category_form is not valid")
              category_form = CategoryForm()

       return render(request, 'store/add_category.html')

#Adds Product to the Database
@login_required(login_url = 'accounts:login')
def add_product(request):
       category_object = Category.objects.all()
       
       context = {
              "cat_list" : category_object,
       }
       # print("category_object")
       # for cat in category_object:
       #        print( cat)
       if request.method == 'POST':
#Instantiate the database
              product = Product()
              
              
# Connecting database column with html field objects
              product.product_name = request.POST.get("name")
              product.slug         = request.POST.get('slug')
              product.description  = request.POST.get('describe')
              product.price        = request.POST.get('price')
              product.stock        = request.POST.get('quantity')
              cat_type             = request.POST.get('select_category')
              
              category_object_ = Category.objects.values_list('category_name', 'id')
              for cat_objects in category_object_:
                     if cat_objects[0] == cat_type:
                            category_id = cat_objects[1]
                            print("category_id: ", category_id)
                            print("category_name: ", cat_type)
                            break
                                                

              # print("category id: ", category_id)
              #print("index: ", type(category_id))
              # category             = Category.objects.get(id=4)
             
              product.category = Category.objects.get(id=category_id)
              # print(category.filter(category_name=cat_type))
              if len(request.FILES) != 0:
                     product.image = request.FILES['product_picture']
              if int(request.POST.get('quantity')) > 0:
                     product.is_available = True 
              else:
                     product.is_available = False
# Commit data in teh database
              product.save()
# proclaim success for successful saving
              messages.success(request, "Product is successfully added")
# Return to home page
              return redirect('home')
       else:
# Clean the form for another trial
              product = Product()
       return render(request, 'store/add_product.html', context)

def products(request, category_slug=None):
# Reset all product items and category lists to None
       products = None
       category = None
# if category_slug is something
       if category_slug != None:
# get the desired category based on the received slug values
              category = get_object_or_404(Category, slug = category_slug)
# Fetch the available products filtered by their category 
              products = Product.objects.filter(category=category, is_available=True)
       else:
# Fetch all the available products
              products = Product.objects.all()
# Fetch all category types from Category table
       # categories = Category.objects.all()
# Create a context object for products
       context = {
              'products' : products,
              # 'cat_list' : categories,
       }
# Pass this context object to store.html
       return render(request, 'store/store.html', context)

"""
       if request.method == 'POST':
              category = request.POST.get('category_name')
              category_object = Category.objects.values_list('category_name', 'id')
              for cat_objects in category_object:
                     if cat_objects[0] == category:
                            category_id = cat_objects[1]
                            break

              products = Product.objects.filter(category=category_id, is_available=True)
       else:
              print("Post is not working")
"""
# If category slug is provided then
# Fetch all the available products from database
       # products = Product.objects.all().filter(is_available=True).order_by('created_date')
#******** PRODUCT DETAIL *********************
def product_details(request, category_slug, product_slug):
# TRY to find the product based on the provided category_slug and product_slug
       vat_rate = 1.24
       try:
              product_detail = Product.objects.get(category__slug=category_slug, slug=product_slug)
       except Exception as e:
              raise e

       context = {
              'product_detail' : product_detail,
              'price_vat' : round( product_detail.price * Decimal(vat_rate), 2),
       }
       return render(request, 'store/product_detail.html', context)