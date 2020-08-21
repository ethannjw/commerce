from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist=[]

class Auction(models.Model):
    CATEGORIES=[
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
    ]
    name = models.CharField(max_length=128, primary_key=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=1280)
    category = models.CharField(max_length=128, choices=CATEGORIES, default='Fashion')
    def __str__(self):
        return f"Auction name: {self.name} Price: {self.price}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid_price = models.DecimalField(max_digits=9, decimal_places=2)

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
