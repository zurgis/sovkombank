from django_filters import FilterSet, CharFilter

from .models import Application


class ApplicationFilter(FilterSet):
    phone = CharFilter(field_name='phone', lookup_expr='icontains')
    comment= CharFilter(field_name='comment', lookup_expr='icontains')

    class Meta:
        model = Application
        fields = ('product', 'solution')