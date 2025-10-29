import os
import telebot
from telebot import types
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY =  os.getenv("WEATHER_API")

bot = telebot.TeleBot(BOT_TOKEN)

# Клавиатура с кнопками
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("/start"))
    keyboard.add(types.KeyboardButton("/weather"))
    return keyboard

# /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Нажми /weather, чтобы узнать погоду.",
        reply_markup=main_keyboard()
    )

# /weather
@bot.message_handler(commands=["weather"])
def ask_city(message):
    msg = bot.send_message(message.chat.id, "Отправь название города, чтобы узнать погоду:")
    bot.register_next_step_handler(msg, send_weather)

# Функция получения погоды
def send_weather(message):
    city = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        # Попробуем взять данные за последний час, если есть
        rain_last_hour = data.get("rain", {}).get("1h", 0)
        snow_last_hour = data.get("snow", {}).get("1h", 0)
        
        weather_msg = (
            f"Погода в {city}:\n"
            f"{weather_desc}\n"
            f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"Влажность: {humidity}%\n"
            f"Ветер: {wind_speed} м/с\n"
            f"Осадки за последний час: дождь {rain_last_hour} мм, снег {snow_last_hour} мм"
        )
        bot.send_message(message.chat.id, weather_msg, reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id, "Не удалось получить погоду. Проверь название города.", reply_markup=main_keyboard())

bot.polling(none_stop=True)
