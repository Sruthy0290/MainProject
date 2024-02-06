from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, name, phone, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name,phone, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
            phone=phone,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    CLIENT = 1
    MENTOR = 2

    ROLE_CHOICE = (
        (CLIENT, 'Client'),
        (MENTOR, 'Mentor'),
    )

    username=None
    first_name=None
    last_name=None
    USERNAME_FIELD = 'email'
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')
    is_blocked = models.BooleanField(default=False)
    

   

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()



    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.name

    

CATEGORY_CHOICES = [
    ('Wheelchair', 'Wheelchair'),
    ('Walker', 'Walker'),
    ('Crutches', 'Crutches'),
    # Add more choices as needed
]

    
class Product(models.Model):
    category =models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='default')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    image = models.ImageField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    
class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True)
    


    def __str__(self):
        return str(self.id)  

    

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total  

  

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

from django.db import models
from django.contrib.auth.models import User

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shipping_addresses', default=1)  # Replace '1' with the ID of the default user
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=10, null=False)
    district = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=200, null=False)
    landmark = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.address}, {self.city}, {self.state}"


        


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.user.name}\'s cart'


sorted_products = {category[0]: Product.objects.filter(category=category[0]) for category in CATEGORY_CHOICES}





class Slots(models.Model):
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
   
    def __str__(self):
        return f"Slot for Dr. {self.mentor.name} on {self.date} at {self.start_time}-{self.end_time}"



class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    mentor = models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.user} - {self.date} {self.time}"

