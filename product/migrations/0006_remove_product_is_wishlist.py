# Generated by Django 4.2.6 on 2023-10-25 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_is_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_wishlist',
        ),
    ]
