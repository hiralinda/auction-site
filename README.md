# Auction Site

This is a Django-based auction site created as part of the CS50 Web Programming with Python and JavaScript course's [Projects](https://cs50.harvard.edu/web/2020/projects/2/commerce/), that allows users to create and bid on auction listings, add items to a watchlist, and leave comments. The site supports user authentication and features an admin interface for managing listings, bids, and comments. Tailwind CSS is used for styling the frontend.

## Video Preview

[Video Link](https://youtu.be/UMwwRYbdUAY)

## Features

- **User Authentication**: Users can register, log in, and log out. Different content is displayed depending on whether the user is signed in.
- **Create Listing**: Users can create new auction listings with a title, description, starting bid, optional image, and category.
- **Active Listings Page**: Displays all active auction listings, including title, description, current price, and image (if provided).
- **Listing Page**: Each listing has a dedicated page showing all details, including current bids, comments, and options to add to a watchlist, place a bid, or close the auction.
- **Watchlist**: Signed-in users can add listings to their watchlist and view all items in their watchlist on a dedicated page.
- **Bidding**: Users can place bids on active listings. The bid must be higher than the current bid and meet the starting bid criteria.
- **Auction Closing**: The creator of a listing can close the auction, declaring the highest bidder as the winner.
- **Comments**: Users can add comments to each listing, and all comments are displayed on the listing page.
- **Categories**: Users can view and filter listings by category.
- **Django Admin Interface**: Administrators can manage listings, bids, and comments via the Django admin panel.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/hiralinda/auction-site.git
    cd auction-site
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the site**:
    - Visit `http://127.0.0.1:8000/` in your browser.
    - Access the admin panel at `http://127.0.0.1:8000/admin/`.

## Models

- **User**: Inherits from Django’s `AbstractUser`, representing users of the application.
- **Listing**: Represents an auction listing, with fields for title, description, starting bid, image URL, and category.
- **Bid**: Represents a bid placed on a listing, associated with a user and a listing.
- **Comment**: Represents a comment made on a listing, associated with a user and a listing.

## Future Improvements

- **Email Notifications**: Notify users via email when they are outbid or when an auction they are watching is about to end.
- **Bid History**: Show a history of all bids placed on a listing, allowing users to see the bidding progression.
- **Advanced Search and Filters**: Implement search functionality with filters such as price range, category, and auction end date.
- **User Profiles**: Allow users to view and manage their bids, watchlist, and created listings from a dedicated profile page.
- **Auction Countdown Timer**: Display a live countdown timer on listing pages to indicate when the auction will end.
- **Buy Now Option**: Add a "Buy Now" feature that allows users to purchase an item immediately at a set price, bypassing the auction process.
- **Rating and Reviews**: Allow users to rate and review sellers after an auction is completed.
- **Social Sharing**: Add options to share listings on social media platforms to attract more bidders.

---

*[This project](https://cs50.harvard.edu/web/2020/projects/2/commerce/) is a part of the CS50 Web Programming with Python and JavaScript course.*

