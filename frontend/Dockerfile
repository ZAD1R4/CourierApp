# frontend/Dockerfile

FROM node:18

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json ./
RUN npm install

# Копируем остальные файлы
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]