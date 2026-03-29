# 🐘 Настройка PostgreSQL - Пошаговая инструкция

## 📋 Что вам нужно сделать:

### 1. Создайте базу данных в pgAdmin (2 минуты)

**Откройте pgAdmin:**
1. Запустите pgAdmin 4
2. В левой панели: **Servers** → **PostgreSQL 15** (или ваша версия)
3. Введите пароль postgres (который устанавливали)

**Создайте базу:**
1. Правой кнопкой на **"Databases"**
2. **Create** → **Database...**
3. Заполните:
   - **Database**: `zoo_catalog`
   - **Owner**: `postgres`
   - **Encoding**: `UTF8`
4. Нажмите **Save**

✅ База `zoo_catalog` создана!

---

### 2. Создайте файл .env (1 минута)

В папке **`backend/`** создайте файл `.env` (точка в начале!)

**Содержимое файла .env:**

```env
# Django Settings
SECRET_KEY=django-insecure-2dvnx3+*0fui)q(+46)ejl7alhm$mepp3(snof6%t*dq_xj-sq
DEBUG=True

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=zoo_catalog
DB_USER=postgres
DB_PASSWORD=ВАШ_ПАРОЛЬ_POSTGRES
DB_HOST=localhost
DB_PORT=5432
```

⚠️ **Замените `ВАШ_ПАРОЛЬ_POSTGRES`** на реальный пароль от PostgreSQL!

---

### 3. Установите драйвер PostgreSQL (30 секунд)

```bash
cd backend
pip install psycopg2-binary
```

---

### 4. Примените миграции (1 минута)

```bash
python manage.py migrate
```

Вы увидите:
```
Applying contenttypes.0001_initial... OK
Applying auth.0001_initial... OK
Applying products.0001_initial... OK
Applying products.0002_product_unit_alter_product_weight... OK
...
```

✅ Структура базы данных создана!

---

### 5. Создайте суперпользователя (30 секунд)

```bash
python manage.py createsuperuser
```

Введите:
- **Username**: `admin`
- **Email**: (можно пропустить - Enter)
- **Password**: `admin123` (или свой)
- **Password (again)**: `admin123`

---

### 6. Создайте категории (10 секунд)

```bash
python fix_categories.py
```

Результат:
```
Всего создано: 26 категорий
Типов животных: 7
```

---

### 7. Импортируйте товары из 1С (1 минута)

```bash
python manage.py import_simple ..\stock_price.xlsx
```

Результат:
```
Создано товаров: 1874
```

---

### 8. Запустите сервер

```bash
python manage.py runserver
```

Откройте:
- **Админка**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/products/
- **Сайт**: http://localhost:3000/catalog

---

## ✅ Готово!

Теперь ваш сайт работает с **PostgreSQL** и содержит:
- 🗄️ 1874 товара из 1С
- 📂 26 категорий
- 🐾 7 типов животных
- 💰 Актуальные цены
- 📦 Статусы наличия

---

## 🔍 Проверка в pgAdmin:

1. Откройте pgAdmin
2. **zoo_catalog** → **Schemas** → **public** → **Tables**
3. Правой кнопкой на **products_product** → **View/Edit Data** → **All Rows**
4. Должны увидеть все 1874 товара!

---

## 🔄 Регулярное обновление:

### Каждый день/неделю:

1. Выгрузите новый отчет из 1С → `stock_price.xlsx`
2. Запустите:
   ```bash
   python manage.py import_simple ..\stock_price.xlsx --update
   ```

Это обновит цены и остатки без удаления товаров!

---

## 📊 Команды для работы:

```bash
# Импорт товаров (первый раз)
python manage.py import_simple ..\stock_price.xlsx

# Обновление (регулярно)
python manage.py import_simple ..\stock_price.xlsx --update

# Проверка подключения к PostgreSQL
python manage.py dbshell

# Бэкап базы (через pgAdmin)
# Правой кнопкой на zoo_catalog → Backup...

# Просмотр товаров
# http://localhost:8000/admin/products/product/
```

---

## 💡 Преимущества PostgreSQL для вашего проекта:

1. **Производительность**
   - Быстрый поиск по 1874 товарам
   - Эффективная фильтрация
   - Оптимизированные индексы

2. **Надежность**
   - ACID транзакции
   - Безопасность данных
   - Бэкапы через pgAdmin

3. **Для курсовой**
   - Использование профессиональной СУБД
   - Можно написать о преимуществах PostgreSQL
   - Покажет серьезный подход

---

**Начните с Шага 1 прямо сейчас!** 🎯

