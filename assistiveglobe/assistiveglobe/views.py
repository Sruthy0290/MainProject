from django.shortcuts import render,redirect 
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import SignupForm
from django.shortcuts import render, get_object_or_404
from userapp.models import *

User=get_user_model()
# Create your views here.
def login(request):
    
    return render(request,"login.html")
from django.shortcuts import render, redirect

# def home(request):
#     if request.user.is_authenticated:
#         if request.user.role == CustomUser.CLIENT:
#             # Assuming you have a different URL name for the client's homepage
#             return redirect('home')
#         # elif request.user.role == CustomUser.THERAPIST:
#         #     # Assuming you have a URL pattern named 'therapist'
#         #     return redirect('therapist')
#         elif request.user.role == CustomUser.ADMIN:
#             return redirect('dashboard')
#     else:
#         return render(request, "home.html", {'user': request.user})
def home(request):
    if request.user.is_authenticated:
        if request.user.role == 1 and not request.path == reverse('home'):
            return redirect(reverse('home'))
        # elif request.user.role == 1 and not request.path == reverse('index'):
        #     return redirect(reverse('index'))

    return render(request, "home.html", {'user': request.user})


