from rest_framework import serializers
from .models import AnimalType, Brand, Category, Product, ProductImage


class AnimalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalType
        fields = ['id', 'name', 'slug', 'icon']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'description', 'logo', 'website']


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'parent_name', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров (краткая информация)"""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    animal_type_name = serializers.CharField(source='animal_type.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'image', 'price', 'weight', 'unit',
            'brand_name', 'category_name', 'animal_type_name',
            'age_group', 'stock_status', 'is_hypoallergenic', 'is_grain_free',
            'view_count'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о товаре"""
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    animal_type = AnimalTypeSerializer(read_only=True)
    additional_images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'composition',
            'weight', 'unit', 'price', 'brand', 'category', 'animal_type',
            'age_group', 'is_hypoallergenic', 'is_grain_free',
            'image', 'additional_images', 'stock_status',
            'view_count', 'created_at', 'updated_at'
        ]



