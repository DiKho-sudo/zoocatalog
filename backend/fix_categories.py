import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zoo_catalog.settings')
django.setup()

from products.models import Category, AnimalType

print("Создание категорий...\n")

# Создаем категории
categories_data = [
    # (название, slug, parent_slug)
    ('Корма', 'korma', None),
    ('Сухие корма', 'suhie-korma', 'korma'),
    ('Влажные корма', 'vlazhnye-korma', 'korma'),
    ('Консервы', 'konservy', 'korma'),
    ('Лакомства', 'lakomstva', 'korma'),
    
    ('Миски и посуда', 'miski-i-posuda', None),
    ('Миски', 'miski', 'miski-i-posuda'),
    ('Кормушки', 'kormushki', 'miski-i-posuda'),
    ('Поилки', 'poilki', 'miski-i-posuda'),
    ('Контейнеры', 'kontejnery', 'miski-i-posuda'),
    
    ('Туалеты и гигиена', 'tualety-i-gigiena', None),
    ('Туалеты', 'tualety', 'tualety-i-gigiena'),
    ('Лотки', 'lotki', 'tualety-i-gigiena'),
    ('Наполнители', 'napolniteli', 'tualety-i-gigiena'),
    ('Совки', 'sovki', 'tualety-i-gigiena'),
    
    ('Игрушки', 'igrushki', None),
    ('Мягкие игрушки', 'mjagkie-igrushki', 'igrushki'),
    ('Мячики', 'mjachiki', 'igrushki'),
    ('Когтеточки', 'kogteto chki', 'igrushki'),
    
    ('Уход и красота', 'uhod-i-krasota', None),
    ('Шампуни', 'shampuni', 'uhod-i-krasota'),
    ('Расчески', 'rascheski', 'uhod-i-krasota'),
    
    ('Амуниция', 'amunicija', None),
    ('Ошейники', 'oshejniki', 'amunicija'),
    ('Поводки', 'povodki', 'amunicija'),
    ('Рулетки', 'ruletki', 'amunicija'),
]

created_cats = {}

# Сначала создаем родительские
for name, slug, parent_slug in categories_data:
    if parent_slug is None:
        cat = Category.objects.create(name=name, slug=slug)
        created_cats[slug] = cat
        print(f"+ {name}")

# Затем дочерние
for name, slug, parent_slug in categories_data:
    if parent_slug is not None:
        parent = created_cats.get(parent_slug)
        if parent:
            cat = Category.objects.create(name=name, slug=slug, parent=parent)
            created_cats[slug] = cat
            print(f"  - {name}")

print(f"\nВсего создано: {Category.objects.count()} категорий")

# Создаем типы животных
animals = [
    ('Кошки', 'koshki'),
    ('Собаки', 'sobaki'),
    ('Грызуны', 'gryzuny'),
    ('Птицы', 'ptitsy'),
    ('Рыбы', 'ryby'),
]

for name, slug in animals:
    AnimalType.objects.get_or_create(slug=slug, defaults={'name': name})

print(f"Типов животных: {AnimalType.objects.count()}")
print("\nГотово!")

