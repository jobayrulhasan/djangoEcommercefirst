from django.shortcuts import render
from .models import Product
from django.views import View

# Create your views here.
class ProductView(View):
 def get(self, request):
  gentspants = Product.objects.filter(category='GP')
  borkhas = Product.objects.filter(category='BK')
  babyfashions = Product.objects.filter(category='BF')
  return render(request, 'Shop/home.html', {'gentspants':gentspants, 'borkhas':borkhas, 'babyfashions':babyfashions})
 