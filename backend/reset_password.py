"""
Скрипт для сброса пароля пользователя
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zoo_catalog.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# НАСТРОЙКИ: Измените под себя
USERNAME = 'admin'  # Имя пользователя
NEW_PASSWORD = 'admin123'  # Новый пароль

try:
    user = User.objects.get(username=USERNAME)
    user.set_password(NEW_PASSWORD)
    user.save()
    
    print(f'\n✅ Пароль успешно изменён!')
    print(f'   Пользователь: {USERNAME}')
    print(f'   Новый пароль: {NEW_PASSWORD}')
    print(f'\n🔐 Войти в админку: http://localhost:8000/admin/')
    print(f'   Username: {USERNAME}')
    print(f'   Password: {NEW_PASSWORD}')
    print(f'\n⚠️  ВАЖНО: Смените пароль после входа!\n')
    
except User.DoesNotExist:
    print(f'\n❌ Пользователь "{USERNAME}" не найден!')
    print(f'   Доступные пользователи:')
    for u in User.objects.filter(is_superuser=True):
        print(f'   - {u.username}')


