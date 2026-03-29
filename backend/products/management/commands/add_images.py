"""
Команда для добавления изображений к товарам
Использование: python manage.py add_images путь/к/папке/с/картинками
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from products.models import Product
from pathlib import Path


class Command(BaseCommand):
    help = 'Добавление изображений к товарам по названию файла или артикулу'

    def add_arguments(self, parser):
        parser.add_argument('images_dir', type=str, help='Папка с изображениями')
        parser.add_argument(
            '--by-name',
            action='store_true',
            help='Искать товары по названию (вместо артикула)'
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Заменять существующие изображения'
        )

    def handle(self, *args, **options):
        images_dir = options['images_dir']
        by_name = options['by_name']
        overwrite = options['overwrite']

        images_path = Path(images_dir)
        if not images_path.exists():
            raise CommandError(f'Папка не найдена: {images_dir}')

        self.stdout.write(self.style.SUCCESS(f'Сканируем папку: {images_dir}'))

        # Поддерживаемые форматы
        extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        
        # Находим все изображения
        image_files = []
        for ext in extensions:
            image_files.extend(images_path.glob(f'*{ext}'))
            image_files.extend(images_path.glob(f'*{ext.upper()}'))

        if not image_files:
            self.stdout.write(self.style.WARNING('Изображения не найдены!'))
            return

        self.stdout.write(f'Найдено изображений: {len(image_files)}')

        # Статистика
        added_count = 0
        updated_count = 0
        skipped_count = 0
        not_found_count = 0

        for image_file in image_files:
            try:
                # Получаем имя файла без расширения
                file_name = image_file.stem
                
                # Ищем товар
                product = None
                
                if by_name:
                    # Поиск по названию
                    product = Product.objects.filter(
                        name__icontains=file_name
                    ).first()
                else:
                    # Поиск по артикулу в slug
                    from django.utils.text import slugify
                    slug = slugify(file_name)
                    product = Product.objects.filter(slug=slug).first()
                    
                    # Если не нашли по slug, попробуем по названию
                    if not product:
                        product = Product.objects.filter(
                            name__icontains=file_name
                        ).first()

                if not product:
                    not_found_count += 1
                    self.stdout.write(self.style.WARNING(
                        f'❌ Товар не найден для: {file_name}'
                    ))
                    continue

                # Проверяем есть ли уже изображение
                if product.image and not overwrite:
                    skipped_count += 1
                    self.stdout.write(
                        f'⏭️  Пропущен "{product.name}" (изображение уже есть)'
                    )
                    continue

                # Загружаем изображение
                with open(image_file, 'rb') as f:
                    product.image.save(
                        image_file.name,
                        File(f),
                        save=True
                    )

                if overwrite and product.image:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'🔄 Обновлено: "{product.name}" ← {image_file.name}'
                    ))
                else:
                    added_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ Добавлено: "{product.name}" ← {image_file.name}'
                    ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'❌ Ошибка с файлом {image_file.name}: {e}'
                ))

        # Итоги
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('ИТОГИ:'))
        self.stdout.write(self.style.SUCCESS(f'✅ Добавлено изображений: {added_count}'))
        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f'🔄 Обновлено изображений: {updated_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⏭️  Пропущено (уже есть): {skipped_count}'))
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(f'❌ Товары не найдены: {not_found_count}'))
        self.stdout.write(self.style.SUCCESS('='*50))

