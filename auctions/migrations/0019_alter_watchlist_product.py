# Generated by Django 4.0.6 on 2022-07-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='product',
            field=models.ManyToManyField(related_name='watchlisted', to='auctions.product'),
        ),
    ]
