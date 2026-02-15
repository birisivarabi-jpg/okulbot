import telebot
from telebot import types
import threading
import time
from datetime import datetime

TOKEN = "8305501223:AAFRNXBEdFSVY7g8_9i7c5-m15krH0mbaTM"
bot = telebot.TeleBot(TOKEN)

# Buttons
BTN_COURSES = "📚 Курсы"
BTN_SIGNUP = "📝 Записаться"
BTN_SCHEDULE = "📅 Расписание"
BTN_NOTIFY = "🔔 Уведомления"
BTN_HELP = "❓ Помощь"
BTN_CANCEL = "⬅️ Отмена"

# Storage (memory)
user_states = {}
user_data = {}
subscribers = set()

# Main menu
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(BTN_COURSES, BTN_SIGNUP)
    kb.add(BTN_SCHEDULE, BTN_NOTIFY)
    kb.add(BTN_HELP)
    return kb

# Start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите пункт меню:",
        reply_markup=main_menu()
    )


