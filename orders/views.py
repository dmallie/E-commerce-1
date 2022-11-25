from django.shortcuts import render, redirect
from .models import Order, Payment, OrderProduct
from accounts.models import UserProfile, Account
from carts.models import CartItem
from store.models import Product, ProductGallery, Variation
from django.contrib.auth.decorators import login_required
from datetime import datetime
########################################################################
from django.contrib import messages
from django.conf import settings 
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
########################################################################
from django.urls import reverse
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
########################################################################
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

# Create your views here.
@login_required(login_url = 'accountss:login')
def payments(request):
# identify the current user
       current_user = request.user
# get information from paypal through html 
       body = json.loads(request.body)
# Instantiate payement object and commit information to the database
       payment                     = Payment()
       payment.user                = current_user
       payment.payment_id          = body['transID']
       payment.payment_method      = body['payment_method']
       payment.amount_paid         = body['amount_paid']
       payment.status              = body['status']
       payment.created_at          = body['created_at']

       payment.save()
# Instantiate Order object and commit information to the database
       order = Order()
# get Account object which instantiate the order
       account = Account.objects.get(email = current_user)
       
# get UserProfile object which instantiate the order
       user_id = Account.objects.filter(email = current_user).values_list("id")[0][0]
       user_profile = UserProfile.objects.get(user = user_id)
# get other Order table columns values
       order.user = account
       order.user_profile = user_profile
       order.payment = payment.id
       order.is_ordered = True 
       order.ip = request.META.get('REMOTE_ADDR')
       order.status = payment.status
       order.tax = payment.amount_paid * 0.24 # VAT is 24%
       order.order_total = payment.amount_paid
       
       order.save()
# generate order number, commit will generate id no for the row using this id value we'll generate order_number
       date_value = datetime.today()
       year = date_value.year.strftime("%y")
       month = date_value.month.strftime("%m")
       day = date_value.day.strftime("%d")

       order_number = year + month + day + str(order.id)
       order.order_no = order_number 
       order.save()
 
# move items from cartItem to order_product
       cartItems = CartItem.objects.filter(user = current_user)

       for an_item in cartItems:
          # create a new orderProduct object
              order_product = OrderProduct()
              order_product.order = order.id
              order_product.payment = payment.id
              order_product.user = account
              order_product.products = an_item.product
              order_product.ordered = order.is_ordered
              order_product.save()  
              # deduct the order quantiry from the no of products in the warehouse
              if an_item.quantity > 1:
                     an_item.quantity = an_item.quantity - 1
              else:
                     an_item.quantity = 0
              an_item.save()
# clear products from cartItem that is to avoide multiple orders
       cartItems.objects.filter(user = current_user).delete()
# send email to the customer that we have received the order
       mail_subject = 'Order has been successfully processed'
       message = render_to_string('orders/order_received.html',{
              'user' : request.user,
              'order' : order,
       })
       to_email = account.email
       send_email = EmailMessage(mail_subject, message,to=[to_email])
       send_email.send()

# send back transaction id & order number back to the customer
       data = {
              'order_number' : order.order_no,
              'transID' : payment.payment_id,
       }

       return jsonResponse(data)

@login_required(login_url = 'accounts:login')
def place_order(request):
# Identify the user
       current_user = request.user
# Instantiate order object
       order = Order()
# get CartItem object which the user instantiate
       cartItem = CartItem.objects.filter(user = current_user)
# calcuate the total amount, tax values and grand_total for the order placed
       total = 0.0
       tax_rate = 0.24
       tax = 0.0
       grand_total = 0.0
       for each_item in cartItem:
              no_items = each_item.quantity
              item = each_item.product.price
              total += no_items * float(item)
       tax = total *  tax_rate
       grand_total = total + tax
# commit order object
       # order.user = account
       # order.user_profile = user_profile
       # order.ip = request.META.get('REMOTE_ADDR')
       # order.status = "Accepted"
       # order.is_ordered = True 
       # order.order_total = grand_total
       # order.tax = tax
       # order.save()
# prepare context dictionary
       context = {
              # 'order' : order,
              'cartItem' : cartItem,
              'total' : total,
              'tax' : tax,
              'grand_total': grand_total,
       }
       # Order.user = current_user
       # profile_id = Order.objects.filter(user = current_user).values_list("user_profile")[0][0]
       # full_name = Order.full_name(request)
       # profile = UserProfile.objects.get(id = profile_id)
       # account = Account.objects.get(email = current_user)
       # print("user_profile: ", profile)
       # 
       
       # full_address = UserProfile.objects.filter(id=profile_id).values_list("address_1")[0][0]
       # print("user name: ", full_name )
       # print("full_address: ", full_address)
       # context = {
       #        'profile': profile,
       #        'account' : account,
       # }
       return render(request, 'orders/place_order.html', context= context)

################################ ################################
# 

@login_required(login_url = 'accounts:login')
@ensure_csrf_cookie
def process_payment(request):
# Identify the current user
       current_user = request.user
       host = request.get_host()
# get ID of the last element in the Order table
       last_element = Payment.objects.all().last()
       if last_element is not None:
              last_id = last_element.id
       else:
              last_id = 0
