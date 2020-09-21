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


import pdfhandler, confighandler, dbhandler, paths, io, time, sys, bcrypt
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, request, redirect, send_file, session, url_for
from flask_session import Session
from user import User

app = Flask(__name__)


def validate_pw(pw,hashandsalt):
    print(pw)
    print(pw.encode())
    print(hashandsalt)
    return bcrypt.checkpw(pw.encode(), hashandsalt)


def hashpw(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())


def pws_equal(pw1, pw2):
    if pw1 == pw2:
        return True
    else:
        return False


def writepdf(data, uinput):
    packet = io.BytesIO()
    packet = pdfhandler.draw(data, uinput, packet)
    packet.seek(0)
    return pdfhandler.compile(packet)


@app.route("/")
def index():
    # try:
    #     if session["user"]:
    #         return render_template("index.html", login=True)
    #     else:
    #         return render_template("index.html", login=False)
    # except KeyError:
    return render_template("index.html")


@app.route("/edit")
def edit():
    data = confighandler.parse_config()
    data["sign_date"] = pdfhandler.get_a_date(type="html")
    start_date, end_date = pdfhandler.get_date(data["kw"], type="server")
    return render_template("edit.html", data=data, start_date=start_date, end_date=end_date)


@app.route("/edit", methods=["POST"])
def get_and_return():
    if request.method == "POST":
        uinput = dict(request.form.copy())
        del uinput["submit"]
        data = confighandler.parse_config()
        pdf = writepdf(data, uinput)
        confighandler.add_config_nr()
        return send_file(pdf, as_attachment=True)


@app.route("/settings")
def settings():
    data = confighandler.parse_config()
    return render_template("settings.html", data=data, action="none")


@app.route("/settings", methods=["POST"])
def get_new_config():
    if request.method == "POST":
        data = dict(request.form.copy())

        try:
            if data["hard_reset"]:
                confighandler.reset_config()
                new_data = confighandler.parse_config()
                return render_template("settings.html", data=new_data, action="success_reset")
        except KeyError:
            del data["submit"]
        except:
            print(pdfhandler.Error_msg.UNKNOWN_ERR)
        try:
            confighandler.update_config(data)
            new_data = confighandler.parse_config()
            return render_template("settings.html", data=new_data, action="success")
        except FileNotFoundError as e:
            print(e, "problems occurred while trying to update config")
            return render_template("settings.html", data=data, action="fail")
        except:
            print(pdfhandler.Error_msg.UNKNOWN_ERR)
            return render_template("settings.html", data=data, action="fail")


@app.route("/login")
def login():
    return render_template("security/login.html")


@app.route("/login", methods=["POST"])
def user_login():
    if request.method == "POST":
        try:
            if request.form["login"]:
                email = request.form["name"]
                hashandsalt = UserDB.getpw(email)
                if not hashandsalt:
                    return render_template("security/login.html", notify="nouser")
                if validate_pw(str(request.form["password"]), hashandsalt):
                    session["user"] = User(email)
                    return redirect(url_for("index"))
                else:
                    return render_template("security/login.html", notify="failed")
        except KeyError:
            return render_template("security/login.html", notify="failed")


@app.route("/register")
def register():
    return render_template("security/register.html")


@app.route("/register", methods=["POST"])
def get_user():
    if request.method == "POST":
        # try:
        #     if request.form["use_as_guest"]:
        #         pass
        # except KeyError:
        #     pass
        try:
            if request.form["register"]:
                name = request.form["name"]
                surname = request.form["surname"]
                email = request.form["email"]
                if pws_equal(request.form["password"], request.form["password_re"]):
                    pwd_and_salt = hashpw(request.form["password"])
                    UserDB.add_user(name, surname, email, pwd_and_salt)
                    session["user"] = User(email)
                    return render_template("security/register.html", notify="success")
        except KeyError:
            return render_template("security/register.html", notify="failed")


@app.route("/logout")
def logout():
    del session["user"]
    return redirect(url_for("index"))


@app.route("/forgot-password")
def forgot_password():
    return render_template("security/forgot_password.html")


@app.route("/change-password")
def change_password():
    return render_template("security/change_password.html")


if __name__ == "__main__":
    HOST='localhost'
    PORT=8000
    SESSION_TYPE="filesystem"
    SESSION_FILE_DIR=paths.COOKIE_PATH
    app.config.from_object(__name__)
    Session(app)

    pdfhandler.checkup()
    UserDB = dbhandler.UserDB()

    if len(sys.argv) > 1:
        if sys.argv[1] in ["--debug", "debug", "-d", "d"]:
            app.run(host=HOST, port=PORT, debug=True)  # for debugging
    else:
        print(f"\nRunning on http://{HOST}:{PORT}/\n")
        server = WSGIServer((HOST, PORT), app)
        server.serve_forever()
