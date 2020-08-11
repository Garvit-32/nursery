from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SellerAccount(models.Model):
    sellerId = models.CharField(max_length=15,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=15,null=True)
    organization = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.organization
    
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null = True)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=14)
    sellerId = models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return self.name
    
    


class Product(models.Model):
    # SellerAccount = models.ForeignKey(SellerAccount,on_delete = models.SET_NULL,null=True,blank=True)
    sellerId = models.CharField(max_length=15,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    desc = models.CharField(max_length=250,null=True)
    image = models.ImageField(upload_to='images/' ,null=True,blank=True)

    def __str__(self):
        return self.name + ' from ' + self.sellerId

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total

class OrderItem(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )
    product = models.ForeignKey(Product,on_delete = models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete = models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS,default="Pending")
    sellerId = models.CharField(max_length=15,null=True,blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete= models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    address2 = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class SellerOrder(models.Model):
    
    seller_account = models.ForeignKey(SellerAccount,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete= models.SET_NULL,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    



    
    
        