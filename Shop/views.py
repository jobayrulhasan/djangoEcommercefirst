from django.shortcuts import render, redirect
from .models import Product
from django.views import View
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

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
    elif data == 'Pakisthani' or data == 'Indian':
        lehengas = Product.objects.filter(category = 'L').filter(brand = data)
    elif data == 'above':
        lehengas = Product.objects.filter(category = 'L').filter(discounted_price__gt = 20000)
    elif data == 'below':
        lehengas = Product.objects.filter(category = 'L').filter(discounted_price__lt = 20000)
    return render(request, 'Shop/lehenga.html', {'lehengaD': lehengas})

# sharees
def sharee(request, data=None):
    message = None  # Default message is None

    if data is None:
        sharees = Product.objects.filter(category='S')
        if not sharees.exists():
            message = "No products found in this category."
    elif data in ['Jamdani', 'Benaroshi', 'Shilkey']:
        sharees = Product.objects.filter(category='S', brand=data)
        if not sharees.exists():
            message = f"No products found for brand '{data}'."
    elif data == 'above':
        sharees = Product.objects.filter(category='S', discounted_price__gt=20000)
        if not sharees.exists():
            message = "No products found above Tk. 20,000."
    elif data == 'below':
        sharees = Product.objects.filter(category='S', discounted_price__lt=20000)
        if not sharees.exists():
            message = "No products found below Tk. 20,000."
    else:
        sharees = None
        message = "Invalid filter option."

    return render(request, 'Shop/sharee.html', {
        'shareeD': sharees,
        'message': message
    })


# class view for user registration
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'Shop/customerregistration.html', {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! registration successfull')
            return render(request, 'Shop/customerregistration.html', {'form': form})


# user login
def user_login(request):
    if request.method == 'POST':
        frm = AuthenticationForm(request=request, data=request.POST)
        if frm.is_valid():
            uName = frm.cleaned_data.get('username')
            uPassword = frm.cleaned_data.get('password')
            user = authenticate(username=uName, password=uPassword)
            if user is not None:
                login(request, user)
                return redirect('profilepage') # profile is the name of url's name
    else:
      frm = AuthenticationForm()
    return render(request, 'Shop/login.html', {'form': frm})

# user logout
def user_logout(request):
    logout(request)
    return redirect('/')


# profile
def profile_view(request):
    return render(request, 'Shop/profile.html')