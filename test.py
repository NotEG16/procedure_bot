import telebot
from telebot import types
from config import api_token

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Бот запущен")

    keyboard = generate_keyboard()
    bot.send_message(message.chat.id, text="Выбери своё настроение", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_buttton_click(call):
        bot.send_message(call.message.chat.id, text=f"Вы выбрали настроение {call.data}")




def generate_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    mood = ["Радость", "Грусть", "Спокойствие", "Удивление"]

    for i in mood:
        button = types.InlineKeyboardButton(text=f"настроение {i}", callback_data=f"{i}")
        keyboard.add(button)

    return keyboard


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)