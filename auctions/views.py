from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import AuctionListing, Bid, Comment, User
from .forms import AuctionListingForm, BidForm, CommentForm


from .models import User


def index(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')

    if order == 'asc':
        listings_list = AuctionListing.objects.filter(active=True).order_by(sort_by)
    else:
        listings_list = AuctionListing.objects.filter(active=True).order_by(f'-{sort_by}')

    paginator = Paginator(listings_list, 9)  # Show 9 listings per page
    page = request.GET.get('page')

    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    return render(request, 'auctions/index.html', {
        'listings': listings,
        'sort_by': sort_by,
        'order': order,
    })


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

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('index')  # Redirect to the index page or the listing detail page
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    is_watchlisted = request.user.is_authenticated and request.user.watchlist.filter(pk=listing_id).exists()
    highest_bid = listing.bids.order_by('-bid_amount').first()

    bid_form = BidForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'bid' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_amount = bid_form.cleaned_data['bid_amount']
                if bid_amount <= max(listing.starting_bid, highest_bid.bid_amount if highest_bid else 0):
                    messages.error(request, 'Your bid must be higher than the current bid and at least as large as the starting bid.')
                else:
                    new_bid = bid_form.save(commit=False)
                    new_bid.listing = listing
                    new_bid.bidder = request.user
                    new_bid.save()
                    listing.current_bid = bid_amount
                    listing.save()
                    messages.success(request, 'Your bid was placed successfully.')
                    return redirect('listing', listing_id=listing_id)
        elif 'comment' in request.POST:
            print("Comment form submitted")  # Debug print
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                print("Comment form is valid")  # Debug print
                new_comment = comment_form.save(commit=False)
                new_comment.listing = listing
                new_comment.commenter = request.user
                new_comment.save()
                print("Comment saved")  # Debug print
                messages.success(request, 'Your comment was added successfully.')
                return redirect('listing', listing_id=listing_id)
            else:
                print("Comment form errors:", comment_form.errors)  # Debug print
        elif 'close_auction' in request.POST and request.user == listing.owner:
            if listing.active:
                highest_bid = listing.bids.order_by('-bid_amount').first()
                if highest_bid:
                    listing.winner = highest_bid.bidder
                    listing.current_bid = highest_bid.bid_amount
                    messages.success(request, f'The auction was closed successfully. Winner: {listing.winner.username}')
                else:
                    messages.info(request, 'The auction was closed. No bids were placed.')
                
                listing.active = False
                listing.save()
            else:
                messages.warning(request, 'This auction is already closed.')
            
            return redirect('listing', listing_id=listing_id)
        elif 'watchlist' in request.POST:
            if is_watchlisted:
                request.user.watchlist.remove(listing)
                messages.success(request, 'The listing was removed from your watchlist.')
            else:
                request.user.watchlist.add(listing)
                messages.success(request, 'The listing was added to your watchlist.')
            return redirect('listing', listing_id=listing_id)
        else:
            messages.error(request, 'Invalid action.')
            return redirect('listing', listing_id=listing_id)

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'comments': comments,
        'bid_form': bid_form,
        'comment_form': comment_form,
        'is_watchlisted': is_watchlisted,
        'highest_bid': highest_bid,
    })
@login_required
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})

def categories(request):
    categories = AuctionListing.CATEGORY_CHOICES
    return render(request, 'auctions/categories.html', {'categories': categories})

def category_listings(request, category_name):
    listings = AuctionListing.objects.filter(category=category_name, active=True)
    return render(request, 'auctions/category_listings.html', {'category_name': category_name, 'listings': listings})

def my_listings(request):
    user_listings = AuctionListing.objects.filter(owner=request.user)
    return render(request, 'auctions/my_listings.html', {
        'listings': user_listings
    })

def closed_listings(request):
    closed_listings = AuctionListing.objects.filter(active=False).order_by('-created_at')
    
    paginator = Paginator(closed_listings, 9)  # Show 9 listings per page
    page = request.GET.get('page')
    
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listings = paginator.page(paginator.num_pages)
    
    return render(request, 'auctions/closed_listings.html', {'listings': listings})
