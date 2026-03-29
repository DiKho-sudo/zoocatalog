FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем entrypoint скрипт
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Копируем проект
COPY . .

# Создаем папки для медиа и устанавливаем права
RUN mkdir -p media/products media/brands media/categories media/animal_types staticfiles && \
    chmod -R 777 media staticfiles

# Открываем порт
EXPOSE 8000

# Устанавливаем entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]







