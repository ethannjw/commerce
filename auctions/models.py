from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watched_list = models.ManyToManyField('Auction', blank=True, related_name="watchlist")

class Auction(models.Model):
    CATEGORIES=[
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Others', 'Others'),
    ]
    auction_name = models.CharField(max_length=128, default="")
    description = models.TextField()

    start_price = models.DecimalField(max_digits=9, decimal_places=2)
    close_price = models.DecimalField(null=True, max_digits=9, decimal_places=2)

    created_time = models.DateTimeField(auto_now_add=True)
    close_time = models.DateTimeField(null=True, blank=True)

    image_url = models.URLField(null=True)
    category = models.CharField(max_length=128, choices=CATEGORIES, default='Fashion')
    open_status = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_owner")
    def __str__(self):
        return f"Auction name: {self.name} Price: {self.price} Creator: {self.creator}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid_price = models.DecimalField(max_digits=9, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Bid by {self.user} on: {self.auction} Price: ${self.bid_price} at: {self.bid_time}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    commented_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.user}  on: {self.auction} Comment: {self.comment}"
