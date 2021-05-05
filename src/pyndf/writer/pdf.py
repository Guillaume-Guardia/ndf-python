# -*- coding: utf-8 -*-

import os
from datetime import datetime

from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import black
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus.paragraph import Paragraph

from pyndf.logbook import Logger, log_time
from pyndf.constants import LOGO, CONFIG

UNKNOWN = "Inconnu"
stylesheet = getSampleStyleSheet()
stylesheet.add(ParagraphStyle(name="Justify", parent=stylesheet["Normal"], alignment=TA_JUSTIFY))
stylesheet.add(ParagraphStyle(name="Center", parent=stylesheet["Normal"], alignment=TA_CENTER))


class PdfWriter(Logger, BaseDocTemplate):
    """NDF template adapted for the NDF apside based on BaseDocTemplate.

    Args:
        Logger (object): for logging on console
        BaseDocTemplate (object): object from reportlab.
    """

    def __init__(self, filename="", directory=".", **kwargs):
        kwargs["pagesize"] = landscape(A4)

        # Define for pylint
        self.pagesize = []
        self.bottomMargin = None
        self.leftMargin = None
        super().__init__(filename, **kwargs)
        self.directory = directory
        self.date = datetime.today().strftime("%d-%m-%Y")
        self.version = "0.0.1"
        self.fund = "fund"

    def all_page_setup(self, canvas, doc, add_header=True, add_footer=True, add_watermark=True):
        """Set up page.

        Args:
            canvas (Canvas): Canvas from reportlab
            doc (Document): Writing document
            add_header (bool, optional): Add the header to page. Defaults to True.
            add_footer (bool, optional): Add the footer to page. Defaults to True.
            add_watermark (bool, optional): Add the watermark to page. Defaults to True.
        """
        canvas.saveState()

        if add_header:
            # header
            canvas.drawRightString(10.5 * inch, 8 * inch, f"{self.date} {self.version}")
            # Set Image
            canvas.drawImage(LOGO, 0.5 * inch, 8 * inch, width=2.5 * cm, height=-2.5 * cm, preserveAspectRatio=True)

        if add_footer:
            # footer
            canvas.drawString(0.5 * inch, 0.5 * inch, "Apside Groupe")
            canvas.drawCentredString(self.pagesize[0] / 2, 0.5 * inch, f"- {doc.page} -")

        if add_watermark:
            # Move the origin to middle, and after rotate the image
            canvas.translate(self.pagesize[0] / 2, self.pagesize[1] / 2)
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
        data = [[]]
        for name in (
            "Nom du client",
            "Période",
            "Adresse de réalisation",
            "Nombre de Kilomètres/mois",
            "Taux",
            "Plafond Apside",
            "Montant Total",
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

        for mission in record.get("missions", {}):
            if not error:
                data.append(
                    [
                        Paragraph(mission.get("client", UNKNOWN), stylesheet["Justify"]),
                        mission.get("periode_production", UNKNOWN),
                        Paragraph(mission.get("adresse_client", UNKNOWN), stylesheet["Justify"]),
                        round(nbrkm_mois, 2),
                        round(quantite_payee, 2),
                        round(prix_unitaire, 2),
                        round(total, 2),
                    ]
                )
            else:
                data.append(
                    [
                        Paragraph(mission.get("client", UNKNOWN), stylesheet["Justify"]),
                        Paragraph(mission.get("adresse_client", UNKNOWN), stylesheet["Justify"]),
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.mediumaquamarine),
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
        return table

    @log_time
    def write(self, data):
        """Create method, add each element of pdf.

        Args:
            data (dict): record data with personnal info of collaborator and his missions info.
        """
        matricule = data.get("matricule", UNKNOWN)
        self.log.info(f"Start Create pdf for matricule {matricule} with {len(data['missions'])} missions.")
        filename = f"{data.get('agence', UNKNOWN)}_{matricule}_{self.date}"

        paragraphs = []
        # add some flowables
        paragraphs.append(Paragraph("NOTE DE FRAIS", stylesheet["title"]))
        paragraphs.append(Paragraph(f"AGENCE: {data.get('agence', UNKNOWN)}", stylesheet["title"]))
        paragraphs.append(Paragraph(f"AGENCE D'ORIGINE: {data.get('agence_o', UNKNOWN)}", stylesheet["title"]))

        paragraphs.append(self.create_table_collaborator(data))
        paragraphs.append(self.create_table_missions(data))

        paragraphs.append(Paragraph("<b>NB: Carte grise à disposition de la direction.</b>", stylesheet["Normal"]))
        path = self.check_path(filename)
        self.build(paragraphs, path)

    def check_path(self, filename, ext="pdf", force=True):
        """Check path method.

        Args:
            filename (string): just the basename of the wanted file
            ext (str, optional): extension of the file added to filename. Defaults to "pdf".
            force (bool, optional): Force the creation of file. Defaults to True.

        Raises:
            FileExistsError: If force is deactivate, raise the error if the filename already exists.

        Returns:
            string: Path of the file
        """
        filename = ".".join([str(filename), ext])
        path = os.path.join(self.directory, filename)

        # Check if the file exists
        if os.path.exists(path) and not force:
            raise FileExistsError
        return path
