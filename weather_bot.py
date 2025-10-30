import os
import telebot
from telebot import types
from flask import Flask, request
import requests


BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY =  os.getenv("WEATHER_API")


bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(name)

# === Данные городов ===
CITIES = {
    "Москва": {"lat": 55.7558, "lon": 37.6173},
    "Санкт-Петербург": {"lat": 59.9343, "lon": 30.3351}
}

# === Клавиатура ===
def city_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(name) for name in CITIES.keys()]
    keyboard.add(*buttons)
    return keyboard

# === Команда /start ===
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот, который показывает погоду.\n\nВыбери город:",
        reply_markup=city_keyboard()
    )

# === Когда пользователь выбирает город ===
@bot.message_handler(func=lambda message: message.text in CITIES)
def show_weather(message):
    city = message.text
    coords = CITIES[city]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={coords['lat']}&lon={coords['lon']}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        msg = (
            f"🌤 Погода в {city}:\n"
            f"{desc}\n"
            f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"Влажность: {humidity}%\n"
            f"Ветер: {wind} м/с"
        )
        bot.send_message(message.chat.id, msg, reply_markup=city_keyboard())
    else:
        bot.send_message(message.chat.id, "⚠️ Не удалось получить погоду. Попробуй позже.", reply_markup=city_keyboard())

# === Обработка прочего ===
@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(message.chat.id, "Выбери город кнопкой 👇", reply_markup=city_keyboard())

# === Flask: принимаем запросы от Telegram ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Бот работает!", 200

# === Запуск вебхука ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
