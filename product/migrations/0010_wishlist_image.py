# Generated by Django 4.2.6 on 2023-10-27 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_rename_customer_wishlist_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.image'),
        ),
    ]