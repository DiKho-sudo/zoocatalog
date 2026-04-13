#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py fix_known_data_issues

# Загрузка данных из фикстуры (только если БД пустая)
python manage.py shell -c "
from products.models import Product
if Product.objects.count() == 0:
    import subprocess
    subprocess.run(['python', 'manage.py', 'loaddata', 'fixtures.json'], check=True)
    subprocess.run(['python', 'manage.py', 'fix_known_data_issues'], check=True)
    print('Fixtures loaded successfully')
else:
    print(f'Database already has {Product.objects.count()} products, skipping fixture load')
"
