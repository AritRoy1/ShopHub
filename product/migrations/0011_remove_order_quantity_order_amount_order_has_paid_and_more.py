# Generated by Django 4.2.6 on 2023-11-10 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_vendor_has_approved'),
        ('product', '0010_wishlist_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(null=True, verbose_name='Amount'),
        ),
        migrations.AddField(
            model_name='order',
            name='has_paid',
            field=models.BooleanField(default=False, verbose_name='Payment Status'),
        ),
        migrations.AddField(
            model_name='order',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Placed', 'Placed'), ('Shipped', 'Shipped'), ('Out for Delevery', 'Out for Delevery'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel'), ('Pending', 'Pending')], default='Placed', max_length=30),
        ),
        migrations.CreateModel(
            name='OrderCancel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reasion', models.CharField(choices=[('EXD', 'Expected delivery date has changed and the product is arriving at a later date.'), ('PRA.', 'Product is not required anymore.'), ('change my mind', 'Change My Mind'), ('BR', 'Bad review from friends/relatives after ordering the product.')], max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]