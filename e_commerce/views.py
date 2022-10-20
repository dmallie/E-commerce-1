from django.shortcuts import render
from store.models import Product
from django.conf import settings
def home(request):
       return render(request, 'home.html')

def index(request):
       products = Product.objects.all().filter(is_available=True).order_by('created_date')
       # print("image path: ", settings.MEDIA_ROOT,"/",products[0].image)
       context = {
              'products' : products[:5],
       }
       return render(request, 'index.html', context)