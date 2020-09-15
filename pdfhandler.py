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


import io, os, time, configparser
from datetime import date
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from textwrap import wrap
from colored import attr, fg

CONFIG_PATH = "./config.ini"
TMP_PATH = "./tmp/"
TEMPLATE_PATH = "Berichtsheft_template.pdf"

# colors
RESET = attr("reset")
BOLD = attr(1)
ERROR = fg(1)
WARNING = fg(214)
SUCCESS = fg(2)

def draw(data, uinput, packet):
    LINE_DISTANCE = 30
    nr = int(data["nr"])
    nr -= 1
    kw = data["beginn"]
    kw = int(kw)
    kw = (kw + nr) % 52
    fullname = data["surname"] + " " + data["name"]

    a_year = int(time.strftime("%Y"))
    start_date = date.fromisocalendar(a_year, kw, 1)
    start_date = start_date.strftime("%d.%m.%Y")
    end_date = date.fromisocalendar(a_year, kw, 5)
    end_date = end_date.strftime("%d.%m.%Y")

    a_date = time.strftime("%d.%m.%Y")

    c = canvas.Canvas(packet, pagesize=A4)

    c.drawString(313, 795, fullname)
    c.drawString(386, 778, data["unit"])
    c.drawString(231, 748, str(nr + 1))
    c.drawString(260, 748, start_date)
    c.drawString(365, 748, end_date)
    c.drawString(530, 748, data["year"])

    # Betrieblich
    height = 680
    bcontent = uinput["Bcontent"].split("\n")
    for cont in bcontent:
        t = c.beginText()
        bcontent = "\n".join(wrap(cont, 80))
        t.setTextOrigin(60, height)
        t.textLines(bcontent)
        c.drawText(t)
        height -= LINE_DISTANCE

    # Schulungen
    height = 515
    scontent = uinput["Scontent"].split("\n")
    for scont in scontent:
        st = c.beginText()
        scontent = "\n".join(wrap(scont, 80))
        st.setTextOrigin(60, height)
        st.textLines(scontent)
        c.drawText(st)
        height -= LINE_DISTANCE

    # Berufschule
    height = 302
    bscontent = uinput["BScontent"].split("\n")
    for bscont in bscontent:
        bt = c.beginText()
        bscontent = "\n".join(wrap(bscont, 80))
        bt.setTextOrigin(60, height)
        bt.textLines(bscontent)
        c.drawText(bt)
        height -= LINE_DISTANCE

    c.drawString(95, 148, a_date)
    c.drawString(260, 148, a_date)
    c.drawString(430, 148, a_date)
    c.save()
    return packet


def parse_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    try:
        data = {}
        for c in config.sections():
            for v in config[c].items():
                data[v[0]] = v[1]
        return data
    except:
        pass


def add_config_nr():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    config["date"]["nr"] = str(int(config["date"]["nr"]) + 1)
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def compile(packet):
    new_pdf = PdfFileReader(packet)
    template = PdfFileReader(open(TEMPLATE_PATH, "rb"))
    out = PdfFileWriter()
    page = template.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    out.addPage(page)
    # filename = "./tmp/" + str(time.strftime("%H-%M_%d%m%Y")) + ".pdf"  # for unique filenames
    filename = TMP_PATH + "save.pdf"
    out_stream = open(filename, "wb")
    out.write(out_stream)
    out_stream.close()
    return filename


def checkup():
    start_time = time.time()
    console = BOLD + "[CHECKUP] " + RESET
    print()

    if not os.path.isdir(TMP_PATH):
        print(console + f"Temporary save directory {TMP_PATH} doesn't exist...", end="")
        os.mkdir(TMP_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "Temporary directory found!" + RESET)

    if not os.path.exists(TEMPLATE_PATH):
        print(console + ERROR + "Template not found! Please add a template!" + RESET)
        sys.exit(1)
    else:
        print(console + SUCCESS + "Template found!" + RESET)

    # garbadge cleaning
    filelist = [f for f in os.listdir(TMP_PATH) if f.endswith(".pdf")]
    if filelist:
        print(console + "Cleaning cache...")
        for f in filelist:
            print(WARNING + "\tremoving: " + os.path.join(TMP_PATH, f) + "..." + RESET, end="")
            os.remove(os.path.join(TMP_PATH, f))
            print(SUCCESS + "done!" + RESET)
    else:
        print(console + SUCCESS +  "Cache is clean!" + RESET)
    diff = time.time() - start_time

    print(console + BOLD + SUCCESS + f"Checkup finished succuessfully in {diff:.4f} seconds!\n" + RESET)
