#!/usr/bin/env python3.8

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
import bcrypt
import os
import re
import sys
import time
import functools

#  flask modules and extensions
from flask import Flask, render_template, request, redirect, send_file, session, url_for, abort
from flask_session import Session

#  WSGI server for better performance
from gevent.pywsgi import WSGIServer

# load internal modules
from defines.colors import RESET, BOLD, ERROR, WARNING, SUCCESS
from defines.colormode import Colormode
from defines import paths
from defines import messages
from handlers import pdfhandler, todolisthandler, dbhandler
from models.messagequeue import MessageQueue


def checkup():
    """
    Global checkup for all files and dirs
    If this doesn't succeed, the server will NOT start!
    """

    start_time = time.time()
    console = BOLD + "[CHECKUP] " + RESET
    print()

    if not os.path.isdir(paths.TMP_PATH):
        print(console + f"Temporary save directory {paths.TMP_PATH} doesn't exist...", end="")
        os.mkdir(paths.TMP_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "Temporary directory found!" + RESET)

    if not os.path.isdir(paths.COOKIE_PATH):
        print(console + f"Cookie directory {paths.COOKIE_PATH} doesn't exist...", end="")
        os.mkdir(paths.COOKIE_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "Cookie directory found!" + RESET)

    if not os.path.isdir(paths.DB_PATH):
        print(console + f"DB directory {paths.DB_PATH} doesn't exist...", end="")
        os.mkdir(paths.DB_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "DB directory found!" + RESET)

    if not os.path.isdir(paths.USER_PATH):
        print(console + f"User directory {paths.USER_PATH} doesn't exist...", end="")
        os.mkdir(paths.USER_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "User directory found!" + RESET)

    if not os.path.exists(paths.PDF_TEMPLATE_PATH):
        print(console + ERROR + "PDF Template not found! Please add a pdf template!" + RESET)
        sys.exit(1)
    else:
        print(console + SUCCESS + "PDF Template found!" + RESET)

    if not os.path.exists(paths.TODOLIST_TEMPLATE_PATH):
        print(console + ERROR + "Todolist template not found! Please add a todolist template!" + RESET)
        sys.exit(1)
    else:
        print(console + SUCCESS + "Todolist template found!" + RESET)

    # garbage cleaning (delete all pdf in tmp file)
    filelist = [f for f in os.listdir(paths.TMP_PATH) if f.endswith(".pdf")]
    if filelist:
        print(console + "Cleaning cache...")
        for f in filelist:
            print(WARNING + "\tremoving: " + os.path.join(paths.TMP_PATH, f) + "..." + RESET, end="")
            os.remove(os.path.join(paths.TMP_PATH, f))
            print(SUCCESS + "done!" + RESET)
    else:
        print(console + SUCCESS + "Cache is clean!" + RESET)

    # Calculate time difference (just because we can)
    diff = time.time() - start_time

    print(console + BOLD + SUCCESS + f"Checkup finished successfully in {diff:.4f} seconds!\n" + RESET)


app = Flask(__name__)


def login_required(func):
    """
    Decorator for pages that need a login
    (redirects to login if not logged in)
    """

    @functools.wraps(func)
    def login_wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return login_wrapper


@app.route("/")
def index():
    if session.get("user"):
        return redirect("user")

    return render_template("index.html")


@app.before_request
def set_color_mode():
    # setting default colormode for new users if not already set
    if not session.get("color_mode") and not session.get("user"):
        session["color_mode"] = Colormode.DARK


@app.route("/change-mode")
def change_mode():
    """
    This function switches between the Dark and the Light color mode.
    (Defaults to Darkmode)
    """
    if session.get("user"):
        # delete color cookie if he exists
        if session.get("color_mode"):
            del session["color_mode"]

        # if user is logged in and colormode is DARK
        if session["user"].color_mode == Colormode.DARK:
            # update database
            UserDB.update_color_mode(Colormode.LIGHT, session.get("user"))
            # update user
            session["user"].update_color_mode(Colormode.LIGHT)
            return redirect(request.referrer)

        # if user is logged in and colormode is LIGHT
        if session["user"].color_mode == Colormode.LIGHT:
            # update database
            UserDB.update_color_mode(Colormode.DARK, session.get("user"))
            # update user
            session["user"].update_color_mode(Colormode.DARK)
            return redirect(request.referrer)

    # user isn't logged in and colormode is DARK
    elif session.get("color_mode") == Colormode.DARK:
        session["color_mode"] = Colormode.LIGHT
        return redirect(request.referrer)
    else:
        session["color_mode"] = Colormode.DARK
        return redirect(request.referrer)


