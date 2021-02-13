from django_filters import FilterSet, CharFilter

from .models import Application

# FilterSet - осуществляет поиск по полям
class ApplicationFilter(FilterSet):
    phone = CharFilter(label='Телефон клиента', field_name='phone', lookup_expr='icontains')
    comment= CharFilter(label='Комментарий к решению', field_name='comment', lookup_expr='icontains')

    class Meta:
        model = Application
        fields = ('product', 'solution')