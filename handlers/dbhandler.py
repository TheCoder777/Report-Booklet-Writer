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


# load system modules
import os
import sqlite3
import sys

# load internal modules
from defines import configs
from defines import paths
from defines.colormode import Colormode
from models.user import User
from handlers import datecalc


def quickedit_defaults():
    """
    Calculates the default /quickedit values, if they aren't returned (re-calculated)
    """
    return {
        # calculate start/end with given values for anonymous user
        "sign": datecalc.calc_sign_date(),
        "year": datecalc.get_current_year(),
        "week": datecalc.get_current_week(),
        "unit": configs.UNIT,
    }


def quickedit_data(year, week):
    """
    Calculates all values needed to export the final pdf
    """
    return datecalc.calc_all_from_config(int(year), int(week))


def edit_data(year, week):
    """
    Calculates /edit values for logged in users
    """
    return datecalc.calc_all_for_user(int(year), int(week))


class UserDB:
    # TODO: unify all comments (""" """/ #)
    def __init__(self):
        self.table_name = "users"
        self.db_path = paths.USER_DB_PATH
        self.initialize()

    def get_cursor(self):
        connection = sqlite3.connect(self.db_path)
        return connection.cursor(), connection

    def initialize(self):
        try:
            cursor, connection = self.get_cursor()

            cursor.execute(f"CREATE TABLE if not exists {self.table_name} \
            (id INTEGER PRIMARY KEY, \
            name TEXT, \
            surname TEXT, \
            nickname TEXT, \
            email TEXT, \
            pwd_and_salt TEXT, \
            unit TEXT, \
            week INTEGER, \
            nr INTEGER, \
            year INTEGER, \
            beginning_year INTEGER, \
            color_mode TEXT)")
            cursor.close()
            connection.close()
            return True

        except FileNotFoundError:
            print(f"Database file '{self.db_path}' not found!", file=sys.stderr)
            return False

    def update_custom(self, field, value, user):
        cursor, connection = self.get_cursor()
        cursor.execute(f"UPDATE {self.table_name} SET {field}=? WHERE id=?", (value, user.uid))
        connection.commit()
        cursor.close()
        connection.close()

    def new_user(self, cr, pwd):
        cursor, connection = self.get_cursor()

        # default nickname is the username
        nickname = cr["name"]
        # get defaults from config
        week = configs.START_WEEK
        nr = configs.NR
        year = configs.YEAR
        beginning_year = calc_beginning_year()
        unit = configs.UNIT
        color_mode = Colormode.DARK

        # list for both the db and the User object
        db_entry = [cr["name"],
                    cr["surname"],
                    nickname,
                    cr["email"],
                    pwd,
                    unit,
                    week,
                    nr,
                    year,
                    beginning_year,
                    color_mode]

        # add user to db
        cursor.execute(f"INSERT INTO {self.table_name}\
        (name, surname, nickname, email, pwd_and_salt, unit, week, nr, year, beginning_year, color_mode) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", db_entry)
        connection.commit()
        # self.cursor.close()

        # add current uid to entry (last used id by the current cursor)
        user_entry = [cursor.lastrowid,
                      cr["name"],
                      cr["surname"],
                      nickname,
                      cr["email"],
                      # Without pwd now!
                      unit,
                      week,
                      nr,
                      year,
                      beginning_year,
                      color_mode]

        return User(user_entry)

    def update_user_config(self, user, data):
        """
        Updates the user.db with new values (changed in /settings)
        Create db entry entirely from data (except uid)
        (this is only to preserve the db order)
        """

        db_entry = [data["name"],
                    data["surname"],
                    data["nickname"],
                    data["email"],
                    data["unit"],
                    data["week"],
                    data["nr"],
                    data["year"],
                    data["beginning_year"],
                    data["color_mode"],
                    user.uid]

        cursor, connection = self.get_cursor()

        cursor.execute(f"UPDATE {self.table_name} SET \
        name=?, surname=?, nickname=?, email=?, unit=?, week=?, nr=?, year=?, beginning_year=?, color_mode=? WHERE id=?",
                       db_entry)

        connection.commit()
        cursor.close()
        connection.close()

        # remove last element (uid) and insert at first position
        db_entry.insert(0, db_entry.pop())
        user.update_all(db_entry)

    def get_pw(self, email):
        """
        Return the password hash if the email is found in the database
        """
        cursor, connection = self.get_cursor()
        cursor.execute(f"SELECT pwd_and_salt FROM {self.table_name} WHERE email=?", (email,))
        return cursor.fetchone()[0]

    def get_user(self, email) -> object:
        """
        Gets all user data form db (except the password)
        and returns a new User obj.
        This is used in /login
        """
        # TODO: select all items that are needed, except pwd, and don't delete pwd later
        cursor, connection = self.get_cursor()
        del cursor
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE email=?", (email,))
        udict = dict(cursor.fetchall()[0])

        del connection.row_factory
        cursor.close()
        connection.close()
        del udict["pwd_and_salt"]

        return User(udict.values())

    def get_dict(self, email) -> dict:
        """
        Gets all user data form db (except the password)
        and returns a dict with the corresponding table headers.
        """
        # do the same as needed in get_user (don't fetch pwd from db)
        cursor, connection = self.get_cursor()
        del cursor
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE email=?", (email,))
        udict = dict(cursor.fetchall()[0])

        del connection.row_factory
        cursor.close()
        connection.close()
        del udict["pwd_and_salt"]
        return udict

    def email_exists(self, email):
        # check if email is already in db
        cursor, connection = self.get_cursor()
        cursor.execute(f"SELECT email FROM {self.table_name} WHERE email=?", (email,))
        return cursor.fetchone()

    def reset_to_default(self, user):
        cursor, connection = self.get_cursor()

        week = configs.START_WEEK
        nr = configs.NR
        year = configs.YEAR
        unit = configs.UNIT
        color_mode = Colormode.DARK

        user.update_defaults(week, nr, year, unit, color_mode)

        cursor.execute(f"UPDATE {self.table_name} SET \
                unit=?, week=?, nr=?, year=?, color_mode=? WHERE id=?", (unit, week, nr, year, color_mode, user.uid))
        connection.commit()
        cursor.close()
        connection.close()
        return user

    def update_color_mode(self, colormode, user):
        cursor, connection = self.get_cursor()
        cursor.execute(f"UPDATE {self.table_name} SET color_mode=? WHERE id=?", (colormode, user.uid))
        connection.commit()
        cursor.close()
        connection.close()

        user.update_color_mode(colormode)

    def get_data(self, user):
        """
        This fetches the needed info for /edit from the db
        """
        cursor, connection = self.get_cursor()
        cursor.execute(f"SELECT name, surname, unit, kw, nr, year FROM {self.table_name} WHERE id=?", (user.uid,))
        data = {"name": (cursor.fetchone())[0], "surname": (cursor.fetchone())[1], "unit": (cursor.fetchone())[2],
                "kw": (cursor.fetchone())[3], "nr": (cursor.fetchone())[4], "year": (cursor.fetchone())[5]}
        return data

    def increase_nr(self, user):
        """
        Increse number of contentdb records
        """
        cursor, connection = self.get_cursor()
        # fetch number from db
        cursor.execute(f"SELECT nr FROM {self.table_name} WHERE id=?", (user.uid,))
        nr = cursor.fetchone()
        # increase actual number
        nr = nr[0] + 1
        # write increased number back into db
        cursor.execute(f"UPDATE {self.table_name} SET nr=? WHERE id =?", (nr, user.uid))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def get_pw_by_nickname(self, nickname):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT pwd_and_salt FROM {self.table_name} WHERE nickname=?", (nickname,))
        pwd_and_salt = self.cursor.fetchone()
        if pwd_and_salt:
            return pwd_and_salt[0]
        else:
            return False

    def get_id_by_email(self, email):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE email=?", (email,))
        id = self.cursor.fetchone()
        if id:
            return id[0]
        else:
            return False

    def get_id_by_nickname(self, nickname):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE nickname=?", (nickname,))
        id = self.cursor.fetchone()
        if id:
            return id[0]
        else:
            return False

    def fetch_by_id(self, id):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, nickname, email FROM {self.table_name} WHERE id=?", (id,))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return False

    def get_name_nickname_by_email(self, email):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, nickname FROM {self.table_name} WHERE email =?", (email,))
        data = self.cursor.fetchone()
        return data

    def get_email_by_nickname(self, nickname):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT email FROM {self.table_name} WHERE nickname =?", (nickname,))
        data = self.cursor.fetchone()
        if data:
            return data[0]
        else:
            return False

    def get_name_email_by_nickname(self, nickname):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, email FROM {self.table_name} WHERE nickname =?", (nickname,))
        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return False

    def get_user_data(self, user):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT name, surname, unit, kw, nr, year FROM {self.table_name} WHERE id =?", (user.id,))
        data = {}
        data["name"], data["surname"], data["unit"], data["kw"], data["nr"], data["year"] = self.cursor.fetchone()
        return data

    def get_settings_data(self, user):
        self.cursor = self.get_cursor()
        self.cursor.execute(
            f"SELECT name, surname, nickname, email, unit, kw, nr, year FROM {self.table_name} WHERE id =?", (user.id,))
        data = {}
        data["name"], data["surname"], data["nickname"], data["email"], data["unit"], data["kw"], data["nr"], data[
            "year"] = self.cursor.fetchone()
        return data


