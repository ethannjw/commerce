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
            'category': forms.Select(choices=Auction.CATEGORIES, attrs={'class': 'hero__search__categories'},),
            'image_url': forms.TextInput(attrs={'class': 'form-control'}),
            'start_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_start_price(self):
        start_price = self.cleaned_data.get('start_price')
        if start_price < 0:
            raise forms.ValidationError("Auction price must be higher 0!")
        return start_price


class BidForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.auction_id = kwargs.pop("auction_id")
        self.auction = Auction.objects.get(id=self.auction_id)
        self.auction_close_price = self.auction.close_price
        self.auction_start_price = self.auction.start_price
        super(BidForm, self).__init__(*args,**kwargs)

    class Meta:
        model = Bid
        fields = ['bid_price']
        labels = {
            'bid_price': ''
        }
        widgets = {
            'bid_price': forms.NumberInput(attrs={
                                                'placeholder': 'Enter your bid',
                                                'id': 'bid',
                                                'label': ''}),
        }

    def clean_bid_price(self):
        bid_price = self.cleaned_data.get('bid_price')
        if bid_price < 0:
            raise forms.ValidationError("Bid price must be higher 0!")
        if bid_price <= self.auction_start_price:
            raise forms.ValidationError("Bid price must be higher than starting bid!")
        if self.auction_close_price:
            if bid_price <= self.auction_close_price:
                raise forms.ValidationError("Bid price must be higher than current bid!")

        return bid_price


class CommentForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.auction_id = kwargs.pop("auction_id")
    #     self.auction = Auction.objects.get(id=self.auction_id)
    #     super(CommentForm, self).__init__(*args,**kwargs)

    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': '',
        }
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Enter your comment',
                                                'id': 'comment',}),
        }
