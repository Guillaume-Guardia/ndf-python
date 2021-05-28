# -*- coding: utf-8 -*-

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
from pyndf.constants import CONST
from pyndf.utils import Utils

stylesheet = getSampleStyleSheet()
stylesheet.add(ParagraphStyle(name="Justify", parent=stylesheet["Normal"], alignment=TA_JUSTIFY))
stylesheet.add(ParagraphStyle(name="Center", parent=stylesheet["Normal"], alignment=TA_CENTER))


class PdfWriter(AbstractWriter, BaseDocTemplate):
    """NDF template adapted for the NDF apside based on BaseDocTemplate.

    Args:
        Logger (object): for logging on console
        BaseDocTemplate (object): object from reportlab.
    """

    ext = CONST.EXT.PDF

    def __init__(self, date, color, **kwargs):
        kwargs["pagesize"] = landscape(A4)

        super().__init__(filename="", **kwargs)
        self.color = color or CONST.WRITER.PDF.COLOR

        self.date = date
        if date is not None:
            self.date += relativedelta(months=+1)

        self.log.info("Generate PDF files")

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
            if self.date is not None:
                canvas.drawRightString(right, top, f"{self.date.strftime('%B %Y')}")
            # Set Image
            canvas.drawImage(
                CONST.FILE.LOGO, left, top + cm, width=2.5 * cm, height=-2.5 * cm, preserveAspectRatio=True
            )

        if add_footer:
            # footer
            canvas.drawString(left, bottom, "Apside Groupe")
            canvas.drawCentredString(x_center, bottom - cm, f"- {doc.page} -")
            canvas.drawRightString(right, bottom, f"version: {CONST.VERSION}")

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

    def create_table_collaborator(self, record):
        """Create the collaborator table from record.

        Args:
            record (dict): dict info.

        Returns:
            Table: returned the table with style.
        """
        result = []
        for col in CONST.WRITER.PDF.COL_PERSO:
            result.append([CONST.FILE.YAML[CONST.TYPE.PDF][col], record.get(col, CONST.WRITER.PDF.UNKNOWN)])

        table = Table(result, spaceBefore=cm, spaceAfter=cm)
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
        nbrkm_mois = 0
        quantite_payee = 0
        total = 0
        prix_unitaire = 0
        total_status = set()

        # Add header
        for name in CONST.WRITER.PDF.COL_MISSION:
            data[0].append(Paragraph(CONST.FILE.YAML[CONST.TYPE.PDF][name], stylesheet["Center"]))

        for mission in record.get("missions", {}):
            total_status.add(str(mission["status"]))

            nbrkm_mois += mission.get("nbrkm_mois", 0)
            quantite_payee += mission.get("quantite_payee", 0)
            total += mission.get("total", 0)
            prix_unitaire = max(mission.get("prix_unitaire", 0), prix_unitaire)

        nbrkm_mois = round(nbrkm_mois, 2)
        quantite_payee = round(quantite_payee, 2)
        prix_unitaire = round(prix_unitaire, 2)
        total = round(total, 2)

        if quantite_payee > 0 and nbrkm_mois / quantite_payee > 100:
            nbrkm_mois = f"> {100 * quantite_payee}"

        for mission in record.get("missions", {}):
            client = mission.get("client", CONST.WRITER.PDF.UNKNOWN)
            address = mission.get("adresse_client", CONST.WRITER.PDF.UNKNOWN)

            if (client, address) not in memory_mission:
                data.append(
                    [
                        Paragraph(client, stylesheet["Justify"]),
                        mission.get("periode_production", CONST.WRITER.PDF.UNKNOWN),
                        Paragraph(address, stylesheet["Justify"]),
                        nbrkm_mois,
                        quantite_payee,
                        prix_unitaire,
                        total,  # TODO
                    ]
                )
                memory_mission.append((client, address))

        # Create table with data
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
                ("BACKGROUND", (0, 0), (-1, 0), self.color),
                ("GRID", (0, 0), (-1, -1), 0.25, black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )

        # Merge
        total_status = Utils.getattr(CONST.STATUS, total_status)
        if total_status:
            for i in (1, 3, 4, 5, 6):
                style.add("SPAN", (i, 1), (i, -1))

        table.setStyle(style)
        return table, total_status

    def create_path(self, data=None):
        filename = self.create_filename(data)
        return super().create_path(filename)

    def create_filename(self, data):
        matricule = data.get("matricule", CONST.WRITER.PDF.UNKNOWN)
        self.log.debug(f"Create pdf for matricule {matricule} with {len(data.get('missions', []))} missions.")
        if self.date is not None:
            date = self.date.strftime("%Y%m")
        else:
            date = "NODATE"
        return f"{data.get('agence', CONST.WRITER.PDF.UNKNOWN)}_{matricule}_{date}"

    def _write(self, data, path):
        """Create method, add each element of pdf.

        Args:
            data (dict): record data with personnal info of collaborator and his missions info.
        """

        paragraphs = []
        # add some flowables
        paragraphs.append(Paragraph("NOTE DE FRAIS", stylesheet["title"]))
        paragraphs.append(Paragraph(f"AGENCE: {data.get('agence', CONST.WRITER.PDF.UNKNOWN)}", stylesheet["title"]))
        paragraphs.append(
            Paragraph(f"AGENCE D'ORIGINE: {data.get('agence_o', CONST.WRITER.PDF.UNKNOWN)}", stylesheet["title"])
        )
        paragraphs.append(self.create_table_collaborator(data))
        table, status = self.create_table_missions(data)
        paragraphs.append(table)
        paragraphs.append(Paragraph("<b>NB: Carte grise à disposition de la direction.</b>", stylesheet["Normal"]))

        self.build(paragraphs, path)

        return status
