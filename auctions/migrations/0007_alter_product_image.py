# Generated by Django 4.0.6 on 2022-07-06 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(height_field=100, upload_to='./static/auctions', width_field=100),
        ),
    ]
