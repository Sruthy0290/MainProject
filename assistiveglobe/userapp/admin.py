from django.contrib import admin
from .models import CustomUser
# from .models import Category
from .models import Product
from .models import Order
from .models import OrderItem
from .models import ShippingAddress
from .models import CartItem,Appointment

# Register your models here.
# admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(CartItem)
admin.site.register(Appointment)
