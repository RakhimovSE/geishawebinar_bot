# -*- coding: utf-8 -*-
import telebot

from scripts.warehouse import Warehouse
from docs import private_config as configs

bot = telebot.TeleBot(configs.TOKEN)
warehouse = Warehouse()


@bot.message_handler(commands=['start'])
def start_message(message):
    data = configs.DATA
    data['telegram_id'] = message.chat.id
    print(data)
    bot.send_message(message.chat.id, configs.START_MESSAGE)
    warehouse.save_data(data=data)


@bot.message_handler(content_types=["text"])
def send_text_messages(message):
    bot.send_message(message.chat.id, configs.START_MESSAGE)



if __name__ == '__main__':
    bot.polling(none_stop=True)
