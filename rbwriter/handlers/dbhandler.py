
# system modules
import os
import sqlite3
import sys

# internal modules
from . import datehandler
from ..defines import configs, paths
from ..defines.colormode import Colormode
from ..models.user import User


def quickedit_defaults():
    """
    Calculates the default /quickedit values, if they aren't returned (re-calculated)
    """
    return {
        # calculate start/end with given values for anonymous user
        "sign": datehandler.calc_sign_date(),
        "year": datehandler.get_current_year(),
        "week": datehandler.get_current_week(),
        "unit": configs.UNIT
    }


def edit_defaults(year):
    return datehandler.calc_user_defaults(int(year))


def quickedit_data(year, week):
    """
    Calculates all values needed to export the final pdf
    """
    return datehandler.calc_all(int(year), int(week))


def edit_data(year, beginning_year, week, start_week):
    """
    Calculates /edit values for logged in users
    """
    return datehandler.calc_all(int(year), int(week), int(beginning_year), int(start_week))


class UserDB:
    # TODO: unify all comments (""" """/ #)
    def __init__(self):
        self.db_path = paths.USER_DB_PATH
        self.initialize()

    def get_cursor(self):
        connection = sqlite3.connect(self.db_path)
        return connection.cursor(), connection

    def initialize(self):
        try:
            cursor, connection = self.get_cursor()

            cursor.execute("CREATE TABLE if not exists users \
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

    def new_user(self, cr, pwd):
        cursor, connection = self.get_cursor()

        # default nickname is the username
        nickname = cr["name"]
        # get defaults from config
        week = configs.START_WEEK
        start_week = configs.START_WEEK
        year = configs.YEAR
        beginning_year = datehandler.calc_beginning_year()
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
        cursor.execute("INSERT INTO users\
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

        cursor.execute("UPDATE users SET \
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
        cursor.execute("SELECT pwd_and_salt FROM users WHERE email=?", (email,))
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
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
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
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        udict = dict(cursor.fetchall()[0])

        del connection.row_factory
        cursor.close()
        connection.close()
        del udict["pwd_and_salt"]
        return udict

    def email_exists(self, email):
        # check if email is already in db
        cursor, connection = self.get_cursor()
        cursor.execute("SELECT email FROM users WHERE email=?", (email,))
        return cursor.fetchone()

    def reset_to_default(self, user):
        cursor, connection = self.get_cursor()

        week = configs.START_WEEK
        start_week = configs.START_WEEK
        year = configs.YEAR
        # This only resets beginning_year to the current year
        beginning_year = datehandler.calc_beginning_year()
        unit = configs.UNIT
        color_mode = Colormode.DARK

        user.update_defaults(week, start_week, year, unit, color_mode)

        cursor.execute("UPDATE users SET \
                       unit=?, week=?, start_week=?, year=?, beginning_year=?, color_mode=? WHERE id=?",
                       (unit, week, start_week, year, beginning_year, color_mode, user.uid))
        connection.commit()
        cursor.close()
        connection.close()
        return user

    def update_color_mode(self, colormode, user):
        cursor, connection = self.get_cursor()
        cursor.execute("UPDATE users SET color_mode=? WHERE id=?", (colormode, user.uid))
        connection.commit()
        cursor.close()
        connection.close()


class ContentDB:
    def __init__(self, uid):
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
            cursor.execute("CREATE TABLE if not exists content \
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

        cursor.execute("INSERT INTO content \
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
        query = cursor.execute("SELECT * FROM content ORDER BY week ASC")
        # get the names from the table headers
        colnames = [d[0] for d in query.description]
        results = []
        for row in cursor:
            # merge table headers and actual row together
            results.append(dict(zip(colnames, row)))
        return results

    def get_by_id(self, cid):
        # initialize cursor with a row_factory
        cursor, connection = self.get_cursor()
        del cursor
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        # get specified record from db using content id
        cursor.execute("SELECT * FROM content WHERE id=?", (cid,))
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

        cursor.execute("UPDATE content SET \
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

    def delete_by_id(self, cid):
        cursor, connection = self.get_cursor()
        cursor.execute("DELETE FROM content WHERE id=?", (cid,))
        return connection.commit()

    def count_rows(self) -> int:
        cursor, connection = self.get_cursor()
        cursor.execute("SELECT id from content ORDER BY id DESC LIMIT 1")
        res = cursor.fetchone()
        if res:
            return res[0]
        # return 0 db records if there aren't any
        return 0
