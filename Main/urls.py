from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "main"

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('details/<int:id>/', views.detail, name="detail"),
    path('addmovies/', views.add_movies, name="add_movies"),
    path('editmovies/<int:id>/', views.edit_movies, name="edit_movies"),
    path('deletemovies/<int:id>/', views.delete_movies, name="delete_movie"),
    path('addreview/<int:id>/', views.add_review, name="add_review"),
    path('editreview/<int:movie_id>/<int:review_id>/', views.edit_review, name="edit_review"),
    path('deletereview/<int:movie_id>/<int:review_id>/', views.delete_review, name="delete_review"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('addcategories/', views.add_category, name="add_category"),
    path('deletecategories/<int:id>/', views.delete_category, name="delete_category"),


    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
