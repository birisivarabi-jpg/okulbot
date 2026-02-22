import telebot
from telebot import types
import threading
import time
from datetime import datetime

TOKEN = "8305501223:AAFRNXBEdFSVY7g8_9i7c5-m15krH0mbaTM"
bot = telebot.TeleBot(TOKEN)

BTN_COURSES = "📚 Курсы"
BTN_SIGNUP = "📝 Записаться"
BTN_SCHEDULE = "📅 Расписание"
BTN_NOTIFY = "🔔 Уведомления"
BTN_HELP = "❓ Помощь"
BTN_CANCEL = "⬅️ Отмена"

user_states = {}
user_data = {}
subscribers = set()

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(BTN_COURSES, BTN_SIGNUP)
    kb.add(BTN_SCHEDULE, BTN_NOTIFY)
    kb.add(BTN_HELP)
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать!",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == BTN_COURSES)
def courses(message):
    bot.send_message(message.chat.id, "Наши курсы:\nPython\nWeb\nData Science")

@bot.message_handler(func=lambda m: m.text == BTN_SIGNUP)
def signup_start(message):
    user_states[message.chat.id] = "name"
    bot.send_message(message.chat.id, "Как тебя зовут?")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "name")
def signup_name(message):
    user_data[message.chat.id] = {"name": message.text}
    user_states[message.chat.id] = "course"

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Python", "Web", "Data Science")
    kb.add(BTN_CANCEL)

    bot.send_message(message.chat.id, "Выбери курс:", reply_markup=kb)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "course")
def signup_course(message):
    if message.text == BTN_CANCEL:
        user_states.pop(message.chat.id, None)
        user_data.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "Отменено", reply_markup=main_menu())
        return

    name = user_data[message.chat.id]["name"]
    course = message.text

    user_states.pop(message.chat.id, None)
    user_data.pop(message.chat.id, None)

    bot.send_message(
        message.chat.id,
        f"{name}, ты записан на {course}",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == BTN_SCHEDULE)
def schedule(message):
    bot.send_message(message.chat.id, "Пн Ср Пт — 18:00")

@bot.message_handler(func=lambda m: m.text == BTN_NOTIFY)
def notifications(message):
    chat_id = message.chat.id
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        bot.send_message(chat_id, "Уведомления выключены")
    else:
        subscribers.add(chat_id)
        bot.send_message(chat_id, "Уведомления включены")

def notification_worker():
    sent_dates = set()
    while True:
        now = datetime.now()
        if now.weekday() in [0, 2, 4] and now.hour == 17 and now.minute == 50:
            if now.date() not in sent_dates:
                for chat_id in subscribers:
                    try:
                        bot.send_message(chat_id, "Через 10 минут занятие")
                    except:
                        pass
                sent_dates.add(now.date())
        time.sleep(30)

threading.Thread(target=notification_worker, daemon=True).start()

print("Bot started...")
bot.polling(none_stop=True)
