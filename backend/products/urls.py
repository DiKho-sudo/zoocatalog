from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalTypeViewSet, BrandViewSet, CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'animal-types', AnimalTypeViewSet, basename='animal-type')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]



