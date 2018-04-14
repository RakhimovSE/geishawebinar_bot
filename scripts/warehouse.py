from scripts.sqlite3_api import Sqlite3
from docs import private_config as config
from docs import messages
import time
class Warehouse(object):
    def __init__(self):
        #todo: add normal ways
        way = '../data/geishawebinar_bot.db'
        self.database = Sqlite3(way, 'geishawebinar_bot', config.DATA)

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
        request = '''update geishawebinar_bot
                    set payment_status = 1, payment_date = {}
                    where telegram_id == {}'''.format( message.date,
                                                       message.from_user.id )
        try:
            self.database.set_values(request)

        except Exception as e:
            print(e)
    def get_payment(self):
        #todo: shit
        result = []
        try:
            request = ''' select telegram_id
                        from geishawebinar_bot 
                        where {} - start_date > {} and send_payment_status == 0
                        '''.format(int(time.time()), messages.TIME_FOR_PAYMENT)
            chats = self.database.get_values(request)
            result = list(chats[0])
        except Exception as e:
            print(e)
        return result

    def set_send_payment_status(self, chats, statuses):
        try:
            for i in range(len(chats)):

                request = '''update geishawebinar_bot
                            set send_payment_status = {}
                            where telegram_id == {}'''.format(int(statuses[i]), chats[i])
                self.database.set_values(request)
        except Exception as e:
            print(e)

    def get_if_not_pay(self):
        result = []
        try:
            request = ''' select telegram_id 
                        from geishawebinar_bot 
                        where send_payment_status == 1 and payment_status == 0 
                        and send_if_not_pay_status == 0'''
            chats = self.database.get_values(request)
            result = list(chats[0])
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
            request = ''' select telegram_id 
                        from geishawebinar_bot 
                         where payment_status == 1 and send_next_day_first_status == 0'''
            chats = self.database.get_values(request)
            result = list(chats[0])
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
            request = ''' select telegram_id 
                           from geishawebinar_bot 
                            where payment_status == 1 and send_next_day_second_status == 0'''
            chats = self.database.get_values(request)
            result = list(chats[0])
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

wh = Warehouse()
print(wh.get_payment())