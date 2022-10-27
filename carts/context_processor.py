from .models import Cart, CartItem
from .views import _cart_id
def counter(request):
# First Initialise the counter to zero
       counted_items = 0
# create if else statement to block what is in the cart from the admin
       if 'admin' in request.path:
              return {}
       else:
# then create TRY ESCAPE block to raise an exception when there is one
              try:
# get cart object using session key 
                     cart_object = Cart.objects.filter(cart_id = _cart_id(request))
# If user is authenticated then fetch cartitem objects based on user and is_active parameters
                     if request.user.is_authenticated:
                            cart_items = CartItem.objects.all().filter(user = request.user,
                                                                      is_active = True)
# if user is not authenticated then fetch cart_items through cart objects
                     else:
                            cart_items = CartItem.objects.all().filter(cart = cart_object[:1]) # select the first object
# Since we have set of objects in cart_items we can loop it through and examine each objects                     
                     for items in cart_items:
                            counted_items += items.quantity
              except Cart.DoesNotExist:
                     counted_items = 0
       return dict(counted_items = counted_items)

# Return dictionary object with counted items in the cart
