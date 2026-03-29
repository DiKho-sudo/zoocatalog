from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Case, When, IntegerField, Value, Count
from .models import AnimalType, Brand, Category, Product, ProductView
from .serializers import (
    AnimalTypeSerializer, BrandSerializer, CategorySerializer,
    ProductListSerializer, ProductDetailSerializer
)
from .filters import ProductFilter


class AnimalTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer
    lookup_field = 'slug'


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name']
    ordering = ['name']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


def _get_session_id(request):
    return request.headers.get('X-Session-ID', '')


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related(
        'brand', 'category', 'animal_type'
    ).prefetch_related('additional_images')

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'composition']
    ordering_fields = ['price', 'created_at', 'name', 'view_count']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    # POST /api/products/{slug}/track-view/
    @action(detail=True, methods=['post'], url_path='track-view')
    def track_view(self, request, slug=None):
        product = self.get_object()
        Product.objects.filter(pk=product.pk).update(view_count=F('view_count') + 1)

        sid = _get_session_id(request)
        if sid:
            ProductView.objects.create(session_id=sid, product=product)

        return Response({'status': 'ok'})

    # GET /api/products/{slug}/similar/
    @action(detail=True, methods=['get'], url_path='similar')
    def similar(self, request, slug=None):
        product = self.get_object()
        price = float(product.price)
        price_lo, price_hi = price * 0.5, price * 2.0

        annotations = (
            Value(0, output_field=IntegerField())
            + Case(When(category=product.category, then=Value(3)),
                   default=Value(0), output_field=IntegerField())
            + Case(When(animal_type=product.animal_type, then=Value(2)),
                   default=Value(0), output_field=IntegerField())
            + Case(When(brand=product.brand, then=Value(1)),
                   default=Value(0), output_field=IntegerField())
            + Case(When(price__gte=price_lo, price__lte=price_hi, then=Value(1)),
                   default=Value(0), output_field=IntegerField())
        )

        if product.is_hypoallergenic:
            annotations = annotations + Case(
                When(is_hypoallergenic=True, then=Value(2)),
                default=Value(0), output_field=IntegerField())

        if product.is_grain_free:
            annotations = annotations + Case(
                When(is_grain_free=True, then=Value(2)),
                default=Value(0), output_field=IntegerField())

        qs = Product.objects.select_related('brand', 'category', 'animal_type') \
            .exclude(pk=product.pk) \
            .filter(stock_status='in_stock') \
            .annotate(score=annotations) \
            .filter(score__gt=0) \
            .order_by('-score', '-view_count')[:8]

        serializer = ProductListSerializer(qs, many=True)
        return Response(serializer.data)

    # GET /api/products/popular/
    @action(detail=False, methods=['get'], url_path='popular')
    def popular(self, request):
        qs = Product.objects.select_related('brand', 'category', 'animal_type') \
            .filter(stock_status='in_stock') \
            .order_by('-view_count', '-created_at')[:8]
        serializer = ProductListSerializer(qs, many=True)
        return Response(serializer.data)

    # GET /api/products/recommended/
    @action(detail=False, methods=['get'], url_path='recommended')
    def recommended(self, request):
        sid = _get_session_id(request)
        if not sid:
            return Response([])

        recent_views = ProductView.objects.filter(session_id=sid) \
            .select_related('product') \
            .order_by('-viewed_at')[:30]

        if not recent_views:
            return Response([])

        viewed_ids = set()
        cat_counts = {}
        animal_counts = {}
        brand_counts = {}
        has_hypo = False
        has_gf = False

        for pv in recent_views:
            p = pv.product
            viewed_ids.add(p.pk)
            cat_counts[p.category_id] = cat_counts.get(p.category_id, 0) + 1
            animal_counts[p.animal_type_id] = animal_counts.get(p.animal_type_id, 0) + 1
            brand_counts[p.brand_id] = brand_counts.get(p.brand_id, 0) + 1
            if p.is_hypoallergenic:
                has_hypo = True
            if p.is_grain_free:
                has_gf = True

        top_cats = sorted(cat_counts, key=cat_counts.get, reverse=True)[:3]
        top_animals = sorted(animal_counts, key=animal_counts.get, reverse=True)[:2]
        top_brands = sorted(brand_counts, key=brand_counts.get, reverse=True)[:3]

        annotations = (
            Value(0, output_field=IntegerField())
            + Case(When(category_id__in=top_cats, then=Value(3)),
                   default=Value(0), output_field=IntegerField())
            + Case(When(animal_type_id__in=top_animals, then=Value(2)),
                   default=Value(0), output_field=IntegerField())
            + Case(When(brand_id__in=top_brands, then=Value(1)),
                   default=Value(0), output_field=IntegerField())
        )

        if has_hypo:
            annotations = annotations + Case(
                When(is_hypoallergenic=True, then=Value(2)),
                default=Value(0), output_field=IntegerField())
        if has_gf:
            annotations = annotations + Case(
                When(is_grain_free=True, then=Value(2)),
                default=Value(0), output_field=IntegerField())

        qs = Product.objects.select_related('brand', 'category', 'animal_type') \
            .exclude(pk__in=viewed_ids) \
            .filter(stock_status='in_stock') \
            .annotate(score=annotations) \
            .filter(score__gt=0) \
            .order_by('-score', '-view_count')[:8]

        serializer = ProductListSerializer(qs, many=True)
        return Response(serializer.data)
