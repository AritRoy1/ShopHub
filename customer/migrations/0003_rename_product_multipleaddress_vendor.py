# Generated by Django 4.2.6 on 2023-10-26 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_multipleaddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multipleaddress',
            old_name='product',
            new_name='vendor',
        ),
    ]