from django.urls import path

from . import views

urlpatterns = [
    path("", views.AuctionListView.as_view(), name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create-auction/", views.create_auction, name="create-auction"),
    path("view-auction/<int:auction_id>", views.view_an_auction, name="view-auction"),
    path("list-categories/", views.list_categories, name="list-categories"),
    path("category/<str:category>", views.show_categories, name="show-category"),
    path("view-watchlist/<int:user_id>", views.view_watchlist, name="view-watchlist"),
    path("close-auction/", views.close_auction, name="close-auction"),
    path("add-watchlist/", views.add_watchlist, name="add-watchlist"),
    path("bid-auction/", views.bid_auction, name="bid-auction"),
    path("add-comment/", views.add_comment, name="add-comment"),
]
