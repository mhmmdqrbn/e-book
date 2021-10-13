from django.db import models
from django.contrib.auth.models import User
from django.db.models import fields

from django.forms import ModelForm
from product.models import Product

# Create your models here.

class ShopCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def amount(self):
        
        return (self.quantity * self.product.price)

    @property
    def price(self):
        if self.product_id is not None:
            return (self.product.price)
        

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields={'quantity'}


class Order(models.Model):
    STATUS = (
        ('Yeni','Yeni'),
        ('Qəbul olundu','Qəbul olundu'),
        ('Yolda','Yolda'),
        ('Tamamlandı','Tamamlandı'),
        ('Ləğv olundu','Ləğv olundu')
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=5,editable=False)
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    phone = models.CharField(blank=True,max_length=155)
    address = models.CharField(blank=True,max_length=155)
    city = models.CharField(blank=True,max_length=155)
    country = models.CharField(blank=True,max_length=155)
    total = models.FloatField()
    status = models.CharField(max_length=155,choices=STATUS,default='Yeni')
    ip = models.CharField(blank=True,max_length=55)
    adminnote = models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','phone','city','country']


class OrderProduct(models.Model):
    STATUS = (
        ('Yeni','Yeni'),
        ('Qəbul olundu','Qəbul olundu'),
        ('Ləğv olundu','Ləğv olundu')
    )
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=15,choices=STATUS,default='Yeni')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

