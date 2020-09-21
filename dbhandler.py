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
        data = confighandler.parse_config()
        kw = int(data["kw"])
        nr = int(data["nr"])
        year = int(data["year"])
        unit = str(data["unit"])
        nickname = name

        self.cursor.execute(f"INSERT INTO {self.table_name}\
        ('name', 'surname', 'nickname', 'email', pwd_and_salt, unit, kw, nr, year) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, nickname, email, pwd_and_salt, unit, kw, nr, year))

        self.connection.commit()


    def getpw(self, name):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT pwd_and_salt FROM {self.table_name} WHERE email=?", (name, ))
        pwd_and_salt = self.cursor.fetchone()
        print(pwd_and_salt)
        if len(pwd_and_salt[0]) > 0:
            return pwd_and_salt[0]
        elif len(pwd_and_salt[0]) > 0:
            self.cursor.execute(f"SELECT pwd_and_salt FROM {self.table_name} WHERE nickname=?", (name, ))
            pwd_and_salt = self.cursor.fetchone()
            print("db response", pwd_and_salt)
            return pwd_and_salt[0]
        else:
            return False


    def get_name_nickname(self, email):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, nickname FROM {self.table_name} WHERE email =?", (email, ))
        data = self.cursor.fetchone()
        print("db response", data)
        if len(data) > 0:
            return data
        elif len(data) > 0:
            self.cursor.execute(f"SELECT name, nickname FROM {self.table_name} WHERE nickname =?", (email, ))
            return data
        else:
            return False


    def get_val(self, id=False):
        if id == False:
            self.cursor.execute("SELECT * FROM people")
            row = self.cursor.fetchone()

            vals = []
            while row is not None:
                # for v in row:
                #     vals.append(str(v))
                vals.append((str(row[0]), str(row[1]), str(row[2]))) # append name and id to list in tuple
                row = self.cursor.fetchone()

            self.connection.commit()
            return vals

        else:
            self.cursor.execute("SELECT * FROM people WHERE id=?", (id, ))
            row = self.cursor.fetchone()
            # new_id = row[0]
            name = row[1]
            age = row[2]
            self.connection.commit()
            return (new_id, name, age)
