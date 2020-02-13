# Класс записывает в базу данных показания с сенсоров.

import sqlite3
import time

class SensorsDB:
    def __init__(self, db_path, table_name, value=1):
        self.db_path = db_path
        self.table_name = table_name
        self.value = value

    def create_commit(self):
        con = sqlite3.connect(self.db_path)

        cur = con.cursor()

        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}\
                    (Time TEXT,"
                    "Value FLOAT)")

        cur.execute(f"INSERT INTO {self.table_name}\
                    VALUES({time.time()},\
                     {self.value})")

        con.commit()
        cur.close()
        con.close()