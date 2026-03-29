# 🐳 Docker - Запуск проекта в контейнерах

## Преимущества Docker для проекта:

✅ Одна команда для запуска всего  
✅ Не нужно настраивать PostgreSQL вручную  
✅ Одинаковая среда на всех компьютерах  
✅ Легко развернуть на сервере  

---

## 📋 Установка Docker

### Windows:
1. Скачайте Docker Desktop: https://www.docker.com/products/docker-desktop
2. Установите
3. Запустите Docker Desktop
4. Дождитесь пока запустится (значок Docker в трее)

---

## 🚀 Запуск проекта в Docker

### Простой способ (одна команда):

```bash
cd D:\courseProj
docker-compose up
```

**Что произойдет:**
1. Скачаются образы PostgreSQL, Python, Node.js
2. Создастся контейнер с PostgreSQL
3. Создастся контейнер с Django
4. Создастся контейнер с React
5. Применятся миграции
6. Всё запустится автоматически!

**Первый запуск:** ~5-10 минут (скачивание образов)  
**Последующие:** ~30 секунд

---

## 📊 После запуска:

**Backend:** http://localhost:8000  
**Frontend:** http://localhost:3000  
**Админка:** http://localhost:8000/admin/  

---

## 🔄 Импорт данных в Docker

### Импорт товаров:

```bash
# Подключаемся к контейнеру backend
docker-compose exec backend python fix_categories.py
docker-compose exec backend python manage.py import_simple /app/../stock_price.xlsx
```

**Или проще - скопируйте файл в контейнер:**
```bash
docker cp stock_price.xlsx zoo_backend:/app/
docker-compose exec backend python manage.py import_simple stock_price.xlsx
```

---

## 🛑 Остановка и управление

```bash
# Остановить всё
docker-compose down

# Остановить и удалить данные
docker-compose down -v

# Перезапустить
docker-compose restart

# Посмотреть логи
docker-compose logs backend
docker-compose logs frontend

# Посмотреть запущенные контейнеры
docker-compose ps
```

---

## 📸 Добавление изображений в Docker

### Способ 1: Через админку (как обычно)
http://localhost:8000/admin/ - работает так же!

### Способ 2: Скопировать папку с изображениями

```bash
# Копируем папку с изображениями в контейнер
docker cp images_zoo zoo_backend:/app/images_zoo

# Запускаем команду добавления
docker-compose exec backend python manage.py add_images images_zoo --by-name
```

---

## 🗄️ Данные PostgreSQL в Docker

**Данные сохраняются между перезапусками!**

Volume `postgres_data` хранит всю БД даже после остановки контейнеров.

**Бэкап базы:**
```bash
docker-compose exec db pg_dump -U postgres zoo_catalog > backup.sql
```

**Восстановление:**
```bash
docker-compose exec -T db psql -U postgres zoo_catalog < backup.sql
```

---

## 🔧 Полезные команды

```bash
# Зайти в контейнер backend
docker-compose exec backend sh

# Зайти в PostgreSQL
docker-compose exec db psql -U postgres -d zoo_catalog

# Создать суперпользователя
docker-compose exec backend python manage.py createsuperuser

# Применить миграции
docker-compose exec backend python manage.py migrate

# Очистить volumes и начать заново
docker-compose down -v
docker-compose up
```

---

## 📝 docker-compose.yml - Что внутри

```yaml
services:
  db:          ← PostgreSQL база
  backend:     ← Django (Python)
  frontend:    ← React (Node.js)

volumes:
  postgres_data:  ← Данные БД
  media_files:    ← Изображения товаров
  static_files:   ← Статика
```

---

## 🎯 Быстрый старт с Docker

```bash
# 1. Установите Docker Desktop
# 2. Запустите его
# 3. В терминале:

cd D:\courseProj
docker-compose up -d

# Дождитесь запуска (проверить: docker-compose ps)

# 4. Импортируйте данные:
docker cp stock_price.xlsx zoo_backend:/app/
docker-compose exec backend python fix_categories.py
docker-compose exec backend python manage.py import_simple stock_price.xlsx

# 5. Создайте админа:
docker-compose exec backend python manage.py createsuperuser

# 6. Откройте:
# http://localhost:3000
```

---

## ❓ Проблемы

**"Docker не запускается"**
- Убедитесь что Docker Desktop запущен
- Проверьте в трее (значок кита)

**"Порт занят"**
- Остановите локальный сервер Django/React
- Или измените порты в docker-compose.yml

**"Контейнер не запускается"**
- Посмотрите логи: `docker-compose logs backend`

---

**Docker упрощает развертывание проекта!** 🐳



