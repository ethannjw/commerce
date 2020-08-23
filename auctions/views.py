from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction, Bid, Comment
from .forms import AuctionForm, BidForm, CommentForm

categories = [category[1] for category in Auction.CATEGORIES]

def index(request):
    return render(request, "auctions/index.html", {'categories': categories,})

@login_required
def create_auction(request):
    if request.method == "POST":
        auction_form = AuctionForm(request.POST)
        if auction_form.is_valid():
            auction = auction_form.save(commit=False)
            auction.creator = request.user
            auction.save()
            return render(request, "auctions/create-auction.html", {
                            'form': auction_form,
                            'message': "New Auction Created!",})
        else:
            return render(request, "auctions/create-auction.html", {
                            'form': auction_form,
                            'message': "Error in creating auction",})
    else:
        auction_form = AuctionForm()
        return render(request, "auctions/create-auction.html", {
                                'form': auction_form,
                                'categories': categories,})

def view_an_auction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    bids = Bid.objects.filter(auction=auction)
    comments = Comment.objects.filter(auction=auction)
    comment_form = CommentForm(request.POST)
    bid_form = BidForm(request.POST, auction_id=auction_id)
    return render(request, "auctions/auction.html", {
                        'auction': auction,
                        'comment_form': comment_form,
                        'bid_form': bid_form,
                        'bids': bids,
                        'comments': comments,
                        'categories': categories,})

class AuctionListView(ListView):
    model = Auction
    template_name = "auctions/index.html"
    context_object_name = 'auctions'
    extra_context = {'categories': categories,}


def list_categories(request):
    return render(request, "auctions/list-categories.html", {'categories': categories})

def show_categories(request, category):
    auction = Auction.objects.filter(category=category)
    return render(request, "auctions/index.html", {
                            'category_name': category,
                            'auctions': auction,
                            'categories': categories,})

@require_http_methods(["POST"])
@login_required
def add_watchlist(request):
    current_user = User.objects.get(username=request.user.username)
    auction = Auction.objects.get(id=request.POST["auction_id"])
    current_user.watched_list.add(auction)
    return redirect(f"/view-auction/{auction.id}", )

@login_required
def view_watchlist(request, user_id):
    watchlist = User.objects.get(id=user_id).watched_list.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@require_http_methods(["POST"])
@login_required
def bid_auction(request):
    auction = Auction.objects.get(id=request.POST["auction_id"])
    bids = Bid.objects.filter(auction=auction)
    comments = Comment.objects.filter(auction=auction)
    comment_form = CommentForm(request.POST)
    bid_form = BidForm(request.POST, auction_id=auction.id)
    if bid_form.is_valid():
        bid = bid_form.save(commit=False)
        bid.user = request.user
        bid.auction = auction
        bid.save()
        auction.close_price = request.POST["bid_price"]
        auction.save()
        return redirect(f"/view-auction/{auction.id}", )
    else:
        return render(request, "auctions/auction.html", {
                                'auction': auction,
                                'comment_form': comment_form,
                                'bid_form': bid_form,
                                'bids': bids,
                                'comments': comments,
                                'message': "Unsuccessful bid",
                                'categories': categories,})

@require_http_methods(["POST"])
@login_required
def add_comment(request):
    auction = Auction.objects.get(id=request.POST["auction_id"])
    bids = Bid.objects.filter(auction=auction)
    comments = Comment.objects.filter(auction=auction)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.auction = auction
        comment.save()
        return redirect(f"/view-auction/{auction.id}", )
    else:
        return render(request, "auctions/auction.html", {
                        'auction': auction,
                        'comment_form': bid_form,
                        'bids': bids,
                        'comments': comments,
                        'message': 'Unsuccessful commenting',
                        'categories': categories,})

@require_http_methods(["POST"])
@login_required
def close_auction(request):
    auction = Auction.objects.get(id=request.POST["auction_id"])
    if auction.open_status:
        auction.open_status = False
        if auction.close_price:
            bids = Bid.objects.filter(auction=auction)
            auction.winner = bids.get(bid_price=auction.close_price).user
        auction.save()
        return redirect(f"/view-auction/{auction.id}", )
    else:
        return render(request, "auctions/auction.html", {
                            'auction': auction,
                            'message': f"The auction is already closed with price of ${auction.close_price}!"})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                'categories': categories,
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                'categories': categories,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                'categories': categories,
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
                                'categories': categories,
                                })
