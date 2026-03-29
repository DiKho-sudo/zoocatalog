#!/bin/bash

# Устанавливаем права на директории media и static
chmod -R 777 /app/media /app/staticfiles 2>/dev/null || true

# Создаем поддиректории если их нет
mkdir -p /app/media/products /app/media/brands /app/media/categories /app/media/animal_types 2>/dev/null || true

# Устанавливаем права снова
chmod -R 777 /app/media /app/staticfiles 2>/dev/null || true

echo "Media directories ready!"

# Запускаем переданную команду
exec "$@"

