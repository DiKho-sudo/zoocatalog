FROM node:18-alpine

WORKDIR /app

# Копируем package.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходники
COPY . .

# Открываем порт
EXPOSE 3000

# Запуск приложения
CMD ["npm", "start"]









