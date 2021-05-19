# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import black
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus.paragraph import Paragraph

from pyndf.process.writer.abstract import AbstractWriter
from pyndf.logbook import log_time
from pyndf.constants import LOGO, CONFIG, VERSION

UNKNOWN = "Inconnu"
stylesheet = getSampleStyleSheet()
stylesheet.add(ParagraphStyle(name="Justify", parent=stylesheet["Normal"], alignment=TA_JUSTIFY))
stylesheet.add(ParagraphStyle(name="Center", parent=stylesheet["Normal"], alignment=TA_CENTER))


class PdfWriter(AbstractWriter, BaseDocTemplate):
    """NDF template adapted for the NDF apside based on BaseDocTemplate.

    Args:
        Logger (object): for logging on console
        BaseDocTemplate (object): object from reportlab.
    """

    def __init__(self, date, **kwargs):
        kwargs["pagesize"] = landscape(A4)

        super().__init__(**kwargs)

        self.date = datetime(year=int(date[:4]), month=int(date[4:6]), day=1) + relativedelta(months=+1)
        self.version = VERSION

        self.log.info("Create PDFs")

    def all_page_setup(self, canvas, doc, add_header=True, add_footer=True, add_watermark=False):
        """Set up page.

        Args:
            canvas (Canvas): Canvas from reportlab
            doc (Document): Writing document
            add_header (bool, optional): Add the header to page. Defaults to True.
            add_footer (bool, optional): Add the footer to page. Defaults to True.
            add_watermark (bool, optional): Add the watermark to page. Defaults to True.
        """
        canvas.saveState()

        marge = 2.5 * cm

        # X [0 -> 29.7]
        right = self.pagesize[0] - marge
        x_center = self.pagesize[0] / 2
        left = marge

        # Y [0 -> 21]
        top = self.pagesize[1] - marge
        y_center = self.pagesize[1] / 2
        bottom = marge

        if add_header:
            # header
            canvas.drawRightString(right, top, f"{self.date.strftime('%B %Y')}")
            # Set Image
            canvas.drawImage(LOGO, left, top + cm, width=2.5 * cm, height=-2.5 * cm, preserveAspectRatio=True)

        if add_footer:
            # footer
            canvas.drawString(left, bottom, "Apside Groupe")
            canvas.drawCentredString(x_center, bottom - cm, f"- {doc.page} -")
            canvas.drawRightString(right, bottom, f"{self.version}")

        if add_watermark:
            # Move the origin to middle, and after rotate the image
            canvas.translate(x_center, y_center)
            canvas.rotate(-30)
            canvas.setFont("Helvetica", 150)
            canvas.setStrokeGray(0.90)
            canvas.setFillGray(0.90)
            canvas.drawCentredString(0, 0, "confidentiel")

        canvas.restoreState()

    def build(self, *args, **kwargs):
        self._calc()  # in case we changed margins sizes etc
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(frames=frame, onPage=self.all_page_setup, pagesize=self.pagesize))
        super().build(*args, **kwargs)

    def create_table_collaborator(self, data):
        """Create the collaborator table from data.

        Args:
            data (dict): dict info.

        Returns:
            Table: returned the table with style.
        """
        data = [
            ["Nom Prénom:", data.get("nom", UNKNOWN)],
            ["Matricule:", data.get("matricule", UNKNOWN)],
            ["Adresse:", data.get("adresse_intervenant", UNKNOWN)],
        ]
        table = Table(data, spaceBefore=cm, spaceAfter=cm)
        style = TableStyle([("GRID", (0, 0), (-1, -1), 0.25, black)])
        table.setStyle(style)
        return table

    def create_table_missions(self, record):
        """Create missions table from record.

        Args:
            record (dict): data info

        Returns:
            Table: returned table with style.
        """
        memory_mission = []
        data = [[]]
        for name in (
            "Nom du client",
            "Période",
            "Adresse de réalisation",
            "Nb de Km par mois",
            "Taux",
            "Plafond APSIDE",
            "Montant total",
        ):
            data[0].append(Paragraph(name, stylesheet["Center"]))
        nbrkm_mois = 0
        quantite_payee = 0
        total = 0
        prix_unitaire = 0

        error = False

        for mission in record.get("missions", {}):
            if mission["status"] not in CONFIG["good_status"]:
                error = True
                break

            nbrkm_mois += mission.get("nbrkm_mois", 0)
            quantite_payee += mission.get("quantite_payee", 0)
            total += mission.get("total", 0)
            prix_unitaire = max(mission.get("prix_unitaire", 0), prix_unitaire)

        nbrkm_mois = round(nbrkm_mois, 2)
        quantite_payee = round(quantite_payee, 2)
        prix_unitaire = round(prix_unitaire, 2)
        total = round(total, 2)

        if nbrkm_mois / quantite_payee > 100:
            nbrkm_mois = f"> {100 * quantite_payee}"

        for mission in record.get("missions", {}):
            client = mission.get("client", UNKNOWN)
            address = mission.get("adresse_client", UNKNOWN)
            if not error:
                if (client, address) not in memory_mission:
                    data.append(
                        [
                            Paragraph(client, stylesheet["Justify"]),
                            mission.get("periode_production", UNKNOWN),
                            Paragraph(address, stylesheet["Justify"]),
                            nbrkm_mois,
                            quantite_payee,
                            prix_unitaire,
                            total,
                        ]
                    )
                    memory_mission.append((client, address))
            else:
                data.append(
                    [
                        Paragraph(client, stylesheet["Justify"]),
                        Paragraph(address, stylesheet["Justify"]),
                        mission.get("status"),
                    ]
                )

        table = Table(
            data,
            spaceBefore=cm,
            spaceAfter=cm,
            colWidths=self.width / len(data[0]),
            hAlign="CENTER",
            normalizedData=True,
        )
        style = TableStyle(
            [
                # First row in blue
                ("BACKGROUND", (0, 0), (-1, 0), "#99ccff"),
                ("GRID", (0, 0), (-1, -1), 0.25, black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )

        if not error:
            # Merge
            for i in (1, 3, 4, 5, 6):
                style.add("SPAN", (i, 1), (i, -1))

        table.setStyle(style)
        return table, total

    @log_time
    def write(self, data):
        """Create method, add each element of pdf.

        Args:
            data (dict): record data with personnal info of collaborator and his missions info.
        """
        matricule = data.get("matricule", UNKNOWN)
        self.log.debug(f"Create pdf for matricule {matricule} with {len(data['missions'])} missions.")
        filename = f"{data.get('agence', UNKNOWN)}_{matricule}_{self.date.strftime('%Y%m')}"
        path = self.create_path(filename)

        paragraphs = []
        # add some flowables
        paragraphs.append(Paragraph("NOTE DE FRAIS", stylesheet["title"]))
        paragraphs.append(Paragraph(f"AGENCE: {data.get('agence', UNKNOWN)}", stylesheet["title"]))
        paragraphs.append(Paragraph(f"AGENCE D'ORIGINE: {data.get('agence_o', UNKNOWN)}", stylesheet["title"]))

        paragraphs.append(self.create_table_collaborator(data))
        table, total = self.create_table_missions(data)
        paragraphs.append(table)

        paragraphs.append(Paragraph("<b>NB: Carte grise à disposition de la direction.</b>", stylesheet["Normal"]))

        try:
            self.build(paragraphs, path)
        except Exception as e:
            self.log.exception(e)
            return filename, None, "error"
        return filename, total, CONFIG["good_status"][0]
