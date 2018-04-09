from scripts.sqlite3_api import Sqlite3
from docs import private_config as config

class Warehouse(object):
    def __init__(self):
        #todo: add normal ways
        way = '../data/geishawebinar_bot.db'
        self.database = Sqlite3(way, 'auto_betting', config.DATA)

    def save_data(self, data):
        request = self.database.get_request('insert', data)
        self.database.set_values(request, list(data.values()))
