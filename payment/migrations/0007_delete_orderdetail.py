# Generated by Django 4.2.6 on 2023-11-02 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_orderdetail_session_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderDetail',
        ),
    ]
