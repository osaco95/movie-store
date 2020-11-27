import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class MovieFilter(django_filters.FilterSet):
    
	name =  CharFilter(field_name='name', lookup_expr='icontains' )
	director = CharFilter(field_name='director', lookup_expr='icontains')
	cast = CharFilter(field_name='cast', lookup_expr='icontains')


    

	class Meta:
		model = Movie
		fields = '__all__'
		exclude = ['description', 'release_date', 'averageRating','image','price','digital']
		
	



			