class ContentDB:
    def __init__(self, uid):
        self.table_name = "content"
        self.uid = uid
        self.db_path = os.path.join(paths.USER_PATH, str(uid), paths.CONTENT_DB_PATH)
        self.initialize()

    def get_cursor(self):
        connection = sqlite3.connect(self.db_path)
        return connection.cursor(), connection

    def initialize(self):
        try:
            cursor, connection = self.get_cursor()
            cursor.execute(f"CREATE TABLE if not exists {self.table_name} \
            (id INTEGER PRIMARY KEY, \
            name TEXT, surname TEXT, \
            kw INTEGER, \
            nr INTEGER, \
            year INTEGER, \
            unit TEXT, \
            start TEXT, \
            end TEXT, \
            sign TEXT, \
            Bcontent TEXT, \
            Scontent TEXT, \
            BScontent TEXT)")  # changed date names!! (removed _date suffix)
            cursor.close()
            connection.close()
            return True

        except FileNotFoundError:
            print(f"Database file '{self.db_path}' not found!", file=sys.stderr)
            return False

    def add_record(self, uinput, data):
        week = week_from_html_date()  # rethink this later
        name = uinput["name"]
        surname = uinput["surname"]
        nr = uinput["nr"]
        year = uinput["year"]
        unit = uinput["unit"]
        start_date = uinput["start_date"]
        end_date = uinput["end_date"]
        sign_date = uinput["sign_date"]
        Bcontent = uinput["Bcontent"]
        Scontent = uinput["Scontent"]
        BScontent = uinput["BScontent"]
        self.cursor = self.get_cursor()
        self.cursor.execute(f"INSERT INTO {self.table_name}\
        (name, surname, kw, nr, year, unit, start_date, end_date, sign_date, Bcontent, Scontent, BScontent) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            name, surname, kw, nr, year, unit, start_date, end_date, sign_date, Bcontent, Scontent, BScontent))
        self.connection.commit()

    def get_all(self):
        cursor, connection = self.get_cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        content = cursor.fetchall()
        return content

    def get_content_by_id(self, id):
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE id=?", (id,))
        content = self.cursor.fetchone()
        return content

    def update(self, data, id):
        self.cursor = self.get_cursor()
        data = list(data)
        # append id to end of list (because of sql statment)
        data.append(id)
        self.cursor.execute(f"UPDATE {self.table_name} SET \
        name=?, surname=?, kw=?, nr=?, year=?, unit=?,\
        start_date=?, end_date=?, sign_date=?, Bcontent=?, \
        Scontent=?, BScontent=? WHERE id=?", (data))
        self.connection.commit()
