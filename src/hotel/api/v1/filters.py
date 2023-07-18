from django_filters import rest_framework as filters


class HotelFilterSet(filters.FilterSet):
    country = filters.CharFilter('location__country', lookup_expr='iexact')
    city = filters.CharFilter('location__city', lookup_expr='iexact')

    checkin_date = filters.DateFilter('rooms__reservations__end_date',
                                      lookup_expr='lte', exclude=True)

    checkout_date = filters.DateFilter('rooms__reservations__start_date',
                                       lookup_expr='gte', exclude=True)
