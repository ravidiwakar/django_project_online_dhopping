from itertools import product
from msilib.schema import Class
from pyexpat import model
from sre_constants import CATEGORY
from statistics import mode
from tkinter import CASCADE
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('Bihar','Bihar'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Delhi','Delhi'),
    ('Haryana', 'Haryana'),
    ('Punjab', 'Punjab')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    Zipcode = models.IntegerField()
    states = models.CharField(choices=STATE_CHOICES, max_length=50)
    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('Mobile','Mobile'),
    ('Laptop', 'Laptop'),
    ('Top wear', 'Top wear'),
    ('Buttom wear', 'Buttom wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    decription = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_image = models.ImageField(upload_to='productimg')
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price    

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='pending')

    def __str__(self):
        return str(self.id)


    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price     















# Create your models here.
