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
    path('checkout/<int:amt>', v.checkout, name='checkout'),
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

    path('paymenthandler/<int:amount>', v.paymenthandler, name='paymenthandler'),
    path('payment/<int:amt>',v.payment,name="payment"),

    path('add_to_wishlist/<int:product_id>/', v.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', v.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:product_id>/', v.remove_from_wishlist, name='remove_from_wishlist'),

    path('my_profile/', v.my_profile, name='my_profile'),
    path('product_search/', v.product_search, name='product_search'),
    path('order_history/', v.order_history, name='order_history'),
    
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



