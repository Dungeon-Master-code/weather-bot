import os
import requests
import telebot

TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API = os.getenv("WEATHER_API")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я скажу тебе погоду в Петербурге 🌦")

@bot.message_handler(commands=['weather'])
def weather(message):
    city = "Saint Petersburg"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=ru"
    response = requests.get(url).json()
    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]
    bot.reply_to(message, f"Сейчас в Петербурге {temp}°C, {desc}")

bot.polling()
