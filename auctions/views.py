from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction
from .forms import AuctionForm

def index(request):
    return render(request, "auctions/list-auctions.html")

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
        return render(request, "auctions/create-auction.html", {'form': auction_form})

def view_an_auction(request, auction_name):
    auction = Auction.objects.get(auction_name=auction_name)
    return render(request, "auctions/auction.html", {'auction': auction})

class AuctionListView(ListView):
    model = Auction
    template_name = "auctions/list-auctions.html"
    context_object_name = 'auctions'

def list_categories(request):
    categories = [category[1] for category in Auction.CATEGORIES]
    return render(request, "auctions/list-categories.html", {'categories': categories})

def show_categories(request, category):
    auction = Auction.objects.filter(category=category)
    return render(request, "auctions/list-auctions.html", {
                            'category_name': category,
                            'auctions': auction,})
@login_required
def view_watchlist(request):
    pass

@login_required
def bid_auction(request):
    pass

@require_http_methods(["POST"])
@login_required
def add_watchlist(request):
    current_user = User.objects.get(name=request.user.name)
    auction = Auction.objects.get(auction_name=request.POST["auction_name"])
    current_user.watched_list.add(auction)
    return HttpResponseRedirect(reverse(f"viewauction/{request.POST['auction_name']}"))

@login_required
def close_auction(request):
    pass


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
                "message": "Invalid username and/or password."
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
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
