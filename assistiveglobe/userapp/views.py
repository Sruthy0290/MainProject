from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .models import Order
from .models import  Product
from django.shortcuts import render
from assistiveglobe.forms import ProductForm,ProductUpdateForm
from django.shortcuts import get_object_or_404, redirect





User=get_user_model()
# Create your views here.

            
def signup(request):
    if request.user.is_authenticated:
        if request.user.role == CustomUser.CLIENT:
            return redirect('http://127.0.0.1:8000/')
        # elif request.user.role == CustomUser.THERAPIST:
        #     return redirect(reverse('therapist'))
        elif request.user.role == CustomUser.ADMIN:
            return redirect(reverse('dashboard'))
        else:
            return redirect('http://127.0.0.1:8000/')
    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        if request.user.role == CustomUser.CLIENT:
            return redirect('http://127.0.0.1:8000/')
        # elif request.user.role == CustomUser.THERAPIST:
        #     return redirect(reverse('therapist'))
        elif request.user.role == CustomUser.ADMIN:
            return redirect(reverse('dashboard'))
        else:
            return redirect('http://127.0.0.1:8000/')
    elif request.method == 'POST':
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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def about(request):
    return render(request, 'about.html')

def dashboard(request):
    return render(request,'dashboard.html')

def logout(request):
    auth_logout(request)
    return redirect('/')


def product(request):
    if request.user.is_authenticated:
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

    else:
        return redirect('home')

    

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

# def wishlist(request):
#     # Logic to retrieve user's wishlist items goes here
#     wishlist_items = []  # Placeholder for wishlist items
    
#     context = {
#         'wishlist_items': wishlist_items,
#     }
    
#     return render(request, 'wishlist.html', context)

# views.py

# from django.http import JsonResponse
# from django.views import View
# from .models import WishlistItem

# class WishlistView(View):
#     def post(self, request):
#         product_id = request.POST.get('product_id')
#         action = request.POST.get('action')

#         # Add or remove item from wishlist based on action
#         if action == 'add':
#             WishlistItem.objects.create(user=request.user, product_id=product_id)
#         elif action == 'remove':
#             WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()

#         return JsonResponse({'message': 'Item updated successfully'})


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
    
    
def user_detail(request):
    # Assuming you want to fetch all users for this view
    users = CustomUser.objects.all()

    context = {
        'users': users
    }

    return render(request, 'user_detail.html', context)



def block_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        if user.is_active== True:
           user.is_active= False
        elif user.is_active== False:
           user.is_active= True 
    
        user.is_blocked = not user.is_blocked
        user.save()
    return redirect('user_detail')  # Assuming you have a URL named 'user_details'

def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and not user.is_blocked:  # Check if user is not blocked
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard
        else:
            # Handle case where user is blocked
            return render(request, 'login.html', {'error_message': 'Your account is blocked.'})

    return render(request, 'login.html')


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




def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_detail.html', {'product': product})



# def product_management(request):
#     products = Product.objects.all()  # Query all products
#     context = {
#         'products': products
#     }
#     return render(request, 'dashboard.html', context)


@login_required
def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))  # Get the selected quantity or default to 1
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart_item = CartItem.objects.filter(product_id=product_id, user_id=user.id).first()
 
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cartItem = CartItem(
            product_id=product_id,
            user_id=user.id,
            quantity=quantity
        )
        cartItem.save()

    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    context = {
        'cart_items':cart_items,
        'total_items':total_items,
        'total_price':total_price,
    }
    return render(request,'cart.html',context)





from django.shortcuts import get_object_or_404, redirect

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(CartItem, id=cart_id)
    cart_item.delete()
    return redirect('cart')


from django.http import JsonResponse

def update_cart_quantity(request, cart_id):
    cart_item = get_object_or_404(CartItem, id=cart_id)
    new_quantity = request.POST.get('quantity')
    cart_item.quantity = new_quantity
    cart_item.save()

    # Calculate the new total for this item
    new_total = cart_item.product.price * float(cart_item.quantity)

    # Get all cart items for the user
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate the new subtotal
    new_subtotal = sum(item.product.price * item.quantity for item in cart_items)
    return JsonResponse({'success': True, 'new_total': new_total, 'new_subtotal': new_subtotal})



