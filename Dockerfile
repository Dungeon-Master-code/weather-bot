# 1️⃣ Базовый образ с Python
FROM python:3.11-slim

# 2️⃣ Устанавливаем рабочую директорию
WORKDIR /app

# 3️⃣ Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Копируем исходный код
COPY . .

# 5️⃣ Указываем порт (Railway использует 8080)
EXPOSE 8080

# 6️⃣ Запускаем приложение через Gunicorn
CMD ["gunicorn", "weather_bot:app", "--bind", "0.0.0.0:8080"]
