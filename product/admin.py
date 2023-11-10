from django.contrib import admin
from .models import Product, Image, Category, SubCategory, Cart, Wishlist

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'vendor']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'vendor', 'category', 'sub']
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display  = ['id', 'product', 'image']
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']

@admin.register(Cart)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'image']
    

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer']