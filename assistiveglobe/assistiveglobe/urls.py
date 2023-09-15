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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about/',v.about,name='about'),
    path('login/',v.login,name='login'),
    path('signup/',v.signup,name='signup'),
    path('logout/',v.logout,name='logout'),
    path('product/', v.product, name='product'),
    path('admin_product/', v.admin_product, name='admin_product'),
    path('product_detail/<int:product_id>/', v.product_detail, name='product_detail'),
    path('cart/',v.cart,name='cart'),
    path('dashboard/',v.dashboard,name='dashboard'),
    path('add_product/', v.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', v.delete_product, name='delete_product'), 
    path('delete_product_confirm/<int:product_id>/',delete_product_confirm, name='delete_product_confirm'),  
    path('update_product/<int:product_id>/', v.update_product, name='update_product'),
    path('product/<str:category>/', v.product, name='product_category'),
    path('wheelchair/', v.wheelchair, name='wheelchair'),
    path('walker/', v.walker, name='walker'),
    path('crutches/', v.crutches, name='crutches'),
    
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
