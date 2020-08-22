from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionListView.as_view(), name="viewauction"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("createauction/", views.create_auction, name="createauction"),
    path("viewauction/<str:auction_name>", views.view_an_auction, name="viewanauction"),
    path("listcategories/", views.list_categories, name="listcategories"),
    path("category/<str:category>", views.show_categories, name="showcategory"),
    path("viewwatchlist/", views.view_watchlist, name="viewwatchlist"),
    path("addwatchlist/", views.add_watchlist, name="addwatchlist"),
    path("bid_auction/", views.bid_auction, name="bid_auction"),
]
