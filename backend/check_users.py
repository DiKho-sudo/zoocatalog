"""
Скрипт для проверки суперпользователей в БД
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zoo_catalog.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print('\n' + '='*50)
print('Суперпользователи в базе данных:')
print('='*50)

superusers = User.objects.filter(is_superuser=True)

if superusers.exists():
    for user in superusers:
        print(f'\nUsername: {user.username}')
        print(f'Email: {user.email}')
        print(f'Активен: {user.is_active}')
        print(f'Staff: {user.is_staff}')
        print(f'Superuser: {user.is_superuser}')
        print(f'Дата создания: {user.date_joined}')
else:
    print('\n[!] Суперпользователи не найдены!')
    print('    Создайте суперпользователя:')
    print('    python manage.py createsuperuser')

print('\n' + '='*50)
print(f'Всего пользователей: {User.objects.count()}')
print(f'Суперпользователей: {superusers.count()}')
print('='*50 + '\n')


