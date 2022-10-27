from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import Product, Variation
from carts.models import CartItem
from django.shortcuts import render, redirect
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from decimal import *
from django.core.paginator import Paginator
from django.db.models import Q
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
              products = Product.objects.filter(category=category, is_available=True).order_by('-price')
       else:
# Fetch all the available products
              products = Product.objects.all().order_by('-price')
# Now we have product items we then can limit the no. of items
# to be displayed on a single page and using pagination we can navigate across all products
# step 1 create a pageinator object. Takes two parameters items object and no of items to be displayed 
       paginator  = Paginator(products, 3)
# step 2 create pagenumber object
       page_no = request.GET.get('page')
# step 3 create page object from paginator and page_number
       page_obj = paginator.get_page(page_no)
       no_items = products.count()
# Create a context object for products
       context = {
              'products' : page_obj,
              'counted_items' : no_items
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
              product_detail  = Product.objects.get(category__slug=category_slug, slug=product_slug)
              is_item_in_cart = CartItem.objects.filter(product=product_detail).exists()
       except Exception as e:
              raise e

       context = {
              'product_detail'     : product_detail,
              'is_item_in_cart'    : is_item_in_cart,
              'price_vat'          : round( product_detail.price * Decimal(vat_rate), 2),
       }
       return render(request, 'store/product_detail.html', context)

################################################################################################
################################ SEARCH FUNCTIONALITY ##########################################
# class Search(ListView):
#        model = Product
#        template_name = 'store/store.html'

#        def get_queryset(self):
#               query = self.request.GET.get('keyword')
#               products  = Product.objects.order_by('-price').filter(O(description__icontains=keyword) | O(product_name__icontains=keyword))

#               return products 
def search(request):
# if the name of search input field is 'keyword' then
       if 'keyword' in request.GET:
# bring whatever is writed on the search input
              keyword = request.GET['keyword']
# if the search input is not empty then
              if keyword:
# filter the products based if the description field or the name field contains one word in the search input
                     products = Product.objects.order_by('-price').filter(Q(description__icontains=keyword) | Q(product_name__icontains = keyword))
# count the number of results returned by the query function
              product_count = products.count()
              context = {
                     'products' : products,
                     'prodocut_count': product_count,
              }
       return render(request, 'store/store.html', context)

################################################################################################
################################ ADD VARIATIONS FUNCTION #######################################
@login_required(login_url = 'accounts:login')
def add_variations(request):
# To populate product name dropdown field fetch all the available products
       products = Product.objects.all()
# save product names on the context object
       context = {
              "products" : products,
       }
# Instantiate Variation table object
       variation = Variation()
# Connect to the form object
       if request.method == 'POST':
# connect form fields with variation object
              product_name                       = request.POST.get("product")
              variation.variation_category       = request.POST.get("variation_category")
              variation.variation_value          = request.POST.get("variation")
              is_active                          = request.POST.get("is_active")

              if is_active == 'on':
                     variation.is_active = True
              else:
                     variation.is_active = False
              print("variation.is_active: ", variation.is_active)
# Fetch all product names with the associated id
              all_products = Product.objects.values_list("product_name" , "id")
# Loop through all products 
              for each_product in all_products:
# compare the product names of all_products with product_name
                     if each_product[0] == product_name:
# Then we got the id of the product we looking for
                            product_id = each_product[1]
                            break # no need to loop through the remaining products
# fetch and assign the product we are looking for on the variation object              
              variation.product = Product.objects.get(id=product_id)
# save the variation object 
              variation.save()
# return to home page
              return redirect('home')
       else:
# Reset the variation object to the default
              variation = Variation()
# Render the add_variation.html template
       return render(request, 'store/add_variation.html', context)

