# admin.py

from django.contrib import admin
from .models import AuctionListing, Comment, Bid

@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'current_bid', 'active', 'owner')
    list_filter = ('active', 'category')
    search_fields = ('title', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'commenter')
    search_fields = ('listing__title', 'commenter__username')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'bid_amount', 'bid_time')
    search_fields = ('listing__title', 'bidder__username')
