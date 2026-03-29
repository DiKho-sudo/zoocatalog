"""
Упрощенная команда импорта ВСЕХ данных из файла остаток_цена.xlsx
Использование: python manage.py import_simple остаток_цена.xlsx
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from products.models import Product, Category, Brand, AnimalType
import openpyxl
from decimal import Decimal


class Command(BaseCommand):
    help = 'Простой импорт товаров из файла с остатками и ценами'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к файлу остаток_цена.xlsx')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Обновлять существующие товары'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить все товары перед импортом'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        update_existing = options['update']
        clear_all = options['clear']

        if clear_all:
            count = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Удалено товаров: {count}'))

        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
        except Exception as e:
            raise CommandError(f'Ошибка при чтении файла: {e}')

        self.stdout.write(self.style.SUCCESS(f'Начинаем импорт из {file_path}'))

        # Получаем дефолтные объекты
        default_category = self._get_or_create_default_category()
        default_animal_type = self._get_or_create_default_animal_type()

        # Статистика
        created = 0
        updated = 0
        skipped = 0
        errors = 0

        # Начинаем читать с 11-й строки (товары)
        for row_num, row in enumerate(sheet.iter_rows(min_row=11, values_only=True), start=11):
            try:
                # Пропускаем пустые строки
                if not row[0]:
                    continue

                # Извлекаем данные
                name_raw = str(row[0]).strip()
                
                # Пропускаем строки с итогами или названиями складов
                if len(name_raw) < 5 or 'магазин' in name_raw.lower() or name_raw.count('ЧУП') > 0:
                    skipped += 1
                    continue

                # Извлекаем остаток и цену
                stock = row[5] if len(row) > 5 else 0
                price = row[7] if len(row) > 7 else 0

                # Пропускаем если нет цены
                if not price or float(price) == 0:
                    skipped += 1
                    continue

                # Обрабатываем название товара
                name, unit = self._parse_name_and_unit(name_raw)
                
                if not name or len(name) < 3:
                    skipped += 1
                    continue

                # Извлекаем бренд из названия
                brand = self._extract_brand(name)

                # Определяем статус наличия
                stock_status = 'in_stock' if stock and float(stock) > 0 else 'out_of_stock'

                # Создаем slug
                slug = slugify(name)[:200]
                base_slug = slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    if not update_existing:
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    else:
                        break

                # Ищем существующий товар
                existing = Product.objects.filter(slug=slug).first()

                if existing and update_existing:
                    # Обновляем
                    existing.name = name
                    existing.price = Decimal(str(price))
                    existing.stock_status = stock_status
                    existing.unit = unit
                    existing.brand = brand
                    existing.save()
                    updated += 1
                    
                    if updated <= 10:
                        self.stdout.write(self.style.SUCCESS(
                            f'Обновлен: "{name[:50]}..." | {price} BYN'
                        ))
                elif not existing:
                    # Создаем новый
                    product = Product.objects.create(
                        name=name,
                        slug=slug,
                        description='',
                        composition='',
                        weight=1.0,
                        unit=unit,
                        price=Decimal(str(price)),
                        category=default_category,
                        brand=brand,
                        animal_type=default_animal_type,
                        stock_status=stock_status,
                        age_group='all'
                    )
                    created += 1
                    
                    if created <= 10:
                        self.stdout.write(self.style.SUCCESS(
                            f'Создан: "{name[:50]}..." | {price} BYN | {stock_status}'
                        ))
                else:
                    skipped += 1

            except Exception as e:
                errors += 1
                if errors <= 5:
                    self.stdout.write(self.style.ERROR(
                        f'Ошибка в строке {row_num}: {e}'
                    ))

        # Итоги
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('ИТОГИ ИМПОРТА:'))
        self.stdout.write(self.style.SUCCESS(f'Создано новых товаров: {created}'))
        self.stdout.write(self.style.SUCCESS(f'Обновлено товаров: {updated}'))
        if skipped > 0:
            self.stdout.write(self.style.WARNING(f'Пропущено строк: {skipped}'))
        if errors > 0:
            self.stdout.write(self.style.ERROR(f'Ошибок: {errors}'))
        self.stdout.write(self.style.SUCCESS('='*60))

    def _parse_name_and_unit(self, name_raw):
        """Извлекает название и единицу измерения"""
        name = name_raw.strip()
        unit = 'шт'
        
        # Убираем лишние пробелы в начале (отступы из иерархии)
        name = ' '.join(name.split())
        
        # Извлекаем единицу измерения
        if ', шт' in name:
            name = name.replace(', шт', '')
            unit = 'шт'
        elif ', кг' in name:
            name = name.replace(', кг', '')
            unit = 'кг'
        elif ', г' in name:
            name = name.replace(', г', '')
            unit = 'г'
        elif ', л' in name:
            name = name.replace(', л', '')
            unit = 'л'
        elif ', мл' in name:
            name = name.replace(', мл', '')
            unit = 'мл'
        
        return name, unit

    def _extract_brand(self, name):
        """Пытается извлечь бренд из названия товара"""
        # Список известных брендов
        known_brands = [
            'ECOLINE', 'Royal Canin', 'Whiskas', 'TRIXIE', 'GAMMA',
            'FLEXI', 'LINGDOK', 'MIGLIORI', 'Papa&Mama', 'Tetra',
            'GreenZORIN', 'MORANDO', 'SIRIUS', 'ACANA', 'ZOLUX',
            '8in1', 'Doctor VIC', 'ALL CATS', 'AMERTЕК'
        ]
        
        name_upper = name.upper()
        
        for brand_name in known_brands:
            if brand_name.upper() in name_upper:
                brand, _ = Brand.objects.get_or_create(
                    name=brand_name,
                    defaults={'country': 'Беларусь'}
                )
                return brand
        
        # Если не нашли - создаем "Неизвестный"
        brand, _ = Brand.objects.get_or_create(
            name='Неизвестный производитель',
            defaults={'country': 'Беларусь'}
        )
        return brand

    def _get_or_create_default_category(self):
        """Создает дефолтную категорию"""
        category, _ = Category.objects.get_or_create(
            slug='roznichnye-tovary',
            defaults={
                'name': 'Розничные товары',
                'description': 'Товары из каталога зоомагазина'
            }
        )
        return category

    def _get_or_create_default_animal_type(self):
        """Создает дефолтный тип животного"""
        animal_type, _ = AnimalType.objects.get_or_create(
            slug='vse',
            defaults={'name': 'Все животные'}
        )
        return animal_type

