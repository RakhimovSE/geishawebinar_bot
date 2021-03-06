# -*- coding: utf-8 -*-
import telebot
from telebot import apihelper

from configs import messages, private_config as configs
from scripts.warehouse import Warehouse

apihelper.proxy = {'https':'https://66.70.147.197:3128'}
bot = telebot.TeleBot(configs.TOKEN)
warehouse = Warehouse()




@bot.message_handler(commands=['start'])
def start_message(message):
    data = configs.DATA
    bot.send_message(message.chat.id, messages.START)
    warehouse.set_start(message)

@bot.message_handler(commands=['payment'])
def start_message(message):
    warehouse.set_payment(message)

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    warehouse.set_payment(message)



if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(e)
