from django.contrib import admin
from .models import AnimalType, Brand, Category, Product, ProductImage


@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'website']
    search_fields = ['name', 'country']  # Для autocomplete
    list_filter = ['country']
    
    # Поля для редактирования
    fields = ['name', 'country', 'description', 'logo', 'website']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['parent', 'created_at']
    raw_id_fields = ['parent']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'brand_country', 'category', 'animal_type', 'weight_with_unit', 'price', 'stock_status', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'composition', 'brand__name', 'brand__country']
    list_filter = ['category', 'brand', 'brand__country', 'animal_type', 'age_group', 'stock_status', 'is_hypoallergenic', 'is_grain_free', 'unit']
    raw_id_fields = ['category', 'animal_type']  # Убрали brand из raw_id_fields
    list_per_page = 20
    inlines = [ProductImageInline]
    
    # Автозаполнение для выбора производителя
    autocomplete_fields = ['brand']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Характеристики', {
            'fields': ('composition', 'weight', 'unit', 'price', 'age_group')
        }),
        ('Классификация', {
            'fields': ('category', 'brand', 'animal_type')
        }),
        ('Особые свойства', {
            'fields': ('is_hypoallergenic', 'is_grain_free', 'stock_status')
        }),
    )
    
    def weight_with_unit(self, obj):
        return f"{obj.weight} {obj.unit}"
    weight_with_unit.short_description = 'Вес/Количество'
    
    def brand_country(self, obj):
        return obj.brand.country if obj.brand else '-'
    brand_country.short_description = 'Страна'
    brand_country.admin_order_field = 'brand__country'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'order']
    list_filter = ['product']
    search_fields = ['product__name', 'alt_text']
