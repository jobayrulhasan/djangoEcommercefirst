from django.shortcuts import render, redirect
from .models import Product, Customer, Cart, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse


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
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'Shop/profile.html', {'form': form, 'active':'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user_name = request.user
            customer_name = form.cleaned_data['name']
            customer_division = form.cleaned_data['division']
            customer_district = form.cleaned_data['district']
            customer_thana = form.cleaned_data['thana']
            customer_villageorroad = form.cleaned_data['villageorroad']
            customer_zipcode = form.cleaned_data['zipcode']
            all_customer_data = Customer(user = user_name, name = customer_name, division = customer_division, district = customer_district, thana = customer_thana, villageorroad = customer_villageorroad, zipcode = customer_zipcode)
            all_customer_data.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        return render(request, 'Shop/profile.html', {'form':form, 'active':'btn-primary'})
    
# Address
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'Shop/address.html', {'add':add, 'active':'btn-primary'})

# Add to card
def add_to_cart(request):
    userName = request.user
    product_Id = request.GET.get('product_id')
    productTable = Product.objects.get(id = product_Id)
    Cart(user=userName, product = productTable).save()
    return redirect('/cart')

# show in cart
def show_cart(request):
    if request.user.is_authenticated:
        username = request.user
        cart = Cart.objects.filter(user=username)
        amount = 0
        shipping_amount = 0
        cart_product = [p for p in cart]  # no need to filter again

        if cart_product:   # if cart is not empty
            for p in cart_product:
                temp_amount = p.quantity * p.product.discounted_price
                amount += temp_amount
                # condition for shipping
                if amount > 0:
                    shipping_amount = 100
                else:
                    shipping_amount = 0
            total_amount = amount + shipping_amount
            return render(request, 'Shop/addtocart.html', {
                'carts': cart,
                'totalamount': total_amount,
                'amount': amount,
                'shippingamount':shipping_amount
            })
        else:   # if cart is empty
            return render(request, 'Shop/emptycart.html')
  

# plus in cart
def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = product_id) & Q(user = request.user))
        c.quantity += 1
        c.save() # first we have to save the incremented value
        
        amount = 0
        shipping_amount = 100
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            if amount > 0:
                 shipping_amount = 100
            else:
                 shipping_amount = 0
                 
            totalamount = amount + shipping_amount
            
    data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount':totalamount,
    'shippingAmount': shipping_amount
    }
    return JsonResponse(data)

# minus in cart
def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = product_id) & Q(user = request.user))
        c.quantity -= 1
        c.save() # first we have to save the incremented value
        
        amount = 0
        shipping_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            if amount > 0:
                 shipping_amount = 100
            else:
                 shipping_amount = 0
            totalamount = amount + shipping_amount
            
    data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount':totalamount,
    'shippingAmount': shipping_amount
    }
    return JsonResponse(data)


# remove cart value
def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = product_id) & Q(user = request.user))
        c.delete()
        
        amount = 0
        shipping_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            if amount > 0:
                 shipping_amount = 100
            else:
                 shipping_amount = 0
            totalamount = amount + shipping_amount
            
    data = {
    'amount': amount,
    'totalamount':totalamount,
    }
    return JsonResponse(data)


# checkout
def checkout(request):
    request_user = request.user
    add = Customer.objects.filter(user = request_user)
    cart_items = Cart.objects.filter(user = request_user)
    amount = 0
    shipping_amount = 100
    totalamount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request_user]
    if cart_product:
     for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      totalamount = amount + shipping_amount
    return render(request, 'Shop/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


# payment done
def payment_done(request):
    user_name = request.user
    customer_id_from_session = request.GET.get('custid')
    customer = Customer.objects.get(id=customer_id_from_session)
    cart = Cart.objects.filter(user = user_name)
    for c in cart:
        OrderPlaced(user=user_name, customer = customer, product = c.product, quantity = c.quantity).save()
        c.delete()
    return redirect('/orders')

# order
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'Shop/orders.html', {'order_placed':op})