# generate order number from the current date values and id of the current element in Order table
       date_value = datetime.today()
       year = str(date_value.year)
       month = str(date_value.month)
       day = str(date_value.day)

       rand_int = random.randint(0, 1001)
       order_number = year + month + day + str(rand_int)
       print("order_number: ", order_number)
# calculate the grand_total from objects in the cartItem
       cartItems = CartItem.objects.filter(user = current_user)

       total = 0.0
       tax_rate = 0.24
       tax = 0.0
       grand_total = 0.0
       for each_item in cartItems:
              no_items = each_item.quantity
              item_price = each_item.product.price
              total += no_items * float(item_price)
       tax = total * tax_rate
       tax_ = round(tax, 3)
       grand_total = total + tax 
# generate order name
       order_name = 'Order made on ' + year + '-' + month + '-' + day + 'io'
# create paypal_dict object 
       paypal_dict = {
              'business': settings.PAYPAL_RECEIVER_EMAIL,
              'amount' : grand_total,
              'item_name' : order_name,
              'invoice' : order_number,
              'currency_code' : 'USD',
              'notify_url' : 'http://{}{}'.format(host, reverse('orders:paypal-ipn')),
              'return_url' : 'http://{}{}'.format(host, reverse('orders:payment_done')),
              'cancel_return' : 'http://{}{}'.format(host, reverse('orders:payment_cancelled')),
       }
# Instantiate Paypal form object
       form = PayPalPaymentsForm(initial = paypal_dict)
# Prepare context object
       context = {
              'cart_items' : cartItems,
              'form' : form,
              'grand_total' : grand_total,
              'vat_amount' : tax_,
              'total_price' : total,
       }
       return render(request, 'orders/paypal_form.html', context = context)


#############################################################################################
################################ PAYMENT DONE  & PAYMENT CANCELLED  #########################
@csrf_exempt
def payment_done(request):
# Identify the current user
       current_user = request.user
# fetch the user_profile object of the user 
       current_user_profile = UserProfile.objects.get(user = current_user)
# identify the order object if is_order is False & user == current_user && user_profile == current_user_profile
       current_user_order = Order.objects.filter(is_ordered = False, user = current_user, user_profile = current_user_profile).values()

       for each_order in current_user_order:
              order = Order.objects.get(id = each_order['id'])
# get the current active cart_item for the current user
              current_cart_item = CartItem.objects.filter(user = current_user, is_active = True).values()
# calculate the grand_total and tax values of objects in the cart_item
              total = 0.0
              tax = 0.0
              for each_item in current_cart_item:
                     total += float(Product.objects.get(id = each_item['product_id']).price)
              tax = round(total * 0.24 , 2)
              grand_total = round(total + tax, 2)
# compare the grand_total against the amount we got paid
              if(each_order['order_total'] == grand_total):
# mark is_ordered True
                     order.is_ordered =  True
# fetch the payment object. Order number and payment is are teh same  
                     order.order_no = Payment.objects.filter(id = each_order['payment_id']).values_list('payement_id')[0][0]
                     order.ip = request.META.get('REMOTE_ADDR')
                     order.save()   
# for each purchased items we need to deduct the quantity purchased from we have
              for each_item in current_cart_item:
                     product = Product.objects.get(id= each_item['product_id'])
                     no_stock = product.stock
                     remaining_quantity = no_stock - each_item['quantity']
                     print("remaining_quantity: ", remaining_quantity)
                     if remaining_quantity <= 0:
                            product.stock = 0
                            product.is_available = False
                     else: 
                            product.stock = remaining_quantity
                     product.save()
# test
              cart_items = CartItem.objects.filter(user=current_user)
              for item in cart_items:
# create OrderProduct object and fill it with right data
                     try: 
                            order_product = OrderProduct()
                            order_product.order = order
                            order_product.payment = Payment.objects.get(id = each_order['id'])
                            order_product.user = current_user
                            print("item.product: ", item.product)
                            order_product.products = item
                            if order.is_ordered == True:
                                   order_product.ordered = True 
                            order_product.save()
                            print("order_product: ", order_product)
                     except:
                            print("Couldn't save antying on order_product")
# clear the cart_items
       CartItem.objects.filter(user=current_user).delete()
# Send order received confirmation eamil to the customer
       subject = 'Order confirmation'
       context = {
              'user': current_user,
              'order': order,
       }
       body = render_to_string('orders/order_confirmation.html', context)
       to_email = current_user.email
       email = EmailMessage(subject, body, to = [to_email])
       email.send()

       data = {
              'order_number' : order.order_no,
              # 'payment_id' : payment.payement_id,
       }
       return render(request,  'orders/payment_done.html')
       # return JsonResponse(data)
@csrf_exempt
def payment_cancelled(request):
       return render(request, 'orders/payment_cancelled.html')

#############################################################################################
################################ CHECKOUT  ##################################################
def checkout(request):
       if request.method == 'POST':
              form = CheckoutForm(request.POST)
              if form.is_valid():
                     cleaned_data = form.cleanded_data
#############################################################################################
################################ RECEIVER  ##################################################
