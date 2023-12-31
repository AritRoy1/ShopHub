# Generated by Django 4.2.6 on 2023-11-23 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_user_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
