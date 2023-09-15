from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import SignupForm
from django.shortcuts import render, get_object_or_404


User=get_user_model()
# Create your views here.
def login(request):
    return render(request,"login.html")
def home(request):
    return render(request,"home.html",{'user': request.user})
