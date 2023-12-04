!pip install pytelegrambotapi

import telebot
from telebot import types

import random
import re

import pandas as pd
elements = pd.read_csv('https://raw.githubusercontent.com/Ciper96/homework/main/quotes.csv')

your_bot = "МЕСТО_ДЛЯ_ТОКЕНА"

bot = telebot.TeleBot(your_bot)

@bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = "Приветствую! Я - бот для обработки текстов. Для начала работы отправьте мне любой текст сообщением."
    bot.send_message(message.chat.id, first_mess)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    
    global user_text
    user_text = message.text
    
    markup = types.InlineKeyboardMarkup()
    button_dlina = types.InlineKeyboardButton(text = 'Длина текста', callback_data='dlina')
    markup.add(button_dlina)
    button_obratno = types.InlineKeyboardButton(text = 'Обратить текст', callback_data='obratno')
    markup.add(button_obratno)
    button_soyuz = types.InlineKeyboardButton(text = 'Наличие союза "И"', callback_data='soyuz')
    markup.add(button_soyuz)   
    button_secret = types.InlineKeyboardButton(text = 'Секретная кнопка', callback_data='secret')
    markup.add(button_secret)
    bot.send_message(message.chat.id, "Принято! А теперь выберите действие.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:
        if function_call.data == "dlina":
            bot.send_message(function_call.message.chat.id, "В тексте " + str(len(user_text)) + " символов(а)")

        elif function_call.data == "obratno":
            bot.send_message(function_call.message.chat.id, "Текст наоборот:\n\n{}".format(user_text[::-1]))
         
        elif function_call.data == "soyuz":
            match = re.search(r'\b[Ии]\b', user_text)
            if match:
                bot.send_message(function_call.message.chat.id, "В тексте есть союз 'И'.")   
            else:
                bot.send_message(function_call.message.chat.id, "В тексте нет союза 'И'.")
                        
        else:
            bot.send_message(function_call.message.chat.id, "Случайная цитата Игоря Крутого:\n\n{}".format(random.choice(elements['quotes'])))
            
        bot.answer_callback_query(function_call.id)

bot.infinity_polling()