@app.route("/quickedit")
def quickedit():
    # Check if user is logged in (maybe somehow?)
    if session.get("user"):
        redirect(url_for("edit"))
    # calls a db function that returns the values from defines.configs
    # as dict (also calculates current week and so on)
    defaults = dbhandler.quickedit_defaults()
    return render_template("quickedit.html", data=defaults)


@app.route("/quickedit", methods=["POST"])
# TODO: add checkups for date validation and stuff like 'if name given' (/quickedit)
def quickedit_reload():
    if request.form.get("download"):
        # Download button is pressed
        defaults = dict(request.form.copy())
        if int(defaults["week"]) >= 53:
            # TODO: count year up if week is too high
            msg = MessageQueue()
            msg.add(messages.INVALID_CALENDER_WEEK)
            return render_template("quickedit.html", data=defaults, msg=msg.get())
        data = dbhandler.quickedit_data(defaults.get("year"),
                                        defaults.get("week"))
        data = {**defaults, **data}
        # TODO: set attachment_filename to save_week_xx.pdf (maybe?)
        # Note that this needs a week here
        return send_file(pdfhandler.writepdf(data),
                         mimetype="application/pdf",
                         attachment_filename="save.pdf",
                         as_attachment=True)
    # TODO: make a defines.errors.py (name ok?) with NOT_IMPLEMENTED / BAD_REQUEST enums
    # raise 'not implemented' error on bad request (or maybe 400 for bad request?)
    abort(501)


# Login/Register related functions


