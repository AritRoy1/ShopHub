from django.contrib import admin
from .models import Product, Image, Category, SubCategory

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'vendor']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'vendor', 'category',]
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display  = ['id', 'product', 'image']
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']

