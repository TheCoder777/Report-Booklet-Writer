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


import pdfhandler, io, time, sys
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, request, redirect, send_file


app = Flask(__name__)


def writepdf(data, uinput):
    packet = io.BytesIO()
    packet = pdfhandler.draw(data, uinput, packet)
    packet.seek(0)
    return pdfhandler.compile(packet)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/edit")
def edit():
    data = pdfhandler.parse_config()
    data["sign_date"] = pdfhandler.get_a_date(type="html")
    start_date, end_date = pdfhandler.get_date(data["kw"], type="server")
    return render_template("edit.html", data=data, start_date=start_date, end_date=end_date)


@app.route("/edit", methods=["POST"])
def get_and_return():
    if request.method == "POST":
        uinput = dict(request.form.copy())
        del uinput["submit"]
        data = pdfhandler.parse_config()
        pdf = writepdf(data, uinput)
        pdfhandler.add_config_nr()
        return send_file(pdf, as_attachment=True)


@app.route("/settings")
def settings():
    data = pdfhandler.parse_config()
    return render_template("settings.html", data=data, action="none")


@app.route("/settings", methods=["POST"])
def get_new_config():
    if request.method == "POST":
        data = dict(request.form.copy())
        del data["submit"]
        try:
            pdfhandler.update_config(data)
            new_data = pdfhandler.parse_config()
            return render_template("settings.html", data=new_data, action="success")
        except FileNotFoundError as e:
            print(e, "problems occurred while trying to update config")
            return render_template("settings.html", data=data, action="fail")
        except:
            print(pdfhandler.Error_msg.UNKNOWN_ERR)


if __name__ == "__main__":
    HOST='localhost'
    PORT=8000
    
    pdfhandler.checkup()

    if len(sys.argv) > 1:
        if sys.argv[1] in ["--debug", "debug", "-d", "d"]:
            app.run(host=HOST, port=PORT, debug=True)  # for debugging
    else:
        print(f"\nRunning on http://{HOST}:{PORT}/\n")
        server = WSGIServer((HOST, PORT), app)
        server.serve_forever()
