# Generated by Django 3.0.4 on 2020-09-23 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200924_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='logo.jpg', null=True, upload_to=''),
        ),
    ]
