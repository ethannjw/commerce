# Generated by Django 3.0.3 on 2020-08-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200824_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='close_price',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
    ]
