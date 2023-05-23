from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=25, null=True)
    email= models.CharField(max_length=25, null=True)
    profile_pic = models.ImageField( default='Default-Profile.png', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
        

class Tags(models.Model):
    name = models.CharField(max_length=20, null =True)

    def __str__(self):
        return self.name

class Products(models.Model):
    CATEGORY = (
            ('Indoor', 'Indoor'),
            ('Outdoor', 'Outdoor')

    )
    name = models.CharField(max_length=25, null=True)
    price = models.FloatField()
    category = models.CharField(max_length=25, choices= CATEGORY, null =True)
    description = models.CharField(max_length=25, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name

class Orders(models.Model):

    STATUS = (
            ('Pending', 'Pending'),
            ('Out for delivery', 'Out for delivery'),
            ('Delivered', 'Delivered')

    )
    customer= models.ForeignKey(Customer, null =True, on_delete= models.SET_NULL)
    product =models.ForeignKey(Products, null = True, on_delete= models.SET_NULL)
    date_created= models.DateTimeField(auto_now_add=True, null = True)
    status = models.CharField(max_length=25, choices= STATUS, null=True)
    notes = models.CharField(max_length=500, null = True)

    def __str__(self):
        return self.product.name