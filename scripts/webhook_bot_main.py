# -*- coding: utf-8 -*-
#todo: delete
import telebot
from flask import Flask, request
from telebot import apihelper

from configs import messages, private_config as configs
from scripts.warehouse import Warehouse

# CONFIG
TOKEN = configs.TOKEN
HOST = '34.209.89.75'
PORT = 8443
CERT = '../docs/webhook_cert.pem'
CERT_KEY = '../docs/webhook_pkey.pem'

apihelper.proxy = {'https':'https://66.70.147.197:3128'}
bot = telebot.TeleBot(configs.TOKEN)
warehouse = Warehouse()

app = Flask(__name__)
context = (CERT, CERT_KEY)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_json(force=True))
    bot.process_new_updates([update])

    return 'OK'


def setWebhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://{}:{}/{}'.format(HOST, PORT, TOKEN),
                   certificate=open(CERT, 'rb'))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, messages.START)
    warehouse.set_start(message)


if __name__ == '__main__':
    setWebhook()

    app.run(host='0.0.0.0',
            port=PORT,
            ssl_context=context,
            debug=True)