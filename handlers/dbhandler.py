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
        "unit": configs.UNIT
    }


def edit_defaults(year):
    return datecalc.calc_user_defaults(int(year))


def quickedit_data(year, week):
    """
    Calculates all values needed to export the final pdf
    """
    return datecalc.calc_all(int(year), int(week))


def edit_data(year, beginning_year, week, start_week):
    """
    Calculates /edit values for logged in users
    """
    return datecalc.calc_all(int(year), int(week), int(beginning_year), int(start_week))


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
            start_week INTEGER, \
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
        start_week = configs.START_WEEK
        year = configs.YEAR
        beginning_year = datecalc.calc_beginning_year()
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
                    start_week,
                    year,
                    beginning_year,
                    color_mode]

        # add user to db
        cursor.execute(f"INSERT INTO {self.table_name}\
        (name, surname, nickname, email, pwd_and_salt, unit, week, start_week, year, beginning_year, color_mode) \
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
                      start_week,
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
                    data["start_week"],
                    data["year"],
                    data["beginning_year"],
                    data["color_mode"],
                    user.uid]

        cursor, connection = self.get_cursor()

        cursor.execute(f"UPDATE {self.table_name} SET \
        name=?, \
        surname=?, \
        nickname=?, \
        email=?, \
        unit=?, \
        week=?, \
        start_week=?, \
        year=?, \
        beginning_year=?, \
        color_mode=? WHERE id=?", db_entry)

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
        start_week = configs.START_WEEK
        year = configs.YEAR
        # This only resets beginning_year to the current year
        beginning_year = datecalc.calc_beginning_year()
        unit = configs.UNIT
        color_mode = Colormode.DARK

        user.update_defaults(week, start_week, year, unit, color_mode)

        cursor.execute(f"UPDATE {self.table_name} SET \
                       unit=?, week=?, start_week=?, year=?, beginning_year=?, color_mode=? WHERE id=?",
                       (unit, week, start_week, year, beginning_year, color_mode, user.uid))
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


class ContentDB:
    def __init__(self, uid):
        self.table_name = "content"
        self.uid = uid
        # ever user has his own contentdb
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
            week INTEGER, \
            year INTEGER, \
            unit TEXT, \
            sign TEXT, \
            Bcontent TEXT, \
            Scontent TEXT, \
            BScontent TEXT)")
            cursor.close()
            connection.close()
            return True

        except FileNotFoundError:
            print(f"Database file '{self.db_path}' not found!", file=sys.stderr)
            return False

    def add_record(self, data):
        cursor, connection = self.get_cursor()

        cursor.execute(f"INSERT INTO {self.table_name}\
        (name, surname, week, year, unit, sign, Bcontent, Scontent, BScontent) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            data["name"],
            data["surname"],
            data["week"],
            data["year"],
            data["unit"],
            data["sign"],
            data["Bcontent"],
            data["Scontent"],
            data["BScontent"]))
        connection.commit()
        cursor.close()
        connection.close()

    def get_all(self):
        cursor, connection = self.get_cursor()

        # fetch everything from the database
        query = cursor.execute(f"SELECT * FROM {self.table_name}")
        # get the names from the table headers
        colnames = [d[0] for d in query.description]
        results = []
        for row in cursor:
            # merge table headers and actual row together
            results.append(dict(zip(colnames, row)))
        return results

    def get_content_by_id(self, cid):
        # initialize cursor with a row_factory
        cursor, connection = self.get_cursor()
        del cursor
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        # get specified record from db using content id
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE id=?", (cid,))
        content = dict(cursor.fetchall()[0])
        cursor.close()
        connection.close()
        return content

    def update(self, data, cid):
        cursor, connection = self.get_cursor()
        db_entry = [
            data["name"],
            data["surname"],
            data["week"],
            data["year"],
            data["unit"],
            data["sign"],
            data["Bcontent"],
            data["Scontent"],
            data["BScontent"],
            cid]

        cursor.execute(f"UPDATE {self.table_name} SET \
        name=?, \
        surname=?, \
        week=?, \
        year=?, \
        unit=?,\
        sign=?, \
        Bcontent=?, \
        Scontent=?, \
        BScontent=? WHERE id=?", db_entry)

        connection.commit()
        cursor.close()
        connection.close()
