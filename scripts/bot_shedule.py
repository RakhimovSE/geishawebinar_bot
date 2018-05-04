
from datetime import datetime
from multiprocessing import Pool
from time import sleep, time

import requests

from configs import messages, private_config as configs
from scripts.warehouse import Warehouse


class SheduleBot(object):
    def __init__(self):
        self.warehouse = Warehouse()
        self.tg_url = 'https://api.telegram.org/bot{}'.format(configs.TOKEN)
        self.proxy_dict = {
              "https" : 'https://66.70.147.197:3128'
            }

    def _send_pyment_message(self, chat_id):
        text = (messages.PAYMENT + configs.PAYMENT_URL).format(chat_id)
        return self._send_message(chat_id, text)

    def balancer(self, method, chats):
        def group(lst, n):
            return [lst[i:i + n] for i in range(0, len(lst), n)]

        statuses = []*len(chats)
        try:
            statuses = []
            for chats_group in group(chats,30):
                start = time()

                with Pool(30) as p:
                    statuses += p.map(method, chats_group)

                duration = time() - start
                if duration < 1:
                    sleep(duration)
        except Exception as e:
            print(e)
        print(statuses)
        return statuses



    def _send_message(self, chat_id, text):
        data = {
            'chat_id': chat_id,
            'text':text,
        }
        request = requests.post(self.tg_url+'/sendMessage', params=data,
                                proxies=self.proxy_dict)
        print(request.json())
        return request.json()['ok']

    def payment(self):
        chats = self.warehouse.get_payment()
        if chats:
            statuses = self.balancer(self._send_pyment_message, chats)
            self.warehouse.set_send_payment_status(chats, statuses)

    def send_if_not_pay(self, chat_id):
        return self._send_message(chat_id, messages.IF_NOT_PAY)

    def if_not_pay(self):
        chats = self.warehouse.get_if_not_pay()
        if chats:
            statuses = self.balancer(self.send_if_not_pay, chats)
            self.warehouse.set_send_if_not_pay_status(chats, statuses)

    def send_next_day_first_status(self, chat_id):
        return self._send_message(chat_id, messages.NEXT_DAY_FIRST)

    def next_day_first(self):
        chats = self.warehouse.get_next_day_first()
        if chats:
            statuses = self.balancer(self.send_next_day_first_status, chats)
            self.warehouse.set_send_next_day_first_status(chats, statuses)

    def send_next_day_second_status(self, chat_id):
        return self._send_message(chat_id, messages.NEXT_DAY_SECOND)

    def next_day_second(self):
        chats = self.warehouse.get_next_day_second()
        if chats:

            statuses = self.balancer(self.send_next_day_second_status, chats)
            self.warehouse.set_send_next_day_second_status(chats, statuses)

    def process(self):
        self.payment()
        self.if_not_pay()
        if datetime.fromtimestamp(time()).hour == 18:
            self.next_day_first()
        if datetime.fromtimestamp(time()).hour == 19:
            self.next_day_second()


    def polling(self):
        while True:
            try:
                self.process()
            except:
                print('Error')
            sleep(30)

if __name__ == '__main__':
    shedule_bot = SheduleBot()
    shedule_bot.polling()