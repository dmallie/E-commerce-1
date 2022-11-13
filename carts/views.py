from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from decimal import *
# Create your views here.

# returns the session key
def _cart_id(request):
# Get a session key 
       cart = request.session.session_key 
# If there is no session key then create one 
       if not cart:
              cart = request.session.create()
       return cart 
# adds items to the cart object
def add_cart(request, product_id):
# Get the product 
       # Get Cart object       
              
############### STEP 1 ################################################################
       if request.method == "POST":
              try:
                     cart = Cart.objects.get(cart_id = _cart_id(request))
              except Cart.DoesNotExist:
                     cart = Cart.objects.create(cart_id = _cart_id(request))
       # Save Cart object
              cart.save()
              product_variations = []
# get product object using its product id
              product = Product.objects.get(id=product_id)
# iterate through reques.POST objects
# These objects include, session_key and various fields from the form of html
              for item in request.POST:
# item is a field name of html fields
                     key = item
# value is the value of the field
                     value = request.POST[key]
                     try: 
# we can extract the variation from table by matching the three parameters                            
                            if key == 'color' or key == 'size':
                                   variation = Variation.objects.get(product = product,
                                                               variation_category=key,
                                                               variation_value=value)
                                   print("variation_id: ", variation.id)
                                   product_variations.append(variation)
                     except:
                            pass
              quantity = request.POST.get('quantity_widget')
# Check if this particular cart_item exists object. If true then 
############### STEP 2 ################################################################
              is_cart_item_exists = CartItem.objects.filter(user = request.user,
                                                               product = product).exists()
              print("is_cart_item_exists", is_cart_item_exists)
# if is_cart_item_exists is True that means we have similar product in cart_items so we'll
# check the variations if the variations match then we will only incrment the quantity otherwise 
# we'll treat it as a new cart_item
              if is_cart_item_exists:
# identify and get cart_item using the product object and user object
                     cart_items = CartItem.objects.filter(user=request.user,
                                                        product=product)
                     print("no. similar product items in cart_items: ", cart_items.count())
# This list all the variation properties of cartItems in the cart
                     cart_item_variations = []     # holds the variations of the product
                     variations_id = []              # this holds the id of variations table
############### STEP 3 ################################################################
# instantiate loop which iterate through each fields of cart_item object
                     for item in cart_items:
# select one cart_item and extract all the variations associated with that item
                            variations = item.variations.all()
# in the ex_var_list append all the extracted variations
                            cart_item_variations.append(list(variations))    # existing_variations are query set so need to change to list
# finally on the id list append the cart_item id
                            variations_id.append(item.id)
                     print("cart_item_variations: ", cart_item_variations)
                     print("product_variations: ", product_variations)
############### STEP 4 ################################################################
# Then we need to compare each values of ex_var_lsit with that of variations of the product we have
                     if product_variations in cart_item_variations:
                            print(" product is in the cart")
                            index  = cart_item_variations.index(product_variations)
                            id     = variations_id[index] # variations id
# using the variations id and product we can get the cartItem
                            item   = CartItem.objects.get( id = id,
                                                               product = product) 
# adjust the quantity value by addin the quantity amount fetched from html
                            item.quantity += int(quantity)
# save the item with new quantity value
                            item.save()
                     else:
# create cart item object
                            cart_item = CartItem.objects.create(
                                                        user = request.user,
                                                        product = product,
                                                        quantity = int(quantity),
                                                        cart = cart)
# attach product_variation to this new cart_item
                            cart_item.variations.clear()
                            cart_item.variations.add(*product_variations)
# save cart_item object on db
                            cart_item.save()
# If is_cart_item_exists returns False, That is products in the CartItem collection doesn't match the product
              else:
# create cart_item object
                     cart_item = CartItem.objects.create(product  = product,
                                                               user = request.user,
                                                               quantity = int(quantity),
                                                               cart = cart)
                     if len(product_variations) > 0:
                            cart_item.variations.clear()
                            cart_item.variations.add(*product_variations)
                     cart_item.save()
######################### Just to check cart_item object #########################
                     print("cart_item.user:", cart_item.user)
                     print("cart_item.product: ", cart_item.product)
                     print("cart_item.quantity: ", cart_item.quantity)
                     for v in cart_item.variations.all():
                            print("       variation_category: ", v.variation_category)
                            print("       variation_value: ", v.variation_value)
                     

              return redirect('carts:cart')
              print(" if the user is not authenticated")
# GET variations of the product in color and size
       # Get Cart object       
              try:
                     cart = Cart.objects.get(cart_id = _cart_id(request))
              except Cart.DoesNotExist:
                     cart = Cart.objects.create(cart_id = _cart_id(request))
       # Save Cart object
              cart.save()
       # Fetch Cart Item
              
              try: 
                     cart_item = CartItem.objects.get(product=product, 
                                                        cart=cart, 
                                                        user=request.user,
                                                        quantity=quantity)
                     
                     # cart_item.quantity = 1
              except CartItem.DoesNotExist: # if not found then create one
                     cart_item = CartItem.objects.create(product=product,
                                                        cart = cart,
                                                        quantity = quantity,
                                                        user = request.user)
              # print("variation_id:", id_variation)
              for item_variation in product_variation:
                     cart_item.variations.add(item_variation.id)
              cart_item.save()

              print("cart_item.variations: ", cart_item.variations.through.objects.all())
              context = {
                     'product': product,
                     'quantity': cart_item.quantity,
                     'cart_item': cart_item,
              }
       # 
       return redirect('carts:cart')
       # return render(request, 'store/cart..html', context)

