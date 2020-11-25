from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Length
from PIL import Image


# Create your models here.

class Category(models.Model):
	title=models.CharField(max_length=200)
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title


# Create your models here.
class Movie(models.Model):
    # fields for the movie table
 
    name = models.CharField(max_length=300)
    director = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    price = models.FloatField(null=True)
    cast = models.CharField(max_length=800)
    description = models.TextField(max_length=5000)
    release_date = models.DateField()
    averageRating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)
    digital = models.BooleanField(default=False,null=True, blank=True)


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000,null=True,blank=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class Order(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.movie.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.movie.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
