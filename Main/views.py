from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from Accounts.models import Profile
from .forms import *
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.db.models.functions import Length
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import json
import datetime

from .filters import MovieFilter

# Create your views here.
def home (request) :   
    allmovies_list = Movie.objects.all() # select * from movie
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        item = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    myFilter = MovieFilter(request.GET, queryset=allmovies_list)
    allmovies_list = myFilter.qs  
    paginator = Paginator(allmovies_list, 3)
    page = request.GET.get('page')
    try:
        allmovies = paginator.page(page)
    except PageNotAnInteger:
        allmovies = paginator.page(1)
    except EmptyPage:
        allmovies = paginator.page(paginator.num_page)
    

    context = {
        "movies" : allmovies ,
        'myFilter' : myFilter,
        'cartItems':cartItems
    }
    return render(request, 'main/index.html',context)

# detail page
def detail(request, id):
    movie = Movie.objects.get(id=id) # select * from movie where id=id
    reviews = Review.objects.filter(movie=id).order_by("-comment")

    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average, 2)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        item = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    


    context = {
        "movie": movie,
        "reviews": reviews,
        "average": average,
        'cartItems':cartItems,
        
    
    }
    return render(request, 'main/details.html', context)

# add movies to the database
def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = MovieForm(request.POST or None)

                # check if the form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    messages.success(request,f'Added a new Movie Successfully!')
                    return redirect("main:home")
            else:
                form = MovieForm()

            return render(request, 'main/addmovies.html',{"form": form, "controller": "Add Movies"})
        
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login")   


def add_category(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = CategoryForm(request.POST or None)

                # check if the form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    messages.success(request,f'Added a new Category Successfully!')
                    return redirect("main:home")
            else:
                form = CategoryForm()

            categories=Category.objects.all()
            return render(request, 'main/addcategory.html',{"form": form,"categories":categories, "controller": "Add Category"})
        
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login")     


# edit the movie
def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the movies linked with id
            movie = Movie.objects.get(id=id)

            # form check
            if request.method == "POST":
                form = MovieForm(request.POST or None, instance=movie)
                # check if form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()

                    messages.info(request,f'The Movie has been Updated!')
                    return redirect("main:detail", id)
            else:
                form = MovieForm(instance=movie)

            return render(request, 'main/addmovies.html', {"form": form, "controller": "Edit Movies"})
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login") 


# delete movies
def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the moveis
            movie = Movie.objects.get(id=id)

            # delte the movie
            movie.delete()
            messages.info(request,f'The Movie has been Deleted!')
            return redirect("main:home")
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login")

def delete_category(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the moveis
            cat = Category.objects.get(id=id)

            # delte the movie
            cat.delete()
            messages.info(request,f'The Category has been Deleted!')
            return redirect("main:home")
        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not loggedin
    return redirect("accounts:login")


def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                if request.POST["comment"]:
                    data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                messages.success(request,f'Added a Review Successfully!')
                return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {"form": form})
    else:
        return redirect("accounts:login")

# edit the review
def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        # review
        review = Review.objects.get(movie=movie, id=review_id)

        # check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 5) or (data.rating < 0):
                         error = "Out or range. Please select rating from 0 to 5."
                         return render(request, 'main/editreview.html', {"error": error, "form": form})
                    else:
                        data.save()
                        messages.info(request,f'The Review has been Updated!')
                        return redirect("main:detail", movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form": form})
        else:
            return redirect("main:detail", movie_id)
    else:
        return redirect("accounts:login")

# delete reivew
def delete_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        # review
        review = Review.objects.get(movie=movie, id=review_id)

        # check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission to delete
            review.delete()
            messages.info(request,f'The Review has been Deleted!')

        return redirect("main:detail", movie_id)
            
    else:
        return redirect("accounts:login")


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        context = {
        "items": items ,
        "order": order,
        'cartItems':cartItems
      }   
    return render(request, 'main/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {
        "items": items ,
        "order": order ,
        'cartItems':cartItems
        }
    return render(request, 'main/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	movieId = data['movieId']
	action = data['action']
	print('Action:', action)
	print('movie:', movieId)

	customer = request.user
	movie = Movie.objects.get(id=movieId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, movie=movie)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)








