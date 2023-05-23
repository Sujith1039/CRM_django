import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    startDate = DateFilter(field_name="date_created", lookup_expr='gte')
    endDate = DateFilter(field_name="date_created", lookup_expr='lte')
    notes = CharFilter(field_name="notes", lookup_expr='icontains')
    class Meta:
        model =  Orders
        fields = '__all__'
        exclude = ['date_created']