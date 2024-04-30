from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model
from .managers import CustomUserManager
from .models import Product
import random
from .models import Review, has_in_cart, Receipt
from django.db.models import Avg
from django.http import HttpResponseNotFound
from .forms import ProductForm
from django.utils import timezone
from django.db.models import Q


def product(request, product_id):
    # Retrieve the product object using the product ID
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        return HttpResponseNotFound("Product does not exist")

    # Pass the product object to the template
    return render(request, 'pages/product.html', {'product': product})


def home(request):
    random_products = Product.objects.order_by('?')[:15]
    print(random_products)
    context = {
        'random_products': random_products
    }
    return render(request, 'pages/home.html', context)

def profile(request, seller_id):
    # Calculate average rating for the current user
    User = get_user_model()
    try:
        seller = User.objects.get(id=seller_id)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        # For example, return a 404 page
        return HttpResponseNotFound("User does not exist")

    # Now you have the 'seller' object, you can pass it to the template


    average_rating = Review.objects.filter(receive_user=seller).aggregate(Avg('rating_number'))['rating_number__avg']

    user_products = Product.objects.filter(seller=seller)
    
    user_reviews = Review.objects.filter(receive_user=seller)
    # Pass the average rating to the template
    return render(request, 'pages/profile.html', {'user_products': user_products, 'user_reviews': user_reviews, 'average_rating': average_rating, 'seller':seller})

def textbooks(request):
    textbook_products = Product.objects.filter(category='textbooks')
    for product in textbook_products:
        print(product.p_image)
    context = {
        'textbook_products': textbook_products
    }
    return render(request, 'pages/textbooks.html', context)

def electronics(request):
    electronic_products = Product.objects.filter(category='electronics')
    context = {
        'electronic_products': electronic_products
    }
    return render(request, 'pages/electronics.html', context)

def login(request):
    return render(request, 'pages/login.html')

def signup(request):
    return render(request, 'pages/signup.html')

def housing(request):
    housing_products = Product.objects.filter(category='housing')
    context = {
        'housing_products': housing_products
    }
    return render(request, 'pages/housing.html', context)

def fashion(request):
    fashion_products = Product.objects.filter(category='fashion')
    context = {
        'fashion_products': fashion_products
    }
    return render(request, 'pages/fashion.html', context)

def stationary(request):
    stationary_products = Product.objects.filter(category='stationary')
    context = {
        'stationary_products': stationary_products
    }
    return render(request, 'pages/stationary.html', context)

def collectibles(request):
    collectible_products = Product.objects.filter(category='collectibles')
    context = {
        'collectible_products': collectible_products
    }
    return render(request, 'pages/collectibles.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Assuming your login form has a field named 'username'
        password = request.POST.get('password')  # Assuming your login form has a field named 'password'

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # User is authenticated, log them in
            auth_login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'pages/login.html')