def is_email(email):
    # Email regex (x@x.x where x is element from all characters)
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def is_password(pw):
    # Password regex
    # - 8 characters (at least 1 Uppercase)
    # - one number
    # - one special character (from !"#$%&'()*+,-./:;<=>?@[\]\^_`{|}~)
    return re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*?\d)(?=.*?[!\"#$%&\'()*+,-./:;<=>?@[\]\\^_`{|}~]).{8,}$", pw)


def validate_pw(pw, hashandsalt):
    return bcrypt.checkpw(pw.encode(), hashandsalt)


def hashpw(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())


def pws_equal(pw1, pw2):
    if pw1 == pw2:
        return True
    else:
        return False


def check_register_credentials(credentials):
    # List for missing credentials (for the msg system)
    msg = MessageQueue()

    # validate name/surname (not empty)
    if not len(credentials["name"]) > 0:
        msg.add(messages.MISSING_NAME)
    if not len(credentials["surname"]) > 0:
        msg.add(messages.MISSING_SURNAME)

    # Check if email exists
    if not len(credentials["email"]) > 0:
        msg.add(messages.MISSING_EMAIL)

    # check email with regex
    elif not is_email(credentials["email"]):
        msg.add(messages.INVALID_EMAIL)

    # chek if email is already in db
    elif UserDB.email_exists(credentials["email"]):
        msg.add(messages.EMAIL_ALREADY_EXISTS)

    # check if password is given
    if not len(credentials["password"]) > 0:
        msg.add(messages.MISSING_PASSWORD)
    # check password match
    elif not is_password(credentials["password"]):
        msg.add(messages.UNFULFILLED_PASSWORD_REQUIREMENTS)

    # check if passwords are equal
    if not pws_equal(credentials["password"], credentials["password_re"]):
        msg.add(messages.PASSWORD_MISMATCH)

    return msg


def check_login_credentials(credentials):
    # Same as check_register_credentials, but for login
    msg = MessageQueue()

    if not len(credentials["email"]) > 0:
        msg.add(messages.MISSING_EMAIL)

    elif not is_email(credentials["email"]):
        msg.add(messages.INVALID_EMAIL)

    elif not UserDB.email_exists(credentials["email"]):
        msg.add(messages.EMAIL_DOESNT_EXIST)

    if not len(credentials["password"]) > 0:
        msg.add(messages.MISSING_PASSWORD)

    return msg


# REGISTER


@app.route("/register")
def register():
    return render_template("security/register.html")


@app.route("/register", methods=["POST"])
# TODO: strip whitespace before and after usernames (also in login)
def get_user():
    # Check if the register button is pressed (this will be a 'next' button soon)
    if request.form.get("register"):
        # copy the user credentials to a python dict and check them
        credentials = dict(request.form.copy())
        msg = check_register_credentials(credentials)
        if msg.is_empty():
            # create a password hash
            pwd_and_salt = hashpw(request.form["password"])
            session["user"] = UserDB.new_user(credentials, pwd_and_salt)
            return redirect(url_for("user"))
        else:
            return render_template("security/register.html", data=credentials, msg=msg.get())
    # Check if the "Use as guest" button is pressed
    elif request.form.get("use_as_guest"):
        return redirect(url_for("edit"))


# LOGIN


@app.route("/login")
def login():
    return render_template("security/login.html")


@app.route("/login", methods=["POST"])
def user_login():
    # Check if the Login Button is pressed
    if request.form.get("login"):
        # copy the user credentials to a python dict and check them
        credentials = dict(request.form.copy())
        msg = check_login_credentials(credentials)
        if msg.is_empty():
            hash_and_salt = UserDB.get_pw(credentials["email"])
            # validate password with hash from db
            if not validate_pw(credentials["password"], hash_and_salt):
                msg.add(messages.INVALID_PASSWORD)
                return render_template("security/login.html", data=credentials, msg=msg.get())
            # Login user
            session["user"] = UserDB.get_user(credentials["email"])
            return redirect(url_for("user"))
        print(credentials)
        return render_template("security/login.html", data=credentials, msg=msg.get())
    # Check if the "Use as guest" button is pressed
    elif request.form.get("use_as_guest"):
        return redirect(url_for("edit"))
    # Check if the "Forgot password" button is pressed
    elif request.form.get("forgot_password"):
        return redirect(url_for("forgot_password"))


@app.route("/logout")
# can only logout if logged in
@login_required
def logout():
    # Logout user
    del session["user"]
    return redirect(url_for("index"))


@app.route("/user")
@login_required
def user():
    return render_template("user.html")


@app.route("/edit")
@login_required
def edit():
    # get all user data that's available
    data = UserDB.get_dict(session["user"].email)
    # get dynamic content (year, sign date)
    calculated = dbhandler.edit_defaults(data.get("year"))

    contentdb = dbhandler.ContentDB(session["user"].uid)

    # calculate week and make a dict out of it
    week = {"week": contentdb.count_rows() + data.get("week")}

    # merge them together
    # this merges data, the new calculated data and the precalculated week
    data = {**data, **calculated, **week}

    # this is for custom edits (db entries from contentdb)
    # if an id to a custom edit is provided:
    if request.args.get("id"):
        contentdb = dbhandler.ContentDB(session["user"].uid)
        data = contentdb.get_by_id(request.args.get("id"))
        # TODO: add a Download button to the custom page (to make single exports possible)
        # TODO: add a mask to select the weeks from which to export (custom export range)
        return render_template("customedit.html", data=data)

    return render_template("edit.html", data=data)


@app.route("/edit", methods=["POST"])
@login_required
def edit_reload():
    # TODO: add checkups for date vailidation and stuff like 'if name given' (/edit)
    if request.form.get("download"):
        data = dict(request.form.copy())

        contentdb = dbhandler.ContentDB(session["user"].uid)
        contentdb.add_record(data)

        data = {**data, **dbhandler.edit_data(data.get("year"),
                                              session["user"].beginning_year,
                                              data.get("week"),
                                              session["user"].start_week)}

        return send_file(pdfhandler.writepdf(data),
                         mimetype="application/pdf",
                         attachment_filename="save.pdf",
                         as_attachment=True)

    elif request.form.get("save"):
        # only save the record to contentdb, but don't download or export anything to PDF
        data = dict(request.form.copy())

        contentdb = dbhandler.ContentDB(session["user"].uid)
        contentdb.add_record(data)
        return redirect(url_for("content_overview"))

    # we'll find out what to do about this here later:
    elif request.form.get("save_custom"):
        # only update the record in the contentdb
        data = dict(request.form.copy())
        contentdb = dbhandler.ContentDB(session["user"].uid)
        contentdb.update(data, request.args.get("id"))
        return redirect(url_for("content_overview"))

    else:
        # raise 'not implemented' error on bad request (or maybe 400 for bad request?)
        abort(501)


def validate_settings(data):
    msg = MessageQueue()
    # TODO: validate date format, email change, ...
    return msg


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", user=session.get("user"))


@app.route("/settings", methods=["POST"])
@login_required
def update_settings():
    if request.form.get("save"):
        data = dict(request.form.copy())
        msg = validate_settings(data)
        if msg.is_empty():
            del data["save"]
            UserDB.update_user_config(session.get("user"), data)
            msg.add(messages.SAVED_SETTINGS)
            return render_template("settings.html", user=session.get("user"), msg=msg.get())
        # TODO: add render_template if settings not validate (some wrong email entered)
    elif request.form.get("hard_reset"):
        msg = MessageQueue()
        UserDB.reset_to_default(session.get("user"))
        msg.add(messages.RESET_USER_TO_DEFAULT)
        return render_template("settings.html", user=session.get("user"), msg=msg.get())


@app.route("/forgot-password")
@login_required
def forgot_password():
    return render_template("security/forgot_password.html")


@app.route("/change-password")
@login_required
def change_password():
    return render_template("security/change_password.html")


@app.route("/todolist")
@login_required
def todolist():
    return render_template("todolist.html", data=todolisthandler.open_todolist(session["user"].uid))


@app.route("/todolist", methods=["POST"])
@login_required
def todolist_save():
    df = todolisthandler.open_todolist(session["user"].uid)
    data = dict(request.form.copy())
    if data.get("save"):
        # Save button is pressed
        # TODO: if a parent todo is uncheckd again, uncheck all child elements too
        df, msg = todolisthandler.update(session["user"].uid, df, data.keys())
        return render_template("todolist.html", data=df, msg=msg.get())
    # raise 'not implemented' error on bad request (or maybe 400 for bad request?)
    abort(501)


@app.route("/content-overview")
@login_required
def content_overview():
    if request.args.get("delete"):
        # the delete button/link was pressed
        cid = request.args.get("delete")
        week = request.args.get("week")
        msg = MessageQueue()

        # init contentdb
        contentdb = dbhandler.ContentDB(session["user"].uid)

        # delete row with that content id
        if contentdb.delete_by_id(cid):
            msg.add(messages.custom_success(f"Successfully deleted Berichtsheft from week {week}"))
        return render_template("content_overview.html", content=contentdb.get_all(), msg=msg.get())

    # initialize content db with user id
    contentdb = dbhandler.ContentDB(session["user"].uid)
    return render_template("content_overview.html", content=contentdb.get_all())


@app.route("/content-overview", methods=["POST"])
@login_required
def content_overview_export():
    # TODO: add a button 'continue editing' or 'edit another one to make the workflow easier
    # TODO: add a delete button for all
    # TODO: add a big plus button in the form of a content card at the end of the list
    if request.form.get("export"):
        contentdb = dbhandler.ContentDB(session["user"].uid)

        # get entire database
        data = contentdb.get_all()

        # calculate start/end dates for all
        result = []
        for row in data:
            result.append({**row, **dbhandler.edit_data(row.get("year"),
                                                        session["user"].beginning_year,
                                                        row.get("week"),
                                                        session["user"].start_week)})

        return send_file(pdfhandler.write_many_pdfs(result),
                         mimetype="application/pdf",
                         attachment_filename="all.pdf",
                         as_attachment=True)


# TODO: add a @app.errorhandler(404) page


if __name__ == "__main__":
    # TODO: make a server config file in root for HOST and PORT (and maybe debug ?)
    # TODO: make a installer to install deps on server start (if not found)
    # TODO: add --clean/-c flag to delete all db/user/tmp files at startup, but ask for confirmation
    # TODO: maybe add a --reload flag to load cookies, and make it standard to delete cookies at startup?
    HOST = 'localhost'
    PORT = 8000
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = paths.COOKIE_PATH
    app.config.from_object(__name__)
    Session(app)
    checkup()
    UserDB = dbhandler.UserDB()
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--debug", "debug", "-d", "d"]:
            app.run(host=HOST, port=PORT, debug=True)  # for debugging
    else:
        print(f"\nRunning on http://{HOST}:{PORT}/\n")
        server = WSGIServer((HOST, PORT), app)
        server.serve_forever()
