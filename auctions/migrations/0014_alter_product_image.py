# Generated by Django 4.0.6 on 2022-07-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='./auctions/static/auctions/images'),
        ),
    ]
