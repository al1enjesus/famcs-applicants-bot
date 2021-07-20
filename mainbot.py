import os
import time
import telebot
import monitoringparser
import datamanipulation

TOKEN = os.getenv("bot_api_key")
bot = telebot.TeleBot(TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row("Инфа", "Пи")
keyboard.row("Кб", "Пм")
keyboard.row("Ам", "Эк")
Parser = monitoringparser.Parser()
DataBase = datamanipulation.DataBase()


def grade_to_range(grade: int) -> str:
    if grade >= 391:               
        return "391+"
    if grade <= 120:
        return "120-" 
    remainder = grade % 5
    if remainder == 0:
        return f'{grade}-{grade - 4}'
    return f'{grade - remainder + 5}-{grade - remainder + 1}'


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id,
                     "Привет, абитуриент! Напиши свои баллы. [Пример: 365]",
                     reply_markup=keyboard)
    DataBase.delete_user(message.chat.id)


@bot.message_handler(content_types=['text'])
def send_score(message):
    print("{}: {}".format(message.from_user.username, message.text))
    if message.text in ["Инфа", "Кб", "Пи", "Пм", "Ам", "Эк"]:
        grade = DataBase.get_user_score(message.chat.id)
        if grade is None:
            bot.send_message(message.chat.id, "*Напиши свои баллы. [Пример: 365]*")

    if message.text == "Инфа" and grade:
        try:
            response = Parser("информатика", grade)
        except Exception:
            bot.send_message(message.chat.id, "Проверь правильность написания баллов!")
            DataBase.delete_user(message.chat.id)
        else:
            bot.send_message(message.chat.id, response)

    elif message.text == "Кб" and grade:
        try:
            response = Parser("компьютерная безопасность (направление - математические методы и программные системы)",
                              grade)
        except Exception:
            bot.send_message(message.chat.id, "Проверь правильность написания баллов!")
            DataBase.delete_user(message.chat.id)
        else:
            bot.send_message(message.chat.id, response)

    elif message.text == "Пи" and grade:
        try:
            response = Parser("прикладная информатика (направление - программное обеспечение компьютерных систем)",
                              grade)
        except Exception:
            bot.send_message(message.chat.id, "Проверь правильность написания баллов!")
            DataBase.delete_user(message.chat.id)
        else:
            bot.send_message(message.chat.id, response)

    elif message.text == "Пм" and grade:
        try:
            response = Parser("прикладная математика (направление - научно-производственная деятельность)", grade)
        except Exception:
            bot.send_message(message.chat.id, "Проверь правильность написания баллов!")
            DataBase.delete_user(message.chat.id)
        else:
            bot.send_message(message.chat.id, response)

    elif message.text == "Ам" and grade:
        try:
            response = Parser("актуарная математика", grade)
        except Exception:
            bot.send_message(message.chat.id, "Проверь правильность написания баллов!")
            DataBase.delete_user(message.chat.id)
        else:
            bot.send_message(message.chat.id, response)

    elif message.text == "Эк" and grade:
        try:
            response = Parser("экономическая кибернетика (направление - математические методы и компьютерное моделирование в экономике)", grade)
        except Exception:
            bot.send_message(message.chat.id, "Проверь правильность написания баллов!")
            DataBase.delete_user(message.chat.id)
        else:
            bot.send_message(message.chat.id, response)

    else:
        try:
            grade = int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, "Некорректный ввод =(")
        else:    
            DataBase.add_user(message.chat.id, message.from_user.username, grade_to_range(grade))
            bot.send_message(message.chat.id, "Если ты правильно написал балл, то выбирай специальность, которую хочешь "
                                            "посмотреть.\nНапиши/Нажми Инфа/Кб/Пм/Пи", reply_markup=keyboard)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(5)
