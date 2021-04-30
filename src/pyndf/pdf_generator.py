from PyQt6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QApplication,
    QFormLayout,
    QWidget,
    QTextEdit,
    QMessageBox,
    QSpinBox,
    QFileDialog,
)
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image
import os
import textwrap
from datetime import datetime
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from reportlab.lib.units import cm
from reportlab.lib.colors import pink, black, red, blue, green


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """

    error = pyqtSignal(str)
    finished = pyqtSignal()


def function(data=None, dir_output=r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\output"):
    data = {
        "nom": "nan",
        "matricule": 261,
        "societe": "APSID",
        "agence": "BRES1",
        "agence_o": "BRES1",
        "periode_paie": "2020-12",
        "client": "BREST 1",
        "adresse_client": "90 rue Ernest Hemingway 29200 BREST",
        "adresse_intervenant": "140 BIS RUE ROBESPIERRE 29200 BREST",
        "quantite_payee": 12,
        "prix_unitaire": 5.4,
        "total": 64.8,
        "nbrkm_mois": 92.85600000000001,
        "forfait": 0.697854742827604,
    }
    filename = os.path.join(
        dir_output, f"{data['agence']}_{data['matricule']}_{datetime.today().strftime('%d_%m_%Y')}.pdf"
    )
    canvas = Canvas(filename, bottomup=0, pagesize=landscape(A4))

    canvas.setStrokeColor(blue)
    canvas.grid(list([x * cm for x in range(31)]), list([y * cm for y in range(22)]))
    canvas.setStrokeColor(black)

    # Set Image
    canvas.saveState()
    canvas.scale(1, -1)
    apside_logo = os.path.join(os.path.dirname(__file__), "data", "apside-logo.png")
    canvas.drawImage(apside_logo, cm, cm, width=3 * cm, height=-3 * cm, preserveAspectRatio=True)
    canvas.restoreState()

    # # Prepared by
    canvas.drawString(2 * cm, 2 * cm, data["nom"])

    # # Date: Todays date
    # today = datetime.today()
    # canvas.drawString(410, ystart, today.strftime("%F"))

    # # Device/Program Type
    # canvas.drawString(230, ystart - 28, row.get("program_type", ""))

    # # Product code
    # canvas.drawString(175, ystart - (2 * 28), row.get("product_code", ""))

    # # Customer
    # canvas.drawString(315, ystart - (2 * 28), row.get("customer", ""))

    # # Vendor
    # canvas.drawString(145, ystart - (3 * 28), row.get("vendor", ""))

    # ystart = 250

    # # Program Language
    # canvas.drawString(210, ystart, "Python")

    # canvas.drawString(430, ystart, row.get("n_errors", ""))

    # comments = row.get("comments", "").replace("\n", " ")
    # if comments:
    #     lines = textwrap.wrap(comments, width=65)  # 45
    #     first_line = lines[0]
    #     remainder = " ".join(lines[1:])

    #     lines = textwrap.wrap(remainder, 75)  # 55
    #     lines = lines[:4]  # max lines, not including the first.

    #     canvas.drawString(155, 223, first_line)
    #     for n, l in enumerate(lines, 1):
    #         canvas.drawString(80, 223 - (n * 28), l)

    canvas.save()


class Generator(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            filename, _ = os.path.splitext(self.data["sourcefile"] or self.data["sourcefile_x"])
            folder = os.path.dirname(self.data["sourcefile"] or self.data["sourcefile_x"])

            # template = PdfReader(self.data["pdf"], decompress=False).pages[0]
            # template_obj = pagexobj(template)

            with open(self.data["sourcefile"], "r", newline="") as f:
                reader = csv.DictReader(f)

                for n, row in enumerate(reader, 1):
                    fn = f"{filename}-{n}.pdf"
                    outfile = os.path.join(folder, fn)
                    canvas = Canvas(outfile)

                    canvas.setPageSize((29.7 * cm, 21 * cm))

                    # xobj_name = makerl(canvas, template_obj)
                    # canvas.doForm(xobj_name)

                    # ystart = 443
                    # canvas.translate(cm, 18 * cm)
                    canvas.setStrokeColor(blue)
                    canvas.grid(list([x * cm for x in range(31)]), list([y * cm for y in range(22)]))
                    canvas.setStrokeColor(black)

                    # # Prepared by
                    # canvas.drawString(170, ystart, row.get("name", ""))

                    # # Date: Todays date
                    # today = datetime.today()
                    # canvas.drawString(410, ystart, today.strftime("%F"))

                    # # Device/Program Type
                    # canvas.drawString(230, ystart - 28, row.get("program_type", ""))

                    # # Product code
                    # canvas.drawString(175, ystart - (2 * 28), row.get("product_code", ""))

                    # # Customer
                    # canvas.drawString(315, ystart - (2 * 28), row.get("customer", ""))

                    # # Vendor
                    # canvas.drawString(145, ystart - (3 * 28), row.get("vendor", ""))

                    # ystart = 250

                    # # Program Language
                    # canvas.drawString(210, ystart, "Python")

                    # canvas.drawString(430, ystart, row.get("n_errors", ""))

                    # comments = row.get("comments", "").replace("\n", " ")
                    # if comments:
                    #     lines = textwrap.wrap(comments, width=65)  # 45
                    #     first_line = lines[0]
                    #     remainder = " ".join(lines[1:])

                    #     lines = textwrap.wrap(remainder, 75)  # 55
                    #     lines = lines[:4]  # max lines, not including the first.

                    #     canvas.drawString(155, 223, first_line)
                    #     for n, l in enumerate(lines, 1):
                    #         canvas.drawString(80, 223 - (n * 28), l)

                    canvas.save()

        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.finished.emit()


if __name__ == "__main__":
    function()
