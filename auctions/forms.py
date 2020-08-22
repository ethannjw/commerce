from django import forms
from .models import Auction, User, Bid, Comment



class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['auction_name', 'description', 'start_price', 'image_url', 'category']
        labels = {
            'auction_name': 'Auction Title',
            'description': 'Description',
            'category' : 'Category',
            'start_price' : 'Starting Price',
            'image_url' : 'Listing Image URL (optional but recommended!)',
        }
        widgets = {
            'auction_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Description', 'rows':8}),
            'category': forms.Select(choices=Auction.CATEGORIES, attrs={'class': 'form-control'},),
            'image_url': forms.TextInput(attrs={'class': 'form-control'}),
            'start_price': forms.TextInput(attrs={'class': 'form-control'}),
        }
