# MIT License
#
# Copyright (c) 2020 TheCoder777
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sqlite3, confighandler, paths, sys


class UserDB():
    def __init__(self):
        self.table_name = "users"
        self.db_path = paths.USER_DB_PATH
        self.initialize()

    def get_cursor(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection.cursor()

    def initialize(self):
        try:
            self.cursor = self.get_cursor()
            self.cursor.execute(f"CREATE TABLE if not exists {self.table_name} \
            (id INTEGER PRIMARY KEY, \
            name TEXT, surname TEXT, \
            nickname TEXT, \
            email TEXT, \
            pwd_and_salt TEXT, \
            unit TEXT, \
            kw INTEGER, \
            nr INTEGER, \
            year INTEGER)")
            return True

        except FileNotFoundError as e:
            print("Database file not found!", file=sys.stderr)
            return False


    def add_user(self, name, surname, email, pwd_and_salt):
        self.cursor = self.get_cursor()
        data = confighandler.get_default_config()
        kw = int(data["kw"])
        nr = int(data["nr"])
        year = int(data["year"])
        unit = str(data["unit"])
        nickname = name

        self.cursor.execute(f"INSERT INTO {self.table_name}\
        ('name', 'surname', 'nickname', 'email', pwd_and_salt, unit, kw, nr, year) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, nickname, email, pwd_and_salt, unit, kw, nr, year))
        self.connection.commit()


    def update_config(self, user, data):
        self.cursor = self.get_cursor()
        try:
            data["kw"] = int(data["kw"])
            data["nr"] = int(data["nr"])
            data["year"] = int(data["year"])
        except ValueError:
            pass
        vals = list(data.values())
        vals.append(user.email)
        #print("UPDATE users SET name={}, surname={}, nickname={}, email={}, unit={}, kw={}, nr={}, year={} WHERE email={}".format(*vals))
        self.cursor.execute(f"UPDATE {self.table_name} SET \
        name=?, surname=?, nickname=?, email=?, unit=?, kw=?, nr=?, year=? WHERE email=?", (vals))
        self.connection.commit()
        return True


    def get_pw_by_email(self, email):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT pwd_and_salt FROM {self.table_name} WHERE email=?", (email, ))
        pwd_and_salt = self.cursor.fetchone()
        if pwd_and_salt:
            return pwd_and_salt[0]
        else:
            return False


    def get_pw_by_nickname(self, nickname):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT pwd_and_salt FROM {self.table_name} WHERE nickname=?", (nickname, ))
        pwd_and_salt = self.cursor.fetchone()
        if pwd_and_salt:
            return pwd_and_salt[0]
        else:
            return False


    def get_name_nickname_by_email(self, email):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, nickname FROM {self.table_name} WHERE email =?", (email, ))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return False


    def get_email_by_nickname(self, nickname):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT email FROM {self.table_name} WHERE nickname =?", (nickname, ))
        data = self.cursor.fetchone()
        if data:
            return data[0]
        else:
            return False


    def get_user_data(self, user):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, surname, unit, kw, nr, year FROM {self.table_name} WHERE email =?", (user.email, ))
        data = {}
        data["name"], data["surname"], data["unit"], data["kw"], data["nr"], data["year"] = self.cursor.fetchone()
        return data


    def get_settings_data(self, user):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, surname, nickname, email, unit, kw, nr, year FROM {self.table_name} WHERE email =?", (user.email, ))
        data = {}
        data["name"], data["surname"], data["nickname"], data["email"], data["unit"], data["kw"], data["nr"], data["year"] = self.cursor.fetchone()
        return data
