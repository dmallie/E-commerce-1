from django.urls import reverse
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.contrib.auth.decorators import login_required
########################################################################
from .models import Order, Payment, OrderProduct
from accounts.models import UserProfile, Account


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
# Receive data from PayPal
       ipn = sender
       context = {
              'ipn_status: ', ipn.payment_status,
              'ipn_invoice: ', ipn.invoice,
              'ipn_amount: ', ipn.mc_gross
       }
# first verify the payment status is completed
       if ipn.payment_status == ST_PP_COMPLETED:
# The intantiaate a payment object and insert all the information
              try: 
                     payment = Payment()
              
                     payment.payement_id = ipn.invoice
                     payment.payment_method = 'PayPal'
                     payment.amount_paid = ipn.mc_gross
                     payment.status = ST_PP_COMPLETED
# from payer_email get account object
                     account = Account.objects.get(email__iexact = ipn.payer_email)
                     payment.user = account
                     payment.save()
              except: 
                     print("couldn't perform payment, thus payment is aborted")


              try:
# get UserProfile object which placed the order
                     user_profile = UserProfile.objects.get(user = account)
# Instantiate and save order object
                     order = Order()
                     order.user = account
                     order.user_profile = user_profile
                     order.payment = payment
                     order.status = payment.status 
                     order.tax = round(float(payment.amount_paid) *  0.24, 2)
                     order.order_total = payment.amount_paid
                     order.save()
              except:
                     print("Order object is instantiated. but went wrong in order.user or order.user_profile")
                     