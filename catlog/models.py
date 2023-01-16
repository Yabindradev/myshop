from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import date



    
    
class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self, ):
        return reverse("category", args=[self.id])


class Product(models.Model):
    slug = models.SlugField(max_length=255)
    title = models.CharField(max_length=120)  # max_length = required
    product_code_number = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    is_discountable = models.BooleanField(default=True)
    first_images = models.ImageField()
    second_images = models.ImageField(blank=True, null=True)
    third_images = models.ImageField(blank=True, null=True)
    forth_images = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    price = models.BigIntegerField()
    is_stock = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self, ):
        return reverse("product_detail", args=[self.id])




class Order(models.Model):
    ORDERED ='Ordered'
    SHIPPED  ='Shipped'
    DELIVERED = 'Delivered'
    
    STATUS = (
        (ORDERED, 'Ordered'),
        (SHIPPED , 'Shipped'),
        (DELIVERED, 'Delivered')
    )
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE, null=True)
    order_no = models.CharField(max_length=20)
    user = models.ForeignKey(
        User, related_name='order', on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    zipcode = models.CharField(max_length=100)
    payment_intent = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True)
    staus = models.CharField(max_length=30, choices=STATUS, default=ORDERED)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255)



   

    class Meta:
        ordering = ['-created_at']
        

    

    def __str__(self):
        return self.email
    
    def get_absolute_url(self, ):
        return reverse("order", args=[self.id])
    
  


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE )

    def __str__(self):
        return f"{self.quantity} of {self.products.title}"



    
class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete = models.CASCADE)
    userprofile = models.ImageField(upload_to='userprofile/', default="userprofile/avator.png")
    
    def __str__(self):
        return str(self.user)
    
    
    
    



class Invoice(models.Model):
   invoice_no = models.CharField(max_length=20)
   invoice_date = models.DateField()
   invoice_amount = models.DecimalField(
       max_digits=12, decimal_places=2, blank=True, null=True)
   
   customer_name = models.CharField(max_length=225)
   customer_email = models.EmailField(max_length=225)
   customer_phone = models.CharField(max_length=20, blank= True, null=True)
   customer_address = models.CharField(max_length=225, blank=True, null=True)
   products = models.CharField(max_length=255, blank=True, null=True)
   
   
   def __str__(self):
       return self.invoice_no
   
   


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    min_purchase = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    expires = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.code
