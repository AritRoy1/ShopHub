# Generated by Django 4.2.6 on 2023-11-03 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_multipleaddress_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='has_approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
