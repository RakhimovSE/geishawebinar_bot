# -*- coding: utf-8 -*-
import sqlite3
import os
class Sqlite3(object):
    def __init__(self, way, table, dummy):
        self.way = way
        self.table = table
        self.dummy = dummy
        self.set_values(self.get_request("create", dummy))

    def set_values(self, request, *argv):
        print(os.listdir('.'))
        print(self.way)
        print(request)
        con = sqlite3.connect(self.way)
        cur = con.cursor()
        cur.execute(request, *argv)
        con.commit()
        con.close()

    def get_values(self, request):
        con = sqlite3.connect(self.way)
        cur = con.cursor()
        cur.execute(request)
        result = cur.fetchall()
        con.commit()
        con.close()
        return result

    def get_request(self, mode, dummy):

        columns = ", ".join(self.dummy.keys())
        placeholders = ", ".join("?" * len(dummy))
        values = ", ".join(["{} {}".format(x[0], x[1])
                            for x in dummy.items()])


        base_requests = dict(
            create="CREATE TABLE IF NOT EXISTS {} ({})".format(self.table, values),
            insert="INSERT INTO {} ({}) values({})".format(self.table, columns, placeholders),
            replace="REPLACE INTO {} values({})".format(self.table, placeholders))

        return base_requests[mode]
