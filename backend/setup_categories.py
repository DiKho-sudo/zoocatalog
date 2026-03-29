"""
Скрипт для создания категорий
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zoo_catalog.settings')
django.setup()

from products.models import Category, AnimalType
from django.utils.text import slugify

print("Очистка старых категорий...")
Category.objects.all().delete()
print("Категории удалены")

print("\nСоздание типов животных...")
animals = [
    ('Кошки', 'koshki'),
    ('Собаки', 'sobaki'),
    ('Грызуны', 'gryzuny'),
    ('Птицы', 'ptitsy'),
    ('Рыбы', 'ryby'),
    ('Рептилии', 'reptilii'),
]

for name, slug in animals:
    AnimalType.objects.get_or_create(slug=slug, defaults={'name': name})
    print(f"  - {name}")

print(f"\nВсего типов животных: {AnimalType.objects.count()}")

print("\nСоздание категорий...")

# Структура категорий
categories = {
    'Корма': [
        'Сухие корма',
        'Влажные корма',
        'Консервы',
        'Лакомства',
        'Витамины и добавки',
    ],
    'Миски и посуда': [
        'Миски',
        'Кормушки',
        'Поилки',
        'Контейнеры',
        'Коврики под миски',
    ],
    'Туалеты и гигиена': [
        'Туалеты',
        'Лотки',
        'Наполнители',
        'Совки',
        'Пакеты',
        'Пеленки',
    ],
    'Игрушки': [
        'Мягкие игрушки',
        'Интерактивные',
        'Мячики',
        'Когтеточки',
        'Дразнилки',
    ],
    'Уход и красота': [
        'Шампуни',
        'Расчески и щетки',
        'Ножницы',
        'Средства по уходу',
    ],
    'Амуниция': [
        'Ошейники',
        'Поводки',
        'Рулетки',
        'Шлейки',
        'Намордники',
    ],
    'Переноски и домики': [
        'Переноски',
        'Домики',
        'Лежанки',
        'Будки',
    ],
    'Аквариумистика': [
        'Аквариумы',
        'Фильтры',
        'Корма для рыб',
        'Декор',
    ],
}

created_total = 0

for parent_name, children in categories.items():
    # Родительская категория
    slug = slugify(parent_name)
    try:
        parent = Category.objects.get(slug=slug)
        print(f"\n{parent_name} (уже существует)")
    except Category.DoesNotExist:
        parent = Category.objects.create(
            name=parent_name,
            slug=slug
        )
        created_total += 1
        print(f"\n{parent_name} (создан)")
    
    # Подкатегории
    for child_name in children:
        child_slug = slugify(child_name)
        try:
            child = Category.objects.get(slug=child_slug)
            print(f"  - {child_name} (уже есть)")
        except Category.DoesNotExist:
            child = Category.objects.create(
                name=child_name,
                slug=child_slug,
                parent=parent
            )
            created_total += 1
            print(f"  - {child_name} (создан)")

print(f"\n\nВсего создано: {created_total}")
print(f"Всего категорий в базе: {Category.objects.count()}")

