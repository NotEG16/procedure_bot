import telebot
from config import api_token
import logging
import json
from datetime import date, timedelta

TOKEN = api_token
bot = telebot.TeleBot(TOKEN)

days_list = []
time_list = []


days_time = 0


#---------learning/homework---------#
    #today
    #d = date.today()
    #dt = datetime.now()
    #t = time(5, 30, 25)
    #d = date(2015, 10, 23)

    #formatted_time = d.strftime("%d/%m/%Y")

    #date1 = date(2007, 2, 4)
    #date2 = date(2016, 7, 16)
    #result = date2 - date1
    #print(result.days)
#-----------------------------------#


user_data = {}
try:
    with open("data.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Бот для записи на процедуры запущен")



def generate_date_schedule():
    keyboard = telebot.types.InlineKeyboardMarkup()
    days = []
    global days_time

    for i in range(7):
        days.append(date.today() + timedelta(days=3 + i))


    for day in days[:]:
        x_day = day.strftime("%Y-%m-%d")
        time = ["10:00", "12:00", "15:00", "17:00"] 
        for day_json in user_data["apointments"]:
            if day_json["date"] == x_day: 
                for b in time:
                    if day_json["time"] == b:
                        time.remove(day_json["time"])
                        if time == []:
                            days.remove(day) 
 
    if days == []:
        days_time = 1

    #making buttons and adding them to keyboard
    for button_text in days:
        callback_data = f"date : {button_text}"
        button = telebot.types.InlineKeyboardButton(text=f"{button_text}", callback_data=callback_data)
        keyboard.add(button)

    return keyboard


@bot.message_handler(commands=["show_dates"])
def handle_schedule(message):
    keyboard = generate_date_schedule()

        
    #if days_time == []:
     #   bot.send_message(message.chat.id, "Sorry no avaliable dates")
    if days_time == 0:
        bot.send_message(message.chat.id, "Выберите дату:", reply_markup=keyboard)
    elif days_time == 1:
        bot.send_message(message.chat.id, "К сожалению, свободных дней нет, вернитесь позже.")


@bot.callback_query_handler(func= lambda call: True )
def handle_button_click(call):


        if "date" in call.data:
            day = call.data.split(" : ")[1]
            days_list.append(day)
            handle_time(call.message, day)
            #generate_time_schedule(call.message, day)


        if "meeting" in call.data:
            time = call.data.split(" : ")[1]
            time_list = time


            for day in days_list:
                bot.send_message(call.message.chat.id, text =f"Вы записаны на {day} в {time_list}. Ждём вас!")
                add_apointment(day, time_list, f"{call.message.chat.id}")
                days_list.remove(day)

@bot.message_handler(commands=["show_time"])
def handle_time(message, date):

    bot.send_message(message.chat.id, "Выберите время:", reply_markup=generate_time_schedule(date))


#@bot.message_handler(commands=["review"])
def handle_review(message):
    bot.send_message(message.chat.id, "Type in review:")
    review = message.text

    bot.register_next_step_handler(message, save_review)


def save_review(message):

    user_review = message.text.strip()
    
    add_review(f"{message.chat.id}", user_review)

    
def generate_time_schedule(date):
    keyboard = telebot.types.InlineKeyboardMarkup()
    time = ["10:00", "12:00", "15:00", "17:00"]

  
    for a in user_data["apointments"]:
        if a["date"] == date:
            for b in time:
                if a["time"] == b:
                    time.remove(a["time"])
                
               # if time == []:
                #    bot.send_message(message.chat.id, "No avaliable date on time. Please choose another")
                 #   handle_schedule(message)

   
    for i in time:
        callback_data = f"meeting : {i}"
        button = telebot.types.InlineKeyboardButton(text=f"{i}", callback_data=callback_data)
        keyboard.add(button)
          
    return keyboard

    
def add_apointment(date, time, client):

    add_new_apointments = {"date" : date, "time" : time, "client" : client}
    user_data["apointments"].append(add_new_apointments)


    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)


def add_review(client, review):

    add_new_review = {"client" : client, "text" : review}
    user_data["review"].append(add_new_review)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)
    

@bot.message_handler(commands=["name"])
def recieve_name(message):
    bot.send_message(message.chat.id, "Как вас зовут?")
    name = message.text

    bot.register_next_step_handler(message, save_name)


def save_name(message):
    user_name = message.text
    add_name_to_dict(f"{message.chat.id}", user_name)
    
    handle_schedule(message)


def add_name_to_dict(id, name):

    add_new_name = {id : name}
    user_data["clients"].append(add_new_name)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    #add_apointment("20.01.2024", "13:00", "Ольга Н.")
    #add_review("test", "test")


    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting bot...")

    bot.polling(non_stop=True)