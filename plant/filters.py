from .models import Plant
import django_filters


class PlantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='')

    class Meta:
        model = Plant
        fields = {
            # 'name':['icontains'],
        }