########################################################################
## return or reduce an item form our cart. If no other item of same element
## remained in our cart then delete the cart for the item 
## This function is triggered by the minus button in the carts page
def subtract_cart(request, product_id, cart_item_id):
# GET the product object
       product = get_object_or_404(Product, id=product_id)
       
       try: 
 # authenticate the user
              if request.user.is_authenticated:
                     print(" we are in subtract_cart")
                     cart_item = CartItem.objects.get(id = cart_item_id, 
                                                        user = request.user, 
                                                        product = product)# after the user is authenticated fetch the cart item
                     
# authentication of the user fails          
              else:
                     
# first fetch the cart object
                     cart = Cart.objects.get(cart_id = _cart_id(request))
# then fetch the cart item 
                     cart_item = CartItem.objects.get(product  = product,
                                                        cart   = cart,
                                                        id     = cart_item_id )
                     
# remove an item from the cart if there is no more item left then delete teh item
              if cart_item.quantity > 1:
                     cart_item.quantity -= 1 # reduce the quantity by one item
                     print("cart_item.quantity:", cart_item.quantity)
                     cart_item.save()     # then save the new status 
              else:
                     print("delete cart item")
                     cart_item.delete()   # otherwise delete the item all together

       except:
              
              pass 
       return redirect('carts:cart')
########################################################################
## add an item to our cart.  
## This function is triggered by the plus button in the carts page
def add_item_to_cart(request, product_id, cart_item_id):
# GET the product object
       product = get_object_or_404(Product, id=product_id)
       print("we are in add_item_to_cart")
       try: 
 # authenticate the user
              if request.user.is_authenticated:
# after the user is authenticated fetch the cart item
                     cart_item = CartItem.objects.get(id = cart_item_id, 
                                                        user = request.user, 
                                                        product = product)
                     
# authentication of the user fails          
              else:
                     
# first fetch the cart object
                     cart = Cart.objects.get(cart_id = _cart_id(request))
# then fetch the cart item 
                     cart_item = CartItem.objects.get(product  = product,
                                                        cart   = cart,
                                                        id     = cart_item_id )
# THEN INCREASE THE QUANTITY BY 1
              cart_item.quantity += 1 
# Then save the new cart item values              
              cart_item.save()
       except:
              
              pass 
       return redirect('carts:cart')

########################################################################
## Remvoe the cart item from our cart.  
## This function is triggered by the Remove button in the carts page
def remove_from_cart(request, product_id, cart_item_id):
# GET the product object
       product = get_object_or_404(Product, id=product_id)
       try: 
 # authenticate the user
              if request.user.is_authenticated:
# after the user is authenticated fetch the cart item
                     cart_item = CartItem.objects.get(id = cart_item_id, 
                                                        user = request.user, 
                                                        product = product)
                     
# IF authentication of the user fails          
              else:                
# first fetch the cart object
                     cart = Cart.objects.get(cart_id = _cart_id(request))
# then fetch the cart item 
                     cart_item = CartItem.objects.get(product  = product,
                                                        cart   = cart,
                                                        id     = cart_item_id )
# THEN DELETE THE CART ITEM 
              cart_item.delete() 
       except:
              
              pass 
       return redirect('carts:cart')


# cart method render the cart page
def cart(request, total=0, quantity=0, cart_items=None):
# Try to get cart objects and calculate the total bill
       try:
              vat = 0.24
              price = 0
              if request.user.is_authenticated:
                     cart_items = CartItem.objects.filter(user = request.user,
                                                               is_active = True)
              else:
                     cart = Cart.objects.get(cart_id = _cart_id(request)) # request the id of the current cart
                     cart_items = CartItem.objects.filter(cart=cart, is_active=True)
              for an_item in cart_items:
                     price += (an_item.product.price * an_item.quantity)
                     quantity += an_item.quantity
              vat_amount = round( price * Decimal(vat), 2)
              grand_total = price + vat_amount  
       except ObjectDoesNotExist:
              pass 
       # cartitem_variations = []
       # for i in cart_items:
       #        cartitem_variations.append(i.variations.through.objects.values_list('cartitem_id','variation_id'))
       #        break# print("i: ", i.variations.through.objects.values_list('cartitem_id','variation_id'))
       # print(cart_items)
       context = {
              'total_price': price,
              'total_price_vat': grand_total,
              'vat_amount': vat_amount,
              'cart_items': cart_items,
       }
       if len(cart_items) == 0:
              return redirect('store:all_products')
       else:
              return render(request,'carts/carts.html', context)

########################################################
## TOTAL PRICE #############################
# This function calculates the total price of the cart 
def calc_price(request):
       price = 0.00
# Try to fetch all the active items in the cart
       try: 
# First authenticate the user then fetch all the items based on active items which belongs to the user
              if request.user.is_authenticated:
                     cart_items = request.objects.filter(is_active=True,
                                                        user = request.user)
              else:
# request the id of the cart
                     id_cart = Cart.objects.get(cart_id = _cart_id(request))
# From the cart_id then fetch the cart_items
                     cart_items = CartItem.objects.filter(cart = id_cart,
                                                               is_active=True)
# Now we calculate the total price of the cart
              for item in cart_items:
                     price += ( item.price * item.quantity)
       except ObjectDoesNotExist:
              pass

              