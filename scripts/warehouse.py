from scripts.sqlite3_api import Sqlite3
from docs import private_config as config
from docs import messages
import time
import pandas as pd
from datetime import datetime
class Warehouse(object):
    """
    Класс - обертка над функционалом Sqlite3: все необходимые запросы обернуты 
    в функции.
    """
    def __init__(self):
        """
        Инициализация базы данных
        """
        #todo: add normal ways
        way = '../data/geishawebinar_bot.db'
        self.database = Sqlite3(way, 'geishawebinar_bot', config.DATA)

    def _get_df(self):
        """
        Для того, чтобы было удобнее работать со временем, выгрузка бд происходит
        в формате pandas.
        :return: 
        """

        request = '''select * from geishawebinar_bot'''
        values = self.database.get_values(request)

        return pd.DataFrame(values, columns = config.DATA.keys())

    def set_start(self, message):
        data = {}
        for key, value in config.DATA.items():
            data[key] = 0
        data['telegram_id'] = message.from_user.id
        data['first_name'] = message.from_user.first_name
        data['username'] = message.from_user.username
        data['last_name'] = message.from_user.last_name
        data['start_date'] = time.time()

        try:
            request = self.database.get_request('insert', data)
            self.database.set_values(request, list(data.values()))
        except Exception as e:
            print(e)

    def set_payment(self, message):
        """
        Функция нужна для установки флага об оплате
        :param message: 
        :return: 
        """
        request = '''update geishawebinar_bot
                    set payment_status = 1, payment_date = {}
                    where telegram_id == {}'''.format( message.date,
                                                       message.from_user.id )
        try:
            self.database.set_values(request)

        except Exception as e:
            print(e)

    def get_payment(self):
        """ 
        Получеаем id людей которым нужно отправить сообщение с предложением 
        оплаты. Это сообщение отправляется спустя время определенное в конфиге
        """
        result = []
        try:
            df = self._get_df()
            users = df[(time.time() - df.start_date > config.DELAY_PAYMENT_MESSAGE)
                        & (df.send_payment_status == 0)].telegram_id
            result = list(users)
        except Exception as e:
            print(e)
        return result


    def set_send_payment_status(self, chats, statuses):
        """
        функция нужна для установки флага отправки сообщения об оплате
        :param chats: 
        :param statuses: 
        :return: 
        """
        try:
            for i in range(len(chats)):

                request = '''update geishawebinar_bot
                            set send_payment_status = {}
                            where telegram_id == {}'''.format(int(statuses[i]), chats[i])
                self.database.set_values(request)
        except Exception as e:
            print(e)

    def get_if_not_pay(self):
        """
        Если человек не оплатил вебинар ему отпарвялется повторное сообщение, 
        
        :return: 
        """
        result = []
        try:
            df = self._get_df()
            users = df[(time.time() - df.start_date > config.DELAY_PAYMENT_MESSAGE)
                        & (df.send_payment_status == 1)
                        & (df.payment_status == 0)
                        & (df.send_if_not_pay_status == 0)].telegram_id
            result = list(users)
        except Exception as e:
            print(e)

        return result

    def set_send_if_not_pay_status(self, chats, statuses):

        try:
            for i in range(len(chats)):

                request = '''update geishawebinar_bot
                            set send_if_not_pay_status = {}
                            where telegram_id == {}'''.format(int(statuses[i]), chats[i])
                self.database.set_values(request)
        except Exception as e:
            print(e)



    def get_next_day_first(self):
        result = []
        try:
            df = self._get_df()
            users = df[(df.apply(_check_next_day, axis = 1))
                & (df.send_next_day_first_status == 0)
                & (df.payment_status == 1)].telegram_id

            result = list(users)
        except Exception as e:
            print(e)

        return result


    def set_send_next_day_first_status(self, chats, statuses):
        try:
            for i in range(len(chats)):
                request = '''update geishawebinar_bot
                               set send_next_day_first_status = {}
                               where telegram_id == {}'''.format(
                    int(statuses[i]), chats[i])
                self.database.set_values(request)
        except Exception as e:
            print(e)


    def get_next_day_second(self):
        result = []
        try:
            df = self._get_df()
            users = df[(df.apply(_check_next_day, axis = 1))
                       & (df.send_next_day_second_status == 0)
                       & (df.payment_status == 1)].telegram_id

            result = list(users)
        except Exception as e:
            print(e)

        return result

    def set_send_next_day_second_status(self, chats, statuses):
        try:
            for i in range(len(chats)):
                request = '''update geishawebinar_bot
                                  set send_next_day_second_status = {}
                                  where telegram_id == {}'''.format(
                    int(statuses[i]), chats[i])
                self.database.set_values(request)
        except Exception as e:
            print(e)

def _check_next_day(x):
        now = datetime.fromtimestamp(time.time())
        start = datetime.fromtimestamp(x.start_date)
        delta = now - start
        return delta.days == -1