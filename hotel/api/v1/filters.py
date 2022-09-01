from django.db.models import Q
from django_filters import rest_framework as filters


class HotelFilterSet(filters.FilterSet):
    country = filters.CharFilter('location__country', lookup_expr='iexact')
    city = filters.CharFilter('location__city', lookup_expr='iexact')
    check_in_date = filters.DateFilter(method='reserved_date')

    @staticmethod
    def reserved_date(queryset, name, value):
        print(queryset)
        print(value)
        #
        return queryset.exclude(Q(
            Q(rooms__reservations__start_date__lt=value) &
            Q(rooms__reservations__end_date__gt=value)
        )
                               )