from .models import CustomUser
from django.shortcuts import render, redirect
from .models import ShippingAddress


def checkout_view(request):
    name = ""
    phone = ""
    district = ""

    if request.method == 'POST':
        # Assuming you have a form for the new address
        form = checkout(request.POST)

        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()

            # Update saved_address and related fields
            name = new_address.name
            phone = new_address.phone
            district = new_address.district
    else:
        form = checkout()

    context = {
        'name': name,
        'phone': phone,
        'district': district,
        'form': form,
    }

    return render(request, 'checkout.html', context)

def checkout(request, amt):
    saved_address = None
    name = ""
    phone = ""
    district = ""

    if request.user.is_authenticated:
        try:
            saved_address = ShippingAddress.objects.get(user=request.user)
            name = saved_address.name
            phone = saved_address.phone
            district = saved_address.district
            
        except ShippingAddress.DoesNotExist:
            saved_address = None

    # Get the cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)

    context = {
        'saved_address': saved_address,
        'name': name,
        'phone': phone,
        'district': district,
        'amt': amt,
        'cart_items': cart_items,  # Add cart items to context
        'sorted_products': sorted_products  # Add sorted products to context
    }

    return render(request, 'checkout.html', context)




def edit_address(request):
    saved_address = ShippingAddress.objects.filter(user=request.user).first()
    form = edit_address(instance=saved_address)
    
    if request.method == 'POST':
        form = edit_address(request.POST, instance=saved_address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')
    
    context = {
        'form': form,
    }
    return render(request, 'edit_address.html', context)

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




def delete_product_confirm(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'delete_product.html', {'product': product})



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
    
    return render(request, 'edit_product.html', {'form': form, 'admin_product': product})



from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

def payment(request,amt):
    currency = 'INR'
    amount = amt*100 # Rs. 200

    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'+str(amount)

    order=Order.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,

    )


    amount=amount/100
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['user']=request.user
    

    return render(request, 'payment.html', context=context)

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.

@csrf_exempt
def paymenthandler(request, amount):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        if result is not None:
            # If the payment signature is verified
            amount = amount

            # Capture the payment
            razorpay_client.payment.capture(payment_id, amount)

            # Find the order related to this payment
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)

            # Update the order with the payment_id
            order.transaction_id = payment_id
            order.complete = True
            order.save()

            return redirect('order_history')
        else:
            return render(request, 'paymentfail.html')

    else:
        return HttpResponseBadRequest()





from django.contrib import messages

def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        if created:
            # Wishlist item was added successfully
            # You can add a success message here if needed
            messages.success(request, "Item added to wishlist successfully.")
        else:
            # Wishlist item already exists for this user and product
            # You can add an error message here if needed
            messages.error(request, "Item is already in your wishlist.")
    else:
        # User is not authenticated, handle this case as needed
        # For example, you might want to redirect them to a login page
        messages.warning(request, "Please log in to add items to your wishlist.")
        return redirect('login')  # Assuming you have a 'login' URL name

    return redirect('product_detail', product_id=product_id)  # Redirect to the product detail page


def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
    else:
        wishlist_items = []

    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


from django.http import JsonResponse
from .models import WishlistItem

def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        try:
            wishlist_item = WishlistItem.objects.get(user=request.user, product_id=product_id)
            wishlist_item.delete()
            return JsonResponse({'success': True})
        except WishlistItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found in wishlist'})
    else:
        return JsonResponse({'success': False, 'error': 'User not authenticated'})
    
    
def my_profile(request):
    user = request.user
    return render(request, 'my_profile.html', {'user': user})


def product_search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query)
        if results.count() == 1:
            # If there is only one result, redirect to its detail page
            product = results.first()
            return redirect('product_detail', product_id=product.id)
        
    # else:
    #     results = Product.objects.all()
    
    context = {
        'results': results,
        'query': query
    }
    
    return render(request, 'product_search.html', context)


def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, complete=True)  # Filter completed orders
        print("hello")
    else:
        orders = []

    context = {
        'orders': orders
    }

    return render(request, 'order_history.html', context)





def process_order(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    order = Order(product=product, quantity=quantity)
    order.save()

    # Decrease stock
    product.decrease_stock(quantity)

    # Add other logic related to order processing (e.g., sending confirmation emails, etc.)

    return redirect('order_history')
