# -*- coding: utf-8 -*-
import telebot
from telebot.types import LabeledPrice

from scripts.warehouse import Warehouse
from docs import private_config as configs

from time import sleep

bot = telebot.TeleBot(configs.TOKEN)
warehouse = Warehouse()


@bot.message_handler(commands=['start'])
def start_message(message):
    data = configs.DATA
    data['telegram_id'] = message.chat.id
    bot.send_message(message.chat.id, configs.START_MESSAGE)
    warehouse.save_data(data=data)

    sleep(configs.SLEEP01)

    prices = [LabeledPrice(label=configs.PRICE_DESCRIPTION, amount=configs.PRICE),]
    bot.send_invoice(message.chat.id, title=configs.PRICE_DESCRIPTION,
                     description=configs.PRICE_LABEL,
                     invoice_payload='payload',
                     provider_token=configs.PROVIDER_TOKEN,
                     currency='RUB',
                     prices=prices,
                     start_parameter='test'
                     )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    pass

@bot.message_handler(content_types=["text"])
def send_text_messages(message):
    bot.send_message(message.chat.id, configs.START_MESSAGE)



if __name__ == '__main__':
    bot.polling(none_stop=True)
