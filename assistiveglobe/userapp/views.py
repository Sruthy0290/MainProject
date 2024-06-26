from django.shortcuts import render,redirect
from userapp.models import CustomUser
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from userapp.models import *
from django.contrib.auth.decorators import login_required
from userapp.models import Order
from userapp.models import  Product
from django.shortcuts import render
from assistiveglobe.forms import ProductForm,ProductUpdateForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail






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



def login(request):
    if request.user.is_authenticated:
        if request.user.role == CustomUser.CLIENT:
            return redirect('http://127.0.0.1:8000/')
        elif request.user.role == CustomUser.MENTOR:
            return redirect('mentor1')
        elif request.user.role == CustomUser.DELIVERY:
            return redirect('deliveryagent')
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
                if user.role == CustomUser.MENTOR:
                    return redirect('mentor1')  # Redirect to the mentor1 page
                elif user.role == CustomUser.DELIVERY:
                    return redirect('deliveryagent')
                else:
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


#
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



from userapp.models import Product, Review
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})



from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from userapp.models import Product, CartItem

@login_required
def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))  # Get the selected quantity or default to 1
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Check if the requested quantity exceeds the available stock
    if quantity > product.stock:
        messages.error(request, f'Sorry, only {product.stock} items are available.')
    else:
        # Check if the product is already in the cart
        cart_item = CartItem.objects.filter(product_id=product_id, user_id=user.id).first()
        
        # If the product is already in the cart, update the quantity
        if cart_item:
            new_quantity = cart_item.quantity + quantity
            # Check if the new quantity exceeds the available stock
            if new_quantity > product.stock:
                messages.error(request, f'Sorry, only {product.stock} items are available.')
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, 'Product quantity updated in cart.')
        else:
            # If the product is not in the cart, create a new cart item
            cart_item = CartItem.objects.create(
                product_id=product_id,
                user_id=user.id,
                quantity=quantity
            )
            messages.success(request, 'Product added to cart successfully.')

    return redirect('cart')



