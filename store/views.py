from django.shortcuts import render
from .models import Product
from django.shortcuts import render , get_object_or_404
from django.http import JsonResponse
def home(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


# 🗑️ Remove from cart
from django.shortcuts import redirect, get_object_or_404
from .models import Product, CartItem

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        if cart_item:
            cart_item.delete()
    return redirect('cart')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CartItem

@login_required(login_url='login')  # Redirect to login page if not logged in
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', {'cart_items':cart_items,'total':total})


from django.core.mail import send_mail
def checkout_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.product.price * item.quantity for item in cart_items)

        if request.method == 'POST':
            # process order here...
            full_name = request.POST['full_name']
            email = request.POST['email']
            address = request.POST['address']
            phone = request.POST['phone']
            subject = "Your Order Confirmation - E-appliances"
            message = f"""
            Hi {full_name},

            Thank you for your order on E-appliances!

            Order Details:
            ---------------------
            Name: {full_name}
            Address: {address}
            Phone: {phone}

            We will contact you if needed. Expect delivery in 3-5 business days.

            Regards,  
            E-appliances Team
            """
            from_email = 'deepakalai2004@gmail.com'  # same as in settings.py
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            # You can save the order to database here
            return redirect('order_success')  # or any page you want

        return render(request, 'store/checkout.html', {
            'cart_items': cart_items,
            'total': total
        })
    else:
        return redirect('login')


 # URL name for success page

def order_success(request):
    return render(request, 'store/order_success.html')


def orders_view(request):
    orders = orders_view.objects.filter(user=request.user)
    return render(request, 'store/orders.html', {'orders': orders})


def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('home')
    orders = orders_view.objects.all()
    return render(request, 'store/admin_dashboard.html', {'orders': orders})

def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })
        total += item_total

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

def place_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']

        # Save order to DB here (optional)
        # You can clear the cart now
        request.session['cart'] = {}
        return render(request, 'store/order_success.html', {'name': name})

    return redirect('checkout')

# store/views.py
from django.http import JsonResponse
import json
from .models import *

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
 
        # Get the product
        product = Product.objects.get(id=product_id)
        
        # Get or create cart item
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart

        return redirect('cart')  # redirect to your cart view
