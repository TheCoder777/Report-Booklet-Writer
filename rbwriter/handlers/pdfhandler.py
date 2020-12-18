
# system modules
import io
import re
from textwrap import wrap

# external modules
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# internal modules
from ..defines import paths
from ..defines.configs import LINE_DISTANCE


def validate_html_date(html_date):
    """
    Validates a date (yyyy-mm-dd) roughly
    (yes, it's not the greatest date validation ever)
    """
    if re.match(r"[\d][\d][\d][\d]-[\d]?[\d]-[\d]?[\d]", html_date):
        year, month, day = html_date.split("-")
        if not int(year) > 1500:
            return False
        if not int(month) < 12:
            return False
        if not int(day) < 32:
            return False
        # only if nothing returned False
        return True
    else:
        return False


def validate_print_date(html_date):
    # TODO: rename html_date to print_date
    """
    Validates a date for display on the frontend.
    This should be an exact match of dd.mm.yyyy
    """
    return re.match(r"[\d][\d].[\d][\d].[\d][\d][\d][\d]", html_date)


def __convert_to_print_date(html_date):
    return ".".join([html_date.split("-")[2],
                     html_date.split("-")[1],
                     html_date.split("-")[0]])


def reformat_html_to_print(html_date: str) -> str:
    # reformats and validates html and print date
    if validate_html_date(html_date):
        print_date = __convert_to_print_date(html_date)
        if validate_print_date(print_date):
            return print_date
    # return empty string if something goes wrong
    # (so that the user has the option to manually change it later)
    return ""


def draw(data, packet):
    # generate full name
    fullname = data.get("surname") + ", " + data.get("name")

    c = canvas.Canvas(packet, pagesize=A4)

    # reformat for printing
    start_date = reformat_html_to_print(data.get("start"))
    end_date = reformat_html_to_print(data.get("end"))
    sign_date = reformat_html_to_print(data.get("sign"))
    # TODO: convert first into single variables like nr, year.. then draw
    # Don't ever touch these coordinates I dare you!
    c.drawString(313, 795, fullname)
    c.drawString(386, 778, data.get("unit"))
    c.drawString(231, 748, str(data.get("nr")))
    c.drawString(260, 748, start_date)
    c.drawString(365, 748, end_date)
    c.drawString(530, 748, str(data.get("year")))

    # Betrieblich
    height = 680
    bcontent = data.get("Bcontent").split("\n")
    for cont in bcontent:
        t = c.beginText()
        bcontent = "\n".join(wrap(cont, 80))
        t.setTextOrigin(60, height)
        t.textLines(bcontent)
        c.drawText(t)
        height -= LINE_DISTANCE

    # Schulungen
    height = 515
    scontent = data.get("Scontent").split("\n")
    for scont in scontent:
        st = c.beginText()
        scontent = "\n".join(wrap(scont, 80))
        st.setTextOrigin(60, height)
        st.textLines(scontent)
        c.drawText(st)
        height -= LINE_DISTANCE

    # Berufsschule
    height = 302
    bscontent = data.get("BScontent").split("\n")
    for bscont in bscontent:
        bt = c.beginText()
        bscontent = "\n".join(wrap(bscont, 80))
        bt.setTextOrigin(60, height)
        bt.textLines(bscontent)
        c.drawText(bt)
        height -= LINE_DISTANCE

    c.drawString(95, 148, sign_date)
    c.drawString(260, 148, sign_date)
    c.drawString(430, 148, sign_date)
    c.save()
    return packet


def compile_packet(packet):
    new_pdf = PdfFileReader(packet)
    template = PdfFileReader(open(paths.PDF_TEMPLATE_PATH, "rb"))
    out = PdfFileWriter()
    page = template.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    out.addPage(page)
    out_stream = io.BytesIO()
    out.write(out_stream)
    out_stream.seek(0)
    return out_stream


def write_many_pdfs(data):

    out = PdfFileWriter()

    for row in data:
        packet = io.BytesIO()
        packet = draw(row, packet)
        packet.seek(0)

        new_pdf = PdfFileReader(packet)
        template = PdfFileReader(open(paths.PDF_TEMPLATE_PATH, "rb"))
        template_page = template.getPage(0)

        template_page.mergePage(new_pdf.getPage(0))
        out.addPage(template_page)

        del packet
        del template_page
        del new_pdf

    out_stream = io.BytesIO()
    out.write(out_stream)
    out_stream.seek(0)
    return out_stream


def writepdf(data):
    packet = io.BytesIO()
    packet = draw(data, packet)
    packet.seek(0)
    return compile_packet(packet)
