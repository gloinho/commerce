# Generated by Django 4.0.6 on 2022-07-06 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[("Men's Fashion", "Men's Fashion"), ('Home and Kitchen', 'Home and Kitchen'), ('Collectible', 'Collectible'), ('Eletronics', 'Eletronics'), ('Office', 'Office'), ('Arts and Crafts', 'Arts and Crafts'), ('Sports and Outdoors', 'Sports and Outdoors'), ('Tools', 'Tools'), ('No Category', 'No Category')], default='No Category', max_length=19),
        ),
    ]
