import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """Фильтры для товаров"""
    
    # Фильтр по диапазону цен
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Фильтр по производителю (множественный выбор)
    brand = django_filters.NumberFilter(field_name='brand__id')
    
    # Фильтр по категории (включая подкатегории)
    category = django_filters.NumberFilter(field_name='category__id')
    
    # Фильтр по типу животного
    animal_type = django_filters.NumberFilter(field_name='animal_type__id')
    
    # Фильтр по возрастной группе
    age_group = django_filters.ChoiceFilter(choices=Product.AGE_CHOICES)
    
    # Булевые фильтры
    is_hypoallergenic = django_filters.BooleanFilter()
    is_grain_free = django_filters.BooleanFilter()
    
    # Фильтр по статусу наличия
    stock_status = django_filters.ChoiceFilter(choices=Product.STOCK_CHOICES)
    
    class Meta:
        model = Product
        fields = [
            'price_min', 'price_max', 'brand', 'category',
            'animal_type', 'age_group', 'is_hypoallergenic',
            'is_grain_free', 'stock_status'
        ]



