"""
Команда для обновления цен товаров из Excel файла
Использование: python manage.py update_prices путь/к/файлу.xlsx
"""

from django.core.management.base import BaseCommand, CommandError
from products.models import Product
import openpyxl
from decimal import Decimal


class Command(BaseCommand):
    help = 'Обновление цен товаров из Excel файла'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к Excel файлу с ценами')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет обновлено (без изменений)'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        dry_run = options['dry_run']

        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
        except Exception as e:
            raise CommandError(f'Ошибка при чтении файла: {e}')

        if dry_run:
            self.stdout.write(self.style.WARNING('РЕЖИМ ПРЕДПРОСМОТРА (изменения не будут сохранены)'))

        # Получаем заголовки
        headers = [cell.value for cell in sheet[1]]
        self.stdout.write(f'Колонки: {headers}')

        # Находим индексы нужных колонок
        name_idx = None
        price_idx = None

        for idx, header in enumerate(headers):
            if not header:
                continue
            h = str(header).lower()
            if 'наименование' in h or 'название' in h:
                name_idx = idx
            elif 'цена' in h or 'price' in h:
                price_idx = idx

        if name_idx is None:
            raise CommandError('Не найдена колонка "Наименование"')
        if price_idx is None:
            raise CommandError('Не найдена колонка "Цена"')

        self.stdout.write(f'Колонка названия: {headers[name_idx]}')
        self.stdout.write(f'Колонка цены: {headers[price_idx]}')

        updated_count = 0
        not_found_count = 0
        skipped_count = 0

        # Обрабатываем строки
        for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            try:
                if name_idx >= len(row) or price_idx >= len(row):
                    continue

                name = row[name_idx]
                price = row[price_idx]

                if not name or not price:
                    skipped_count += 1
                    continue

                # Парсим цену
                try:
                    if isinstance(price, str):
                        price = price.replace(',', '.')
                    price_decimal = Decimal(str(price))
                except:
                    self.stdout.write(self.style.WARNING(
                        f'Строка {row_num}: Неверный формат цены "{price}"'
                    ))
                    skipped_count += 1
                    continue

                # Ищем товар
                product = Product.objects.filter(name__iexact=name).first()
                
                if not product:
                    # Пробуем частичное совпадение
                    product = Product.objects.filter(name__icontains=name).first()

                if not product:
                    not_found_count += 1
                    self.stdout.write(self.style.WARNING(
                        f'❌ Товар не найден: "{name}"'
                    ))
                    continue

                # Обновляем цену
                old_price = product.price
                
                if not dry_run:
                    product.price = price_decimal
                    product.save(update_fields=['price'])

                updated_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'[OK] "{product.name}": {old_price} -> {price_decimal} BYN'
                ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Ошибка в строке {row_num}: {e}'
                ))

        # Итоги
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        if dry_run:
            self.stdout.write(self.style.WARNING('ПРЕДПРОСМОТР (изменения НЕ сохранены)'))
        else:
            self.stdout.write(self.style.SUCCESS('ОБНОВЛЕНИЕ ЗАВЕРШЕНО'))
        self.stdout.write(self.style.SUCCESS(f'✅ Обновлено цен: {updated_count}'))
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(f'❌ Товары не найдены: {not_found_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⏭️  Пропущено строк: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS('='*50))

