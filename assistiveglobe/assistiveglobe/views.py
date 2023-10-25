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


from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetConfirmView

def send_custom_password_reset_email(email, uid, token, protocol, domain):
    subject = 'Password Reset Request'
    message = f'''
    Someone requested a password reset for the email {email}.
    Please click the link below to reset your password:
    
    {protocol}://{domain}/reset/{uid}/{token}/
    
    If you did not request a password reset, please ignore this email.
    '''
    sender = 'your_email@example.com'  # Replace with your email address
    recipients = [email]
    
    send_mail(subject, message, sender, recipients)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:  # Check if the password reset was successful
            email = response.context_data.get('user_email')
            uid = response.context_data.get('uid')
            token = response.context_data.get('token')
            protocol = 'http'
            domain = 'localhost:8000'
            
            send_custom_password_reset_email(email, uid, token, protocol, domain)

        return response
