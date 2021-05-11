# -*- coding: utf-8 -*-

import os
from time import time
from PyQt6 import QtCore
from pyndf.process.reader.excel import ExcelReader
from pyndf.process.reader.csv import CSVReader
from pyndf.process.writer.pdf import PdfWriter
from pyndf.process.distance import DistanceMatrixAPI
from pyndf.logbook import Logger
from pyndf.gui.items.all_item import AllItem
from pyndf.gui.items.api_item import APIItem
from pyndf.gui.items.pdf_item import PDFItem


class WorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.
    """

    error = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal(float)
    progressed = QtCore.pyqtSignal(float, str)
    analysed_all = QtCore.pyqtSignal(object)
    analysed_api = QtCore.pyqtSignal(object)
    analysed_pdf = QtCore.pyqtSignal(object)


class Thread(Logger, QtCore.QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, excel_file, csv_file, output_directory):
        super().__init__()
        self.excel_file = excel_file
        self.csv_file = csv_file
        self.output_directory = output_directory
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        """Run method"""
        try:
            start = time()
            # Read Excel file
            reader = ExcelReader(self.excel_file)
            records, time_spend = reader.read(progress_callback=self.signals.progressed.emit, p=20)
            t1 = time()
            self.signals.analysed_all.emit(AllItem("Read excel file", "OK", t1 - start))

            # Read CSV file
            reader = CSVReader(self.csv_file)
            records_csv, time_spend = reader.read()
            for matricule, record in records.items():
                if int(matricule) in records_csv:
                    record["montant_total"] = records_csv[int(matricule)]
            t2 = time()
            self.signals.analysed_all.emit(AllItem("Read csv file", "OK", t2 - t1))

            # Calcul distance between adresse_client and adresse_intervenant with google API
            api = DistanceMatrixAPI()
            n = len(records)
            for index, record in enumerate(records.values()):
                for mission in record["missions"]:
                    distance = None
                    (status, result), time_spend = api.run(mission["adresse_client"], record["adresse_intervenant"])
                    mission["status"] = status
                    if result is not None:
                        distance, _ = result

                        mission["nbrkm_mois"] = mission["quantite_payee"] * 2 * distance
                        mission["forfait"] = mission["total"] / mission["nbrkm_mois"]

                    self.signals.analysed_api.emit(
                        APIItem(mission["adresse_client"], record["adresse_intervenant"], distance, status, time_spend)
                    )
                self.signals.progressed.emit(
                    20 + (index / n) * 50,
                    self.signals.tr(f"Get distance from Google API or DB or cache: {index} / {n}"),
                )
            t3 = time()
            self.signals.analysed_all.emit(AllItem("Get distance", "OK", t3 - t2))

            # Create PDF with data records and distance from the API
            date = os.path.basename(self.excel_file).split(".")[0].split("_")[1]
            writer = PdfWriter(date, directory=self.output_directory)
            n = len(records)
            for index, record in enumerate(records.values()):
                (filename, total, status), time_spend = writer.write(record)
                self.signals.progressed.emit(70 + (index / n) * 30, self.signals.tr(f"Create PDFs: {index} / {n}"))
                self.signals.analysed_pdf.emit(
                    PDFItem(
                        filename, record.get("montant_total", 0), total, len(record["missions"]), status, time_spend
                    )
                )
            t4 = time()
            self.signals.analysed_all.emit(AllItem("Write PDFs", "OK", t4 - t3))

        except Exception as error:
            self.log.exception(error)
            self.signals.error.emit(error)
        else:
            self.signals.progressed.emit(100, self.signals.tr("Done!"))
            self.signals.finished.emit(round(time() - start, 2))