@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    product_ids = [item.product.id for item in cart_items]
    
    print(product_ids)
    
    context = {
        'cart_items':cart_items,
        'total_items':total_items,
        'total_price':total_price,
        'product_ids':product_ids,
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



# from userapp.models import CustomUser
# from django.shortcuts import render, redirect
# from userapp.models import ShippingAddress

# def checkout_view(request):
#     name = ""
#     phone = ""
#     district = ""

#     if request.method == 'POST':
#         # Assuming you have a form for the new address
#         form = checkout(request.POST)

#         if form.is_valid():
#             new_address = form.save(commit=False)
#             new_address.user = request.user
#             new_address.save()
            

#             # Update saved_address and related fields
#             name = new_address.name
#             phone = new_address.phone
#             district = new_address.district
#     else:
#         form = checkout()

#     context = {
#         'name': name,
#         'phone': phone,
#         'district': district,
#         'form': form,
#     }

#     return render(request, 'checkout.html', context)


from django.shortcuts import render, redirect
from userapp.models import ShippingAddress

from django.shortcuts import render, redirect
from userapp.models import ShippingAddress

def checkout_view(request,amt):
    name = ""
    phone = ""
    district = ""
    amt = 0  # Assuming amt is initialized with a default value

    if request.method == 'POST':
        # Get the values from the HTML form fields
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        zipcode = request.POST.get('zipcode', '')
        state = request.POST.get('state', '')
        landmark = request.POST.get('landmark', '')

        # Save the shipping address
        new_address = ShippingAddress.objects.create(
            user=request.user,
            name=name,
            address=address,
            phone=phone,
            city=city,
            zipcode=zipcode,
            state=state,
            landmark=landmark
        )

        # Update saved_address and related fields
        name = new_address.name
        phone = new_address.phone
        district = new_address.district

        # Fetch the amt value from wherever it's supposed to come from
        amt = amt  # Replace this with your actual logic to determine amt
        return redirect('checkout', amt=amt)
    
    context = {
        'name': name,
        'phone': phone,
        'district': district,
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
        'sorted_products': sorted_products,  # Add sorted products to context
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



# STOCK 
from django.shortcuts import render, redirect
from userapp.models import Product

def stock(request):
    products = Product.objects.all()
    return render(request, 'stock.html', {'products': products})

def update_stock(request, product_id):
    if request.method == 'POST':
        stock = int(request.POST.get('stock'))
        product = Product.objects.get(id=product_id)
        product.stock = stock
        product.save()
        return redirect('stock')



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

    cartitems=CartItem.objects.filter(user=request.user)
    for i in cartitems:
        order=Order.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        product_id=i.product_id
        )
        
        order.save()
        assign_orders(request.user.id,order.id)
        
    cartitems.delete()



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


from django.core.mail import send_mail
from userapp.models import Order, CustomUser

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
            order = Order.objects.filter(razorpay_order_id=razorpay_order_id)

            # Update the order with the payment_id
            for i in order:
                i.transaction_id = payment_id
                i.complete = True
                i.save()
                OrderItem(
                    order_id=i.id,
                    product_id=i.product_id,
                    date_added=timezone.now()
                ).save()
                prod=Product.objects.get(id=i.product_id)
                prod.stock=prod.stock-1
                prod.save()


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


# from django.shortcuts import render
# from userapp.models import Order,Product
# def order_history(request):
#     if request.user.is_authenticated:
#         # Filter completed orders for the logged-in user
#         orders = Order.objects.filter(user=request.user, complete=True)

#         # Initialize an empty dictionary to store order items for each order
#         order_items_dict = {}

#         # Retrieve associated OrderItems for each order
#         for order in orders:
#             order_items = OrderItem.objects.filter(order=order)
#             order_items_dict[order] = order_items

#     else:
#         orders = []
#         order_items_dict = {}

#     context = {
#         'orders': orders,
#         'order_items_dict': order_items_dict,  # Pass the dictionary containing order items for each order
#     }
#     return render(request, 'order_history.html', context)

from django.shortcuts import render
from userapp.models import Order,Product,Delivery
@login_required
def order_history(request):
    if request.user.is_authenticated:
        # Filter completed orders for the logged-in user
        orders = Order.objects.filter(user=request.user, complete=True).order_by('-date_ordered')

        # Initialize a list to store order data
        order_data = []

        # Retrieve associated OrderItems and delivery status for each order
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            order_item_data = []
            for order_item in order_items:
                delivery = Delivery.objects.filter(order=order_item).first()
                delivery_status = delivery.status if delivery else "Not Found"
                order_item_data.append({
                    'product': order_item.product,
                    'delivery_status': delivery_status,
                    # Add other fields as needed
                })
                print(f"Order Item: {order_item}, Delivery Status: {delivery_status}")
            order_data.append({
                'order': order,
                'order_items': order_item_data,
            })

    else:
        orders = []
        order_data = []

    context = {
        'orders': orders,
        'order_data': order_data,
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





def mentorindex(request):
    return render(request, 'mentorindex.html')



from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import CustomUser
from django.contrib import messages

def add_mentor(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Save mentor details to the database (you might want to use a Mentor model)
        mentor = User(name=name, email=email, phone=phone, password=password, role=CustomUser.MENTOR)
        mentor.first_name = name
        mentor.save()

        # Send approval email
        subject = 'Mentor Approval'
        message = f'Hello {name},\n\nYour mentor account has been approved. Use the following credentials to login:\n\nUsername: {email}\nPassword: {password}\n\nThank you!'
        from_email = 'assistiveglobe@gmail.com'  # Update with your admin email
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Mentor added successfully. Approval email sent.')
        return redirect('dashboard')  # Redirect to the dashboard or any other desired page

    return render(request, 'add_mentor.html')  # Update with your actual template path






from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def mentor1(request):
    mentor_name = request.user.username  # Assuming the mentor's name is the username
    mentor_email = request.user.email  # Assuming you have an email attribute in your CustomUser model
    mentor_phone = request.user.phone  # Assuming you have a phone attribute in your CustomUser model

    return render(request, 'mentor1.html', {
        'mentor_name': mentor_name,
        'mentor_email': mentor_email,
        'mentor_phone': mentor_phone,
    })




from django.shortcuts import render, redirect
from userapp.models import Slots
from django.contrib.auth.decorators import login_required
from datetime import datetime
@login_required
def slot(request):
    template_name = 'slot.html'
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time_slots = request.POST.getlist('time_slot')  # Retrieve selected time slots as a list

        print("Date:", date)  # Debug output
        print("Time slots:", time_slots)  # Debug output

        if date and time_slots:
            # Iterate over the selected time slots and save each one
            for selected_slot in time_slots:  # Renamed the loop variable
                start_time, end_time = selected_slot.split(' - ')  # Split the time slot string to get start and end times
                print("Start time:", start_time)  # Debug output
                print("End time:", end_time)  # Debug output
                # Create and save the slot object
                slot_obj = Slots.objects.create(
                    mentor=request.user,
                    date=date,
                    start_time=start_time,
                    end_time=end_time
                )
                slot_obj.save()
            
            return redirect('mentor1')
    slots = Slots.objects.filter(mentor=request.user)
    return render(request, 'slot.html', {'slots': slots})  # Fixed the template name argument


# views.py

from django.http import JsonResponse
from userapp.models import Slots

def get_available_times(request):
    selected_date = request.GET.get('date')
    
    # Retrieve the available time slot for the selected date
    available_slot = Slots.objects.filter(date=selected_date, cancelled=False).first()
    
    if available_slot:
        # If an available slot is found, format the time slot
        available_time = f"{available_slot.start_time} - {available_slot.end_time}"
        return JsonResponse({'availableTimes': [available_time]})
    else:
        return JsonResponse({'availableTimes': []})  # Return an empty array if no slot is available


# Django View
from django.shortcuts import render
from django.http import JsonResponse
from userapp.models import Slots

def check_mentor_availability(request):
    if request.method == 'GET':
        mentor_id = request.GET.get('mentor')
        if mentor_id:
            try:
                # Retrieve available and cancelled slots for the mentor
                available_slots = Slots.objects.filter(mentor_id=mentor_id, cancelled=False)
                cancelled_slots = Slots.objects.filter(mentor_id=mentor_id, cancelled=True)

                # Extract time slots from cancelled slots
                cancelled_times = [f"{slot.start_time}-{slot.end_time}" for slot in cancelled_slots]

                # Determine available times based on available slots
                available_times = []
                for slot in available_slots:
                    available_times.append({
                        'start_time': slot.start_time,
                        'end_time': slot.end_time
                    })

                # Extract available dates from available slots
                available_dates = list(set(slot.date for slot in available_slots))

                # Return data as JSON response
                return JsonResponse({
                    'available_dates': available_dates,
                    'available_times': available_times,
                    'cancelled_times': cancelled_times
                })
            except Slots.DoesNotExist:
                return JsonResponse({'error': 'Slots not found for this mentor'}, status=404)

    return JsonResponse({'error': 'Invalid request method or missing mentor ID'}, status=400)



from django.shortcuts import render, redirect
from userapp.models import CustomUser
from userapp.models import Appointment
from django.contrib import messages
from datetime import datetime

def generate_zoom_link():
    # Replace these with your Zoom API credentials
    api_key = "R3Xmzt5kTwSBiDR62xcz9w"
    api_secret = "35E4VqVqeveFLNXOdtLRWPNy3HYmlKpA"

    # Generate a random meeting ID using the secrets module
    meeting_id = "6300709403"

    # Construct the Zoom link
    zoom_link = f"https://zoom.us/j/{meeting_id}?pwd={api_secret}&api_key={api_key}"

    return zoom_link

def appointment(request):
    mentors = CustomUser.objects.filter(role=2)  # Assuming 'role=2' represents mentors
    context = {'mentors': mentors}
    
    if request.method == 'POST':
        # If the form is submitted
        user = request.user  # Assuming request.user is the logged-in user
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        mentor_id = request.POST.get('mentor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        mentor = CustomUser.objects.get(id=mentor_id)
        
        # Check if an appointment with the same user, mentor, date, and time already exists
        existing_appointment = Appointment.objects.filter(
            # user=user,
            mentor=mentor,
            date=appointment_date,
            time=appointment_time
        ).exists()
        
        if existing_appointment:
            # If an existing appointment is found, show a warning message
            messages.warning(request, 'An appointment with the same mentor, date, and time already exists.')
            return redirect('appointment')
        else:
            # If no existing appointment found, proceed with creating the appointment
            zoom_link = generate_zoom_link()
            print(mentor_id)
            print(zoom_link)

            # Retrieve the mentor object
            mentor = CustomUser.objects.get(id=mentor_id)

            # Create a new appointment object
            appointment = Appointment(
                user=user,
                date=appointment_date,
                time=appointment_time,
                mentor=mentor,
                zoom_link=zoom_link
            )
            # Save the appointment to the database
            appointment.save()

            # Optionally, you can redirect the user to a success page
            return redirect('mentorindex')
    else:
        # If it's a GET request, retrieve mentors from the database
        mentors = CustomUser.objects.all()
        # Get the list of cancelled dates and times
        cancelled_dates = Appointment.objects.filter(cancelled=True).values_list('date', flat=True)
        cancelled_times = Appointment.objects.filter(cancelled=True).values_list('time', flat=True)
        # Pass the cancelled dates and times to the template context
        context['cancelled_dates'] = cancelled_dates
        context['cancelled_times'] = cancelled_times
        return render(request, 'appointment.html', context)
    

from django.shortcuts import render, redirect
from django.contrib import messages
from userapp.models import CustomUser, Appointment

def make_appointment(request):
    if request.method == 'POST':
        # If the form is submitted
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        mentor_id = request.POST.get('mentor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        print(mentor_id)
        
        # Retrieve the mentor object
        mentor = CustomUser.objects.get(id=mentor_id)

        # Create a new appointment object
        appointment = Appointment(
            user=request.user,  # Assuming request.user is the logged-in user
            date=appointment_date,
            time=appointment_time,
            mentor=mentor
        )
        # Save the appointment to the database
        appointment.save()
        print("saved")

        # Optionally, you can redirect the user to a success page
        return redirect('mentorindex')  # Replace 'mentorindex' with the URL name of your success page
    else:
        # If it's a GET request, retrieve mentors from the database
        mentors = CustomUser.objects.all()
        
        # Get available appointments by excluding cancelled appointments
        available_mentors = []
        for mentor in mentors:
            available_appointments = mentor.appointment_set.filter(cancelled=False)  # Exclude cancelled appointments
            available_mentors.append({
                'mentor': mentor,
                'available_appointments': available_appointments
            })

        context = {
            'mentors': available_mentors,
        }
        
        return render(request, 'appointment.html', context)



from django.shortcuts import render
from userapp.models import Appointment

def view_appointment(request):
    mentor = request.user  # Assuming the logged-in user is the mentor
    appointments = Appointment.objects.filter(mentor=mentor)
    # Get the list of cancelled dates and times
    cancelled_dates = Appointment.objects.filter(cancelled=True).values_list('date', flat=True)
    cancelled_times = Appointment.objects.filter(cancelled=True).values_list('time', flat=True)
    return render(request, 'view_appointment.html', {'appointments': appointments, 'cancelled_dates': cancelled_dates, 'cancelled_times': cancelled_times})



from django.shortcuts import render
from userapp.models import Appointment
def appointment_userview(request):
    user = request.user
    # Retrieve all appointments for the user
    appointments = Appointment.objects.filter(user=user)
    print(appointments)
    # Retrieve cancelled appointments for the user
    cancelled_appointments = appointments.filter(cancelled=True)
    # Extract cancelled dates and times
    cancelled_dates = cancelled_appointments.values_list('date', flat=True)
    cancelled_times = cancelled_appointments.values_list('time', flat=True)
    # Pass all appointments and cancelled dates/times to the template
    return render(request, 'appointment_userview.html', {'appointments': appointments, 'cancelled_dates': cancelled_dates, 'cancelled_times': cancelled_times})



from django.shortcuts import redirect, get_object_or_404
from userapp.models import Appointment
from twilio.rest import Client
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.cancelled = True
    appointment.save()

    # Initialize Twilio client with your Twilio account SID and auth token
    client = Client("AC92d60b381a5001f92b074412190efa89", "5835cdfc1e86b98e02c2dd4af81c135e")

    # Replace 'from_' with your Twilio phone number and 'to' with the user's phone number
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="Your appointment has been cancelled.",
        to='whatsapp:+919400453044'
    )

    return redirect('view_appointment')



from django.shortcuts import render
from userapp.models import Slots

def bookedslot(request):
    mentor_id = request.user.id
    booked_slots = Slots.objects.filter(mentor_id=mentor_id, cancelled=False)
    cancelled_slots = Slots.objects.filter(mentor_id=mentor_id, cancelled=True)
    print(booked_slots)
    return render(request, 'bookedslot.html', {'booked_slots': booked_slots, 'cancelled_slots': cancelled_slots})



from django.shortcuts import render, redirect
from django.http import HttpResponse
from userapp.models import Slots
from django.http import JsonResponse

def cancel_slot(request, slot_id):
    if request.method == 'GET':
        try:
            slot = Slots.objects.get(id=slot_id)
            slot.cancelled = True
            slot.save()
            return JsonResponse({'success': True})
        except Slots.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Slot not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method or missing slot_id'}, status=400)



from django.shortcuts import render
from userapp.models import Appointment

def get_user_appointments(request, date):
    user = request.user  # Assuming user is authenticated
    user_appointments = Appointment.objects.filter(user=user, date=date).values_list('time', flat=True)
    return JsonResponse({'appointments': list(user_appointments)})




from django.contrib.auth.hashers import make_password  # Import Django's password hashing function
# from django.contrib.auth.models import CustomUser
from django.utils.crypto import get_random_string
from userapp.models import CustomUser
from django.contrib import messages
from django.core.mail import send_mail


def add_delivery_agent(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')  # New field for the location
        driving_license_file = request.FILES.get('driving_license')


        # Generate a random password
        raw_password = get_random_string(length=10)  # Generates a 10-character random string

        # Hash the password
        hashed_password = make_password(raw_password)

        # Save delivery agent details to the database
        delivery = CustomUser(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            location=location,  # Save the location
            driving_license=driving_license_file,

            role=CustomUser.DELIVERY
        )
        delivery.save()

        # Send approval email
        subject = 'Delivery Agent Approval'
        message = f'Hello {name},\n\nYour delivery agent account has been approved. Use the following credentials to login:\n\nUsername: {email}\nPassword: {raw_password}\n\nThank you!'
        from_email = 'assistiveglobe@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, 'Agent added successfully. Approval email sent.')
        return redirect('dashboard')

    return render(request, 'add_delivery_agent.html')



from django.shortcuts import render
from userapp.models import CustomUser

def view_delivery_agent(request):
    # Fetch all delivery agents
    agents = CustomUser.objects.filter(role=CustomUser.DELIVERY)

    context = {
        'agents': agents
    }

    return render(request, 'view_delivery_agent.html', context)





from django.shortcuts import render, redirect
from userapp.models import Product, Review
from django.contrib import messages

def add_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        user = request.user
        
        # Check if the user has already reviewed the product
        existing_review = Review.objects.filter(user=user, product=product).first()
        if existing_review:
            messages.warning(request, 'You have already reviewed this product.')
        else:
            # Create and save the new review
            review = Review.objects.create(user=user, product=product, rating=rating, comment=comment)
            messages.success(request, 'Your review has been submitted successfully.')
    
    return redirect('product_detail', product_id=product_id)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def deliveryagent(request):
    delivery_name = request.user.username  
    delivery_email = request.user.email  
    delivery_phone = request.user.phone  

    return render(request, 'deliveryagent.html', {
        'delivery_name': delivery_name,
        'delivery_email': delivery_email,
        'delivery_phone': delivery_phone,
    })



from django.shortcuts import render
from userapp.models import Order

def view_orders(request):
    # Get all orders
    orders = Order.objects.all()

    return render(request, 'view_orders.html', {'orders': orders})




from django.shortcuts import render
from userapp.models import OrderItem

def current_delivery_tasks(request):
    # Get all order items
    order_items = OrderItem.objects.all()

    return render(request, 'current_delivery_tasks.html', {'order_items': order_items})




from django.db.models import Min
from django.core.mail import send_mail
from .models import Order, CustomUser

def assign_orders(user_id,order_id):
    order = Order.objects.get(id=order_id)  # Get unassigned orders
    ship_location=ShippingAddress.objects.get(user_id=user_id)

        # Find the closest available delivery person based on user and delivery person locations
    agents=CustomUser.objects.filter(role=3)
    for i in agents:
        if ship_location.city==i.location:
            closest_delivery_person=i
            break
    if closest_delivery_person:
        order.assigned_delivery_person = closest_delivery_person
        order.save()
            # Notify the assigned delivery person
        notify_delivery_person(closest_delivery_person, order)


def notify_delivery_person(delivery_person, order):
    subject = 'New Order Assigned'
    message = f'Hi {delivery_person.name},\n\nYou have been assigned a new order with ID {order.id}.\n\nThank you.'
    from_email = 'assistiveglobe@gmail.com'  # Update with your email
    to_email = delivery_person.email
    send_mail(subject, message, from_email, [to_email])



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import OrderItem

def order_status(request, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id)
    if order_item.delivery:
        status = order_item.delivery.status
    else:
        status = 'Not Available'
    return JsonResponse({'status': status})



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import OrderItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

@login_required
def update_order_status(request, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id)
    delivery, created = Delivery.objects.get_or_create(order=order_item, defaults={'delivery': request.user})
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['out_for_delivery', 'delivered']:
            # Update the delivery status and timestamp
            delivery.status = new_status
            delivery.updated_at = timezone.now()
            delivery.save()

            # Update the product status if order is delivered
            if new_status == 'delivered':
                order_item.product.status = 'Delivered'
                order_item.product.save()

            # Render the updated order item data
            order_item_html = render_to_string('current_delivery_tasks.html', {'order_item': order_item})

            # Return success message and updated order item HTML
            return JsonResponse({'success_message': 'Order status updated successfully', 'order_item_html': order_item_html})
        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



