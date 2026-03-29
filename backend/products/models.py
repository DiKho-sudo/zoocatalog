from django.db import models
from django.utils.text import slugify
import os
import uuid
from datetime import datetime


def upload_to_products(instance, filename):
    """Генерирует безопасное имя файла для изображений товаров"""
    ext = filename.split('.')[-1]
    # Используем slug товара + timestamp + расширение
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f"{instance.slug}_{timestamp}.{ext}"
    return f'products/{safe_filename}'


def upload_to_brands(instance, filename):
    """Генерирует безопасное имя файла для логотипов брендов"""
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f"{slugify(instance.name)}_{timestamp}.{ext}"
    return f'brands/{safe_filename}'


def upload_to_categories(instance, filename):
    """Генерирует безопасное имя файла для изображений категорий"""
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f"{instance.slug}_{timestamp}.{ext}"
    return f'categories/{safe_filename}'


def upload_to_animal_types(instance, filename):
    """Генерирует безопасное имя файла для иконок типов животных"""
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f"{instance.slug}_{timestamp}.{ext}"
    return f'animal_types/{safe_filename}'


def upload_to_product_gallery(instance, filename):
    """Генерирует безопасное имя файла для галереи товара"""
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = f"{instance.product.slug}_{unique_id}_{timestamp}.{ext}"
    return f'products/gallery/{safe_filename}'


class AnimalType(models.Model):
    """Тип животного (собака, кошка, грызун и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    icon = models.ImageField(upload_to=upload_to_animal_types, blank=True, null=True, verbose_name="Иконка")
    
    class Meta:
        verbose_name = "Тип животного"
        verbose_name_plural = "Типы животных"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """Производитель товаров"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    description = models.TextField(blank=True, verbose_name="Описание")
    logo = models.ImageField(upload_to=upload_to_brands, blank=True, null=True, verbose_name="Логотип")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория товаров с поддержкой иерархии"""
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name="Родительская категория"
    )
    image = models.ImageField(upload_to=upload_to_categories, blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Товар в каталоге"""
    
    AGE_CHOICES = [
        ('puppy', 'Щенок/Котенок'),
        ('adult', 'Взрослый'),
        ('senior', 'Пожилой'),
        ('all', 'Все возрасты'),
    ]
    
    STOCK_CHOICES = [
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии'),
        ('pre_order', 'Под заказ'),
    ]
    
    name = models.CharField(max_length=300, verbose_name="Название")
    slug = models.SlugField(max_length=300, unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    composition = models.TextField(blank=True, verbose_name="Состав")
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        help_text="Вес или количество",
        verbose_name="Вес/Количество"
    )
    unit = models.CharField(
        max_length=20,
        default='шт',
        help_text="Единица измерения (шт, кг, г, л и т.д.)",
        verbose_name="Единица измерения"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена (BYN)"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Производитель"
    )
    animal_type = models.ForeignKey(
        AnimalType,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Тип животного"
    )
    
    age_group = models.CharField(
        max_length=20,
        choices=AGE_CHOICES,
        default='all',
        verbose_name="Возрастная группа"
    )
    
    # Особые характеристики
    is_hypoallergenic = models.BooleanField(default=False, verbose_name="Гипоаллергенный")
    is_grain_free = models.BooleanField(default=False, verbose_name="Беззерновой")
    
    image = models.ImageField(upload_to=upload_to_products, verbose_name="Основное изображение")
    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_CHOICES,
        default='in_stock',
        verbose_name="Статус наличия"
    )
    
    view_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'animal_type']),
            models.Index(fields=['price']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductView(models.Model):
    """История просмотров товаров (анонимные сессии)"""
    session_id = models.CharField(max_length=64, db_index=True, verbose_name="ID сессии")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='views', verbose_name="Товар"
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        verbose_name = "Просмотр товара"
        verbose_name_plural = "Просмотры товаров"
        indexes = [
            models.Index(fields=['session_id', '-viewed_at']),
        ]

    def __str__(self):
        return f"{self.session_id[:8]}… → {self.product.name[:40]}"


class ProductImage(models.Model):
    """Дополнительные изображения товара"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="Товар"
    )
    image = models.ImageField(upload_to=upload_to_product_gallery, verbose_name="Изображение")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ['order']
    
    def __str__(self):
        return f"Изображение для {self.product.name}"
