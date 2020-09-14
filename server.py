import pdfhandler, io, time
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
    return render_template("edit.html")


@app.route("/edit", methods=["POST"])
def get_and_return():
    if request.method == "POST":
        uinput = dict(request.form.copy())
        del uinput["submit"]
        data = pdfhandler.parse_config()
        pdf = writepdf(data, uinput)
        return send_file(pdf, as_attachment=True)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8000, debug=True)  # for debugging
    server = WSGIServer(('localhost', 8000), app)
    server.serve_forever()
