from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from django.db import models
from django.conf import settings
from django.db.models.fields import CharField
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
import uuid
 
CATEGORY_CHOICES = (
    ('Cashew','Cashew'),
    ('Grapes','Grapes'),
    ('Icecream','Icecream'),
)
STYLE_CHOICES=(
    ('R','RECTANGLE'),
    ('RO','ROUND'),
)

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Items(models.Model):
    title=models.CharField(max_length=200)
    dis_price=models.FloatField()
    originalprice=models.FloatField(blank=True,null=True)
    category=models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE)
    description=models.CharField(max_length=1000,blank=True,null=True)
    frame_type=models.CharField(max_length=100,blank=True,null=True)
    style=models.CharField(choices=STYLE_CHOICES,default='RECTANGLE',max_length=100)
    color=models.CharField(max_length=20,default="black")
    image=models.ImageField(upload_to='media/',blank=True)
    slug=models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cart:product-detail",kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse("cart:add-to-cart",kwargs={
            'slug':self.slug
        })  

    def get_remove_from_cart(self):
            return reverse("cart:remove-from-cart",kwargs={
            'slug':self.slug
        }) 


    

    



class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    item=models.ForeignKey(Items,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
        

    def __str__(self):
        return self.item.title       

    def get_total_item_price(self):
        return self.quantity * self.item.dis_price   

class BillingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    billingname=models.CharField(max_length=200)
    address_1=models.CharField(max_length=300)
    address_2=models.CharField(max_length=300)
    city=models.CharField(max_length=200)
    district=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=10)
    phonenumber=models.BigIntegerField()
    

    def __str__(self):
        return f"{self.user.username} {self.id}"
   

     


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    total_price=models.FloatField(blank=True,null=True)
    billingaddress=models.OneToOneField(BillingAddress,on_delete=models.CASCADE,null=True)
    delivered=models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.user.username}  {self.id}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total+order_item.get_total_item_price()
        self.total_price=total    
        return total



    def get_update_order(self):
        return reverse("cart:update_order",kwargs={
            'slug':self.id
        })    

    def get_pdf_order(self):
        return reverse("cart:pdf_order",kwargs={
            'slug':self.id
        })    

     

         
class TotalOrder(models.Model):
    totalorder=models.ManyToManyField(Order)


    def __str__(self):
        return f"{self.id}"

    def get_delete_order(self):
            return reverse("cart:delete_order",kwargs={
            'slug': self.id
        })    
   
    


        


class UserOtp(models.Model):
    phonenumber=models.BigIntegerField(blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.IntegerField(blank=True,null=True)    
       


          
 



    


 