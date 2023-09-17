from django.shortcuts import render,redirect

from .models import CustomUser
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import *
from .models import Order
from .models import  Product


User=get_user_model()
# Create your views here.
def signup(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['pass']
        
        if name and email and password:
            if User.objects.filter(email=email).exists():
                return HttpResponseRedirect(reverse('signup') + '?alert=email_already_existing')
            else:

                user = User(name=name,email=email,phone=phone)
                user.set_password(password)
                user.save()
                return HttpResponseRedirect(reverse('signup') + '?alert=registered')
        else:
            return HttpResponseRedirect(reverse('signup') + '?alert=missing_fields')

                
            
                

    return render(request,'signup.html')

# def login(request):
#     error_message = ""
#     if request.method == 'POST': 
#         email = request.POST.get('email')
#         password = request.POST.get('pass')
#         user=auth.authenticate(email=email,password=password)
#         if user is not None:
#             print(user)
#             auth.login(request,user)
#             return redirect('/')
            
#         else:
#             error_message = "Invalid email or password."
#             return render(request, 'login.html', {'error_message': error_message})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use parentheses instead of square brackets
        password = request.POST.get('pass')  # Use parentheses instead of square brackets
        print(email)  # Print the email for debugging
        print(password)  # Print the password for debugging

        if email and password:
            user = authenticate(request, email=email, password=password)
            # print("Authenticated user:", user)  # Print the user for debugging
            if user is not None:
                auth_login(request, user)
                # print("User authenticated:", user.email, user.role)
                return redirect('/')
            else:
                return HttpResponseRedirect(reverse('login') + '?alert=invalid_login')

        else:
            return HttpResponseRedirect(reverse('login') + '?alert=missing_fields')

                
    return render(request, 'login.html')



def about(request):
    return render(request, 'about.html')

def dashboard(request):
    return render(request,'dashboard.html')


def logout(request):
    auth_logout(request)
    return redirect('/')

from django.shortcuts import render
from .models import Product  # Import your Product model


def product(request):
    # Retrieve all products from your database
    products = Product.objects.all()

    # Prepare a dictionary to group products by category
    sorted_products = {}
    for product in products:
        category = product.category
        if category in sorted_products:
            sorted_products[category].append(product)
        else:
            sorted_products[category] = [product]

    return render(request, 'product.html', {'sorted_products': sorted_products})
    



from django.shortcuts import render
from .models import Product

def wheelchair(request):
    # Retrieve products specifically for the wheelchair category
    products = Product.objects.filter(category='Wheelchair')
    return render(request, 'product.html', {'sorted_products': {'Wheelchair': products}})


def walker(request):
    # Retrieve products specifically for the wheelchair category
    products = Product.objects.filter(category='Walker')
    return render(request, 'product.html', {'sorted_products': {'Walker': products}})


def crutches(request):
    # Retrieve products specifically for the wheelchair category
    products = Product.objects.filter(category='Crutches')
    return render(request, 'product.html', {'sorted_products': {'Crutches': products}})



def dashboard(request):
    total_revenue = Order.objects.filter(complete=True).aggregate(total_revenue=models.Sum('product__price'))['total_revenue']
    total_orders = Order.objects.filter(complete=True).count()
    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
    }
    recent_users = User.objects.order_by('-id')[:5]  # Get the 5 most recent users
    context = {
        'recent_users': recent_users
    }
    return render(request, 'dashboard.html', context)
    


# admin
def admin_product(request):
    # Retrieve all products from your database
    products = Product.objects.all()

    # Prepare a dictionary to group products by category
    sorted_products = {}
    for product in products:
        category = product.category
        if category in sorted_products:
            sorted_products[category].append(product)
        else:
            sorted_products[category] = [product]

    return render(request, 'admin_product.html', {'sorted_products': sorted_products})

def recently_added_products(request):
    recently_added_products = Product.objects.order_by('-id')[:10]  # Assuming you want to get the 10 latest products
    categories = set([product.category for product in recently_added_products])
    sorted_products = {category: [product for product in recently_added_products if product.category == category] for category in categories}
    return render(request, 'admin_product.html', {'sorted_products': sorted_products})


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)



from django.shortcuts import render, redirect
from assistiveglobe.forms import ProductForm,ProductUpdateForm

# admin
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_product')  
    else:
        form = ProductForm()
        
    
    return render(request, 'add_product.html', {'form': form})



from django.shortcuts import render
from .models import Product

def delete_product_confirm(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'delete_product.html', {'product': product})


from django.shortcuts import get_object_or_404, redirect
from .models import Product

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_product')  # Redirect to a success page or wherever you want





# admin
def edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_product')
    else:
        form = ProductUpdateForm(instance=product)
    
    return render(request, 'update_product.html', {'form': form, 'admin_product': product})


from django.http import JsonResponse

def updateItem(request):
    return JsonResponse('Product was added', safe=False)



