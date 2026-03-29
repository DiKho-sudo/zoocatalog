"""
Скрипт для создания суперпользователя Django
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zoo_catalog.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Параметры суперпользователя
USERNAME = 'admin'
EMAIL = 'admin@zoo.local'
PASSWORD = 'admin123'  # Измените на безопасный пароль!

# Проверяем, существует ли пользователь
if User.objects.filter(username=USERNAME).exists():
    print(f'✅ Суперпользователь "{USERNAME}" уже существует!')
    user = User.objects.get(username=USERNAME)
    print(f'   Email: {user.email}')
    print(f'   Активен: {user.is_active}')
    print(f'   Суперпользователь: {user.is_superuser}')
else:
    # Создаем суперпользователя
    user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f'✅ Суперпользователь создан!')
    print(f'   Username: {USERNAME}')
    print(f'   Email: {EMAIL}')
    print(f'   Password: {PASSWORD}')
    print(f'\n🔐 Войти в админку: http://localhost:8000/admin/')
    print(f'   ВАЖНО: Смените пароль после первого входа!')


