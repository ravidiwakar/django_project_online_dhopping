from email import message
from itertools import product
from pyexpat.errors import messages
from unicodedata import category
from urllib import request
from django.shortcuts import render,redirect
from django.views import View
from app import views
from .models import Cart, Product, OrderPlaced
from django.contrib.auth import authenticate
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Customer, User
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class ProductView(View):
    def get(self, request):
        total_item = 0
        topwear = Product.objects.filter(category='Top wear')
        bottomwear = Product.objects.filter(category='Buttom wear')
        Mobile = Product.objects.filter(category='Mobile')
        Laptop = Product.objects.filter(category='Laptop')
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user = request.user))
        return render(request, 'app/home.html', {'topwear':topwear, 'bottomwear':bottomwear, 'Mobile':Mobile, 'Laptop':Laptop, 'total_item':total_item})

# class ProductDetailView(View):
#     def get(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         return render(request, 'app/productdetail.html', {'product':product})


def product_detail(request, pk):
    total_item = 0
    product = Product.objects.get(pk=pk)
    
    #---------------go to cart---because item already in cart---------------
    item_already_in_cart = False
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user = request.user))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user = request.user)).exists()
    #-----------------------------------
    return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'total_item':total_item})

@login_required
def add_to_cart(request):
    total_item = 0
    user = request.user  
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user = user, product = product).save()
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user = request.user)) 
    return redirect('/show-cart', {'total_item':total_item})

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        # print(cart)
        amount = 0.0
        shipping_ammount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discount_price)
                amount+= temp_amount
                shipping_ammount = shipping_ammount
                total_amount = amount + shipping_ammount
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user = request.user))    
            return render(request, 'app/addtocart.html', {'carts':cart, 'total_amount':total_amount, 'amount':amount, 'shipping_ammount':shipping_ammount, 'total_item':total_item})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()  
        amount = 0.0
        shipping_ammount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
            shipping_ammount = shipping_ammount
            total_amount = amount + shipping_ammount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()  
        amount = 0.0
        shipping_ammount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
            shipping_ammount = shipping_ammount
            total_amount = amount + shipping_ammount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)        


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()  
        amount = 0.0
        shipping_ammount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
            shipping_ammount = shipping_ammount
            total_amount = amount + shipping_ammount

        data = {
            'amount':amount,
            'totalamount':total_amount
        }
        return JsonResponse(data) 

# def remove_cart(request):
#     cart_remove = Cart.objects.filter(id=id)
#     cart_remove.delete()
#     return redirect('/show-cart')

    

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html' , {'add':add, 'active': 'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html', {'order_placed':op})


def mobile(request, data=None):
    if data == None:
        mobile=Product.objects.filter(category='Mobile')
    elif data == 'Gionee' or 'Samsung':
        mobile=Product.objects.filter(category='Mobile').filter(brand=data)
    elif data == 'below':
        mobile=Product.objects.filter(category='Mobile').filter(discount_price__lt=15000)
    elif data == 'above':
        mobile=Product.objects.filter(category='Mobile').filter(discount_price__gt=15000)    
    
                
    return render(request, 'app/mobile.html', {'mobile':mobile})


def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations  !! Registration Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class CustomerProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active': 'btn-primary' })

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['states']
            zipcode = form.cleaned_data['Zipcode']
            req = Customer(user=user,name=name, locality=locality, city=city, states=state, Zipcode=zipcode)
            
            messages.success(request, 'Congratulation !! Profile is successfully Updated')
            req.save()
        return render(request, 'app/profile.html', {'form':form, 'active': 'btn-primary' })        
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_items = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")        
