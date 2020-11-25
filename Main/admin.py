from django.contrib import admin
from .models import Movie
from .models import Review
from .models import Order
from .models import OrderItem
from .models import ShippingAddress

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("movie", "quantity","get_total")
    list_filter = ('date_added',)


    


# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)

