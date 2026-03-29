# Настройка PostgreSQL для проекта

## Установка PostgreSQL

### Windows
1. Скачайте PostgreSQL с https://www.postgresql.org/download/windows/
2. Запустите установщик
3. Запомните пароль для пользователя postgres
4. Порт по умолчанию: 5432

### Создание базы данных

1. Откройте pgAdmin (устанавливается вместе с PostgreSQL)
2. Подключитесь к серверу (введите пароль postgres)
3. Правой кнопкой на "Databases" → "Create" → "Database"
4. Имя базы: `zoo_catalog`
5. Owner: `postgres`
6. Нажмите "Save"

**ИЛИ через командную строку:**

```bash
# Войти в консоль PostgreSQL
psql -U postgres

# Создать базу данных
CREATE DATABASE zoo_catalog;

# Выйти
\q
```

## Настройка Django для PostgreSQL

1. Установите драйвер PostgreSQL:
```bash
cd backend
pip install psycopg2-binary
```

2. Создайте файл `.env` в папке `backend/`:
```bash
copy .env.example .env
```

3. Откройте `.env` и настройте:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=zoo_catalog
DB_USER=postgres
DB_PASSWORD=ваш_пароль_postgres
DB_HOST=localhost
DB_PORT=5432
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

## Переключение обратно на SQLite

Если нужно вернуться к SQLite, просто в `.env` измените:
```
DB_ENGINE=django.db.backends.sqlite3
```

## Проверка подключения

Запустите Django и проверьте:
```bash
python manage.py dbshell
```

Должна открыться консоль PostgreSQL.

## Преимущества PostgreSQL

✅ Более производительный для большого каталога
✅ Лучший полнотекстовый поиск
✅ Поддержка JSON полей
✅ Подходит для продакшн
✅ Поддержка транзакций

