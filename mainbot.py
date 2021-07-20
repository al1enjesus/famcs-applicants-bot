import os
import time
import telebot
import monitoringparser
import datamanipulation

TOKEN = os.getenv("bot_api_key")
bot = telebot.TeleBot(TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row("Инфа", "Кб", "Пи", "Пм")
Parser = monitoringparser.Parser()
DataBase = datamanipulation.DataBase()


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id,
                     "Привет, абитуриент! Напиши свой промежуток баллов. [ПРИМЕР: 365-361]",
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_score(message):
    print("{}: {}".format(message.from_user.username, message.text))
    if message.text in ["Инфа", "Кб", "Пи", "Пм"]:
        grade = DataBase.get_user_score(message.chat.id)
        if grade is None:
            bot.send_message(message.chat.id, "*Напиши свой промежуток баллов. [Пример: 365-361]*")

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

    else:
        DataBase.add_user(message.chat.id, message.from_user.username, message.text)
        bot.send_message(message.chat.id, "Если ты правильно написал балл, то выбирай специальность, которую хочешь "
                                          "посмотреть.\nНапиши/Нажми Инфа/Кб/Пм/Пи")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(5)
