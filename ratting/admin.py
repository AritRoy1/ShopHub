from django.contrib import admin

# Register your models here.
from .models import Ratting

@admin.register(Ratting)
class RattingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'ratting', 'created_at']