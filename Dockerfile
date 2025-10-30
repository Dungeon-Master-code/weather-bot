# 1️⃣ Базовый образ
FROM python:3.11-slim

# 2️⃣ Рабочая директория
WORKDIR /app

# 3️⃣ Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Копируем весь проект
COPY . .

# 6️⃣ Указываем порт (Railway требует 8080)
EXPOSE 8080

# 7️⃣ Запускаем Flask через Gunicorn
CMD ["gunicorn", "weather_bot:app", "--bind", "0.0.0.0:8080"]
