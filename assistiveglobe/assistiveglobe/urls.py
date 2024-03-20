"""
URL configuration for assistiveglobe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from assistiveglobe import views
from userapp import views as v
from django.conf import settings
from django.conf.urls.static import static
from userapp.views import delete_product_confirm
from userapp.views import add_to_cart
from userapp.views import remove_from_cart
from userapp.views import block_user
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetConfirmView
from userapp.views import make_appointment
from userapp.views import add_mentor
from userapp.views import mentor1
from userapp.views import check_mentor_availability
from userapp.views import get_available_times


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('accounts/', include('allauth.urls')),
    path('about/',v.about,name='about'),
    path('login/',v.login,name='login'),
    path('signup/',v.signup,name='signup'),
    path('logout/',v.logout,name='logout'),
    path('product/', v.product, name='product'),
    path('admin_product/', v.admin_product, name='admin_product'),
    path('product_detail/<int:product_id>/', v.product_detail, name='product_detail'),  
    path('cart',v.cart,name='cart'),
    path('add_to_cart/<int:product_id>/',v.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/', v.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:cart_id>/', v.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/<int:amt>/', v.checkout, name='checkout'),
    path('checkout/new/', v.checkout_view, name='checkout_new'),

    path('edit_address/', v.edit_address, name='edit_address'),
    path('dashboard/',v.dashboard,name='dashboard'),
    path('user_detail/',v.user_detail, name='user_detail'),
    path('block_user/<int:user_id>/', v.block_user, name='block_user'),
    path('login/', v.custom_login, name='login'),
    path('add_product/', v.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', v.delete_product, name='delete_product'), 
    path('delete_product_confirm/<int:product_id>/',delete_product_confirm, name='delete_product_confirm'),  
    path('edit_product/<int:product_id>/', v.edit_product, name='edit_product'),
    path('product/<str:category>/', v.product, name='product_category'),
    path('wheelchair/', v.wheelchair, name='wheelchair'),
    path('walker/', v.walker, name='walker'),
    path('crutches/', v.crutches, name='crutches'),
    path('stock/',v.stock,name='stock'),
    path('update_stock/<int:product_id>/', v.update_stock, name='update_stock'),
    path('add_review/',v.add_review,name='add_review'),

    path('paymenthandler/<int:amount>', v.paymenthandler, name='paymenthandler'),
    path('payment/<int:amt>',v.payment,name="payment"),
    path('payment/<int:product_id>',v.payment,name="payment"),

    path('add_to_wishlist/<int:product_id>/', v.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', v.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:product_id>/', v.remove_from_wishlist, name='remove_from_wishlist'),

    path('my_profile/', v.my_profile, name='my_profile'),
    path('product_search/', v.product_search, name='product_search'),
    path('order_history/', v.order_history, name='order_history'),

    # Mentor
    path('mentorindex/', v.mentorindex, name='mentorindex'),
    path('add_mentor/', v.add_mentor, name='add_mentor'),
    path('mentor1/', v.mentor1, name='mentor1'),
    path('slot/', v.slot, name='slot'),
    path('view_appointment/', v.view_appointment, name='view_appointment'),
    path('appointment/', v.appointment, name='appointment'),
    path('check_mentor_availability/', v.check_mentor_availability, name='check_mentor_availability'),
    path('make_appointment/', v.make_appointment, name='make_appointment'),
    path('appointment_userview/', v.appointment_userview, name='appointment_userview'),
    path('cancel_appointment/<int:appointment_id>/', v.cancel_appointment, name='cancel_appointment'),
    path('bookedslot/', v.bookedslot, name='bookedslot'),
    path('cancel_slot/<int:slot_id>/', v.cancel_slot, name='cancel_slot'),
    path('get_available_times/', v.get_available_times, name='get_available_times'),
    path('get_user_appointments/',v.get_user_appointments, name='get_user_appointments'),
    
    
    path('add_delivery_agent/', v.add_delivery_agent, name='add_delivery_agent'),
    path('deliveryagent/', v.deliveryagent, name='deliveryagent'),
    path('view_delivery_agent', v.view_delivery_agent, name='view_delivery_agent'),
    path('view_orders/', v.view_orders, name='view_orders'),
    path('current_delivery_tasks/', v.current_delivery_tasks, name='current_delivery_tasks'),
    path('accept_order/', v.accept_order, name='accept_order'),









    # path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    
    # path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    
    # path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



