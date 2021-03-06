# Generated by Django 3.0.3 on 2020-08-23 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200822_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watched_auctions',
        ),
        migrations.AddField(
            model_name='user',
            name='watched_list',
            field=models.ManyToManyField(blank=True, related_name='user_watched_list', to='auctions.Auction'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
