from turtle import title
from django.contrib import admin
from .models import (Customer, Product,Cart, OrderPlaced)
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id', 'user', 'name', 'locality', 'city', 'Zipcode', 'states']
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'selling_price', 'discount_price', 'decription', 'brand', 'category', 'product_image']
admin.site.register(Product, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
admin.site.register(Cart, CartAdmin)    

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer', 'product', 'quantity', 'order_date', 'status']
admin.site.register(OrderPlaced, OrderPlacedAdmin)

def customer_info(self, obj):
    link = reverse("admin:app_customer_change", args=[obj.customer.pk])
    return format_html('<a href="{}">{}</a>', link, obj.customer.name)

def product_info(self, obj):
    link = reverse("admin:app_product_change", args=[obj.product.pk])
    return format_html('<a href="{}">{}</a>', link, obj.product.title)    

    