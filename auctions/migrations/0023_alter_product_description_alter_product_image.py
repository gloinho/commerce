# Generated by Django 4.0.6 on 2022-07-13 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(default='https://alnoorfoods.co.uk/wp-content/uploads/2021/01/noimage.jpg'),
        ),
    ]