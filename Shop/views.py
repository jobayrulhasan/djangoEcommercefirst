from django.shortcuts import render
from .models import Product
from django.views import View

# Create your views here.
# show product by different catagory
class ProductView(View):
    def get(self, request):
        genspant = Product.objects.filter(category = 'GP')
        borkhas = Product.objects.filter(category = 'BK')
        babyfasion = Product.objects.filter(category = 'BF')
        return render(request, 'Shop/home.html', {'genspant': genspant, 'borkhas': borkhas, 'babyfasion': babyfasion}) 
    
# show product by primary key
class ProductDetailsView(View):
    def get(self, request, pk):
        productDetails = Product.objects.get(pk=pk)
        return render(request, 'Shop/productdetail.html', {'productD': productDetails})
    
    
# show product by filter
def lehenga(request, data = None):
    if data == None:
        lehengas = Product.objects.filter(category = 'L')
    # elif data == 'Pakisthani' or data == 'Indian':
    #     lehengas = Product.objects.filter(category = 'L').filter(brand=data)
        return render(request, 'Shop/lehenga.html', {'lehengaD': lehengas})
    