# Инструкция по первому запуску проекта

## Быстрый старт

### Шаг 1: Запуск Backend (Django)

1. Откройте терминал и перейдите в папку backend:

```bash
cd backend
```

2. Установите зависимости (если еще не установлены):

```bash
python -m pip install Django djangorestframework django-cors-headers django-filter Pillow
```

3. Примените миграции базы данных:

```bash
python manage.py migrate
```

4. Создайте суперпользователя для доступа к админ-панели:

```bash
python manage.py createsuperuser
```

Введите имя пользователя, email (необязательно) и пароль.

5. Запустите сервер:

```bash
python manage.py runserver
```

✅ Backend запущен! Откройте http://localhost:8000/admin/ для доступа к админ-панели.

### Шаг 2: Добавление тестовых данных

1. Откройте браузер и перейдите на http://localhost:8000/admin/
2. Войдите используя созданные учетные данные
3. Добавьте данные в следующем порядке:

**Типы животных** (Animal types):

- Собаки (slug: sobaki)
- Кошки (slug: koshki)
- Грызуны (slug: gryzuny)
- Птицы (slug: ptitsy)

**Производители** (Brands):

- Royal Canin (Страна: Франция)
- Whiskas (Страна: США)
- Pedigree (Страна: США)
- Felix (Страна: Великобритания)

**Категории** (Categories):

- Корма (slug: korma)
- Сухой корм (slug: suhoj-korm, родитель: Корма)
- Влажный корм (slug: vlazhnyj-korm, родитель: Корма)
- Аксессуары (slug: aksessuary)
- Игрушки (slug: igrushki)

**Товары** (Products):
Добавьте несколько товаров с заполнением всех полей:

- Название, описание, состав
- Вес (например, 1.5)
- Цена (например, 25.90)
- Выберите категорию, производителя, тип животного
- Загрузите изображение
- Выберите возрастную группу
- Отметьте специальные характеристики если нужно

### Шаг 3: Запуск Frontend (React)

1. Откройте **НОВЫЙ** терминал (не закрывайте терминал с Django!)
2. Перейдите в папку frontend:

```bash
cd frontend
```

3. Установите зависимости:

```bash
npm install
```

Это может занять несколько минут при первом запуске.

4. Запустите React приложение:

```bash
npm start
```

✅ Frontend запущен! Браузер автоматически откроется на http://localhost:3000

## Проверка работы

После запуска обеих частей проверьте:

1. **Главная страница** (http://localhost:3000):

   - Должен отображаться приветственный баннер
   - Категории товаров (если добавлены)
   - Новые товары (если добавлены)
2. **Каталог** (http://localhost:3000/catalog):

   - Панель фильтров слева
   - Сетка товаров справа
   - Работа поиска в шапке сайта
3. **Детали товара**:

   - Кликните на любую карточку товара
   - Должна открыться страница с полной информацией
4. **API** (http://localhost:8000/api/):

   - products/ - список товаров
   - categories/ - категории
   - brands/ - производители
   - animal-types/ - типы животных

## Что делать если что-то не работает?

### Backend не запускается

```bash
# Убедитесь что вы в папке backend
cd backend

# Проверьте что виртуальное окружение активировано
# Если нет, активируйте (для Windows):
venv\Scripts\activate

# Установите зависимости еще раз
pip install -r requirements.txt

# Примените миграции
python manage.py migrate
```

### Frontend не запускается

```bash
# Убедитесь что вы в папке frontend
cd frontend

# Удалите node_modules и установите заново
rm -rf node_modules  # для Linux/Mac
rmdir /s node_modules  # для Windows
npm install

# Попробуйте запустить снова
npm start
```

### CORS ошибки

Если в консоли браузера видите ошибки CORS:

1. Проверьте что Django сервер запущен на http://localhost:8000
2. Проверьте settings.py в backend/zoo_catalog/settings.py:
   - В INSTALLED_APPS должен быть 'corsheaders'
   - В MIDDLEWARE должен быть 'corsheaders.middleware.CorsMiddleware'
   - CORS_ALLOWED_ORIGINS должен содержать 'http://localhost:3000'

### Товары не отображаются

1. Убедитесь что вы добавили товары через админ-панель
2. Проверьте что у товаров загружены изображения
3. Откройте http://localhost:8000/api/products/ - должен показываться JSON с товарами

## Дополнительные команды

### Создание новых миграций (при изменении моделей)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Загрузка статических файлов (для продакшн)

```bash
python manage.py collectstatic
```

### Сборка production версии React

```bash
cd frontend
npm run build
```

## Полезные ссылки

- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Frontend**: http://localhost:3000
- **Browsable API**: http://localhost:8000/api/products/

## Структура проекта

```
courseProj/
├── backend/           - Django проект (должен быть запущен)
├── frontend/          - React приложение (должно быть запущено)
├── course.txt         - Текст курсовой работы
├── README.md          - Основная документация
└── SETUP.md          - Эта инструкция
```

## Порты по умолчанию

- Backend (Django): **8000**
- Frontend (React): **3000**

**Важно**: Оба сервера должны работать одновременно!

---

Если у вас возникли проблемы, проверьте:

1. ✅ Python 3.11+ установлен
2. ✅ Node.js 18+ установлен
3. ✅ Оба терминала открыты и серверы запущены
4. ✅ В админ-панели добавлены тестовые данные