def signup_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not email.endswith("@clarku.edu"):
            messages.error(request, 'Must use a Clark email address.')
            return redirect('signup')

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('signup')
        if User.objects.filter(clark_email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email address.')
            return redirect('signup')

        user_manager = CustomUserManager()
        new_user = user_manager.create_user(
            username=username,
            clark_email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'pages/signup.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the profile page after adding the product
            return redirect('profile', seller_id=request.user.id)
    else:
        form = ProductForm()
    return render(request, 'pages/add_product.html', {'form': form})


from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages

def submit_product(request):
    if request.method == 'POST':
        # Retrieve form data
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        while True:
            random_id = random.randint(100000, 999999)  # Generate a random 6-digit ID
            if not Product.objects.filter(product_id=random_id).exists():
                break

        # Create a new Product object
        new_product = Product(
            product_id = random_id,
            p_name=product_name,
            p_description=description,
            price=price,
            p_image=image,
            seller=request.user,
            category=category
        )

        # Save the new product to the database
        new_product.save()

        # Display a success message
        messages.success(request, 'Product added successfully!')

        # Redirect the user to the profile page
        return redirect('profile', seller_id=request.user.id)

    # If the request method is not POST, render the add product page
    return render(request, 'pages/add_product.html')


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    # Check if the user is the seller of the product
    if request.user == product.seller:
        # If the user is the seller, redirect them to an error page or show an error message
        return redirect('home')  # Redirect to home page for now
    else:
        # Check if the item is already in the cart
        if has_in_cart.objects.filter(user_id=request.user, p_id=product).exists():
            # Increment quantity if the item is already in the cart
            cart_item = has_in_cart.objects.get(user_id=request.user, p_id=product)
            cart_item.save()
        else:
            # Add the item to the cart
            has_in_cart.objects.create(user_id=request.user, p_id=product)
    return redirect('cart')

def cart(request):
    # Retrieve all items in the user's cart
    cart_items = has_in_cart.objects.filter(user_id=request.user)
    return render(request, 'pages/cart.html', {'cart_items': cart_items})

def delete_product(request, product_id):
    # Retrieve the product object
    product = get_object_or_404(Product, product_id=product_id)
    
    # Check if the user is the seller of the product
    if request.user == product.seller:
        # Delete the product
        product.delete()
        # Redirect to the profile page
        return redirect('profile', seller_id=request.user.id)
    else:
        # If the user is not authorized to delete the product, you can redirect them to an error page or show an error message
        return redirect('home')  # Redirect to home page for now

def checkout(request):
    if request.method == 'POST':
        # Get the user's cart items
        cart_items = has_in_cart.objects.all()
        
        # Create a list to store the names of products bought
        products_bought = []
        sellers = []

        # Calculate total price
        total_price = 0

        # Process each cart item
        for cart_item in cart_items:
            # Add the product name to the list of products bought
            sellers.append(cart_item.p_id.seller.clark_email)
            products_bought.append(cart_item.p_id.p_name)
            # Calculate total price
            total_price += cart_item.p_id.price

            # Delete the cart item from the database
            cart_item.p_id.delete()

        while True:
            random_id = random.randint(100000, 999999)  # Generate a random 6-digit ID
            if not Receipt.objects.filter(receipt_id=random_id).exists():
                break

        # Save the receipt to the database
        receipt = Receipt.objects.create(
            receipt_id = random_id,
            user_id=request.user,
            date=timezone.now(),
            products_bought=', '.join(products_bought),
            total_price=total_price
        )
        return render(request, 'pages/thank_you.html', {'sellers' : sellers})
    return render(request, 'pages/cart.html')


def orders(request):
    old_receipts = Receipt.objects.filter(user_id = request.user)
        # Redirect to the profile page after adding the product
    return render(request, 'pages/orders.html', {'old_receipts': old_receipts})

def thank_you(request):
    return render(request, 'pages/thank_you.html')

def search(request):
    # Get the search query from the form
    query = request.GET.get('q')
    # Perform the search operation
    results = Product.objects.filter(Q(p_name__icontains=query) | Q(p_description__icontains=query))
    # Pass the search results to the template
    return render(request, 'pages/search_results.html', {'results': results, 'query': query})

def search_results(request):
    return render(request, 'pages/search_results.html')

from .forms import ReviewForm

def add_review(request, seller_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating_number = form.cleaned_data['rating_number']
            review_description = form.cleaned_data['review_description']

            while True:
                random_id = random.randint(100000, 999999)  # Generate a random 6-digit ID
                if not Review.objects.filter(review_id=random_id).exists():
                    break
            # Create and save the review
            Review.objects.create(
                review_id = random_id,
                send_user=request.user,
                receive_user_id=seller_id,
                rating_number=rating_number,
                r_description=review_description
            )
            # Redirect to the profile page
            return redirect('profile', seller_id=seller_id)
    else:
        form = ReviewForm()
    return render(request, 'pages/add_review.html', {'form': form})


def remove_from_cart(request, product_id):
    # Get the product object
    product = get_object_or_404(Product, product_id=product_id)
    
    # Check if the item is in the user's cart
    if has_in_cart.objects.filter(user_id=request.user, p_id=product).exists():
        # Delete the item from the cart
        cart_item = has_in_cart.objects.get(user_id=request.user, p_id=product)
        cart_item.delete()

    return redirect('cart')