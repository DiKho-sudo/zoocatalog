"""
Команда для создания структуры категорий как на garfield.by
"""

from django.core.management.base import BaseCommand
from products.models import Category, AnimalType


class Command(BaseCommand):
    help = 'Создание структуры категорий по типам животных'

    def handle(self, *args, **options):
        self.stdout.write('Создание категорий...')
        
        # Создаем типы животных
        cat_type, _ = AnimalType.objects.get_or_create(
            slug='koshki',
            defaults={'name': 'Кошки'}
        )
        dog_type, _ = AnimalType.objects.get_or_create(
            slug='sobaki',
            defaults={'name': 'Собаки'}
        )
        rodent_type, _ = AnimalType.objects.get_or_create(
            slug='gryzuny',
            defaults={'name': 'Грызуны'}
        )
        bird_type, _ = AnimalType.objects.get_or_create(
            slug='ptitsy',
            defaults={'name': 'Птицы'}
        )
        fish_type, _ = AnimalType.objects.get_or_create(
            slug='ryby',
            defaults={'name': 'Рыбы'}
        )
        
        self.stdout.write(f'Создано типов животных: 5')
        
        # Структура категорий
        categories_structure = {
            'Корма': [
                'Сухие корма',
                'Влажные корма',
                'Консервы',
                'Лакомства',
            ],
            'Миски и аксессуары': [
                'Миски',
                'Кормушки',
                'Поилки',
                'Контейнеры для корма',
            ],
            'Туалеты и наполнители': [
                'Туалеты',
                'Лотки',
                'Наполнители',
                'Совки',
                'Пакеты для уборки',
            ],
            'Игрушки': [
                'Интерактивные игрушки',
                'Мягкие игрушки',
                'Мячики',
                'Когтеточки',
            ],
            'Уход и гигиена': [
                'Шампуни',
                'Расчески',
                'Щетки',
                'Средства гигиены',
            ],
            'Амуниция': [
                'Ошейники',
                'Поводки',
                'Рулетки',
                'Шлейки',
            ],
            'Аквариумистика': [
                'Аквариумы',
                'Фильтры',
                'Компрессоры',
                'Декор',
            ],
        }
        
        created_count = 0
        
        for parent_name, subcategories in categories_structure.items():
            # Создаем родительскую категорию
            parent, created = Category.objects.get_or_create(
                slug=self._slugify(parent_name),
                defaults={'name': parent_name}
            )
            if created:
                created_count += 1
                self.stdout.write(f'Создана категория: {parent_name}')
            
            # Создаем подкатегории
            for subcat_name in subcategories:
                subcat, created = Category.objects.get_or_create(
                    slug=self._slugify(subcat_name),
                    defaults={
                        'name': subcat_name,
                        'parent': parent
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(f'  → {subcat_name}')
        
        # Показываем итоги
        total_categories = Category.objects.count()
        total_animals = AnimalType.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'\nСоздано новых категорий: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Всего категорий в базе: {total_categories}'))
        self.stdout.write(self.style.SUCCESS(f'Всего типов животных: {total_animals}'))
        
        # Показываем структуру
        self.stdout.write('\nСтруктура категорий:')
        parents = Category.objects.filter(parent__isnull=True)
        for parent in parents:
            self.stdout.write(f'  {parent.name}')
            children = Category.objects.filter(parent=parent)
            for child in children:
                self.stdout.write(f'    - {child.name}')
    
    def _slugify(self, text):
        from django.utils.text import slugify
        return slugify(text)
