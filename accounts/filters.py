import django_filters
from .models import *
from django_filters import DateFilter


class OrderFilter(django_filters.FilterSet):
    start_created = DateFilter(field_name='date_created', lookup_expr='gte')
    end_created = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = Order
        fields = '__all__'
