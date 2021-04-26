from django_filters import rest_framework as filters

from yamdb.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilter(filters.FilterSet):
    """Filtering creative works."""
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )
    genre = CharFilterInFilter(
        field_name='genre__slug',
        lookup_expr='in'
    )
    name = filters.CharFilter(
        lookup_expr='icontains'
    )
    year = filters.NumberFilter()

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
