# -*- coding: utf-8 -*-

import os
from time import time
from pyndf.process.reader.factory import reader_factory
from pyndf.qtlib import QtCore
from pyndf.process.writer.useclass.pdf import PdfWriter
from pyndf.process.distance import DistanceMatrixAPI
from pyndf.logbook import Logger
from pyndf.gui.items.useclass.analyse.all import AllItem
from pyndf.gui.items.useclass.analyse.api import ApiItem
from pyndf.gui.items.useclass.analyse.pdf import PdfItem


class WorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.
    """

    error = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal()
    progressed = QtCore.pyqtSignal(float, str)
    analysed = QtCore.pyqtSignal(object)


class Thread(Logger, QtCore.QRunnable, QtCore.QObject):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, excel_file, csv_file, output_directory, color, **kwargs):
        super().__init__(**kwargs)
        self.excel_file = excel_file
        self.csv_file = csv_file
        self.output_directory = output_directory
        self.color = color
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        """Run method"""
        try:
            self.log.info("Start process")
            start = time()

            # Read Excel file
            records, time_spend = reader_factory(
                self.excel_file,
                progress_callback=self.signals.progressed.emit,
                p=10,
                log_level=self.log_level,
            )
            t1 = time()
            self.signals.analysed.emit(AllItem(self.tr("Read EXCEL file"), "OK", t1 - start))

            # Read CSV file
            records_csv, time_spend = reader_factory(
                self.csv_file,
                progress_callback=self.signals.progressed.emit,
                p=10,
                log_level=self.log_level,
            )
            for matricule, record in records.items():
                if int(matricule) in records_csv:
                    record["montant_total"] = records_csv[int(matricule)]
            t2 = time()
            self.signals.analysed.emit(AllItem(self.tr("Read CSV file"), "OK", t2 - t1))

            # Calcul distance between adresse_client and adresse_intervenant with google API
            api = DistanceMatrixAPI(log_level=self.log_level)
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

                    self.signals.analysed.emit(
                        ApiItem(mission["adresse_client"], record["adresse_intervenant"], distance, status, time_spend)
                    )

                # Check agence d'origine/address are in missions:
                for mission in record["missions"]:
                    pass

                self.signals.progressed.emit(
                    20 + (index / n) * 40,
                    self.tr("Get distance from Google API/DB/cache: {} / {}").format(index, n),
                )
            t3 = time()
            self.signals.analysed.emit(AllItem(self.tr("Get distance from Google API/DB/Cache"), "OK", t3 - t2))

            # Create PDF with data records and distance from the API
            date = os.path.basename(self.excel_file).split(".")[0].split("_")[1]
            writer = PdfWriter(date, dir=self.output_directory, color=self.color, log_level=self.log_level)
            n = len(records)
            for index, record in enumerate(records.values()):
                (filename, total, status), time_spend = writer.write(record)
                self.signals.progressed.emit(60 + (index / n) * 40, self.tr("Create PDFs: {} / {}").format(index, n))
                self.signals.analysed.emit(
                    PdfItem(
                        filename, record.get("montant_total", 0), total, len(record["missions"]), status, time_spend
                    )
                )
            self.signals.analysed.emit(AllItem(self.tr("Write PDFs"), "OK", time() - t3))

        except Exception as error:
            self.log.exception(error)
            self.signals.error.emit(error)
        else:
            self.log.info("End process")
            self.signals.progressed.emit(100, self.tr("Done!"))
            self.signals.finished.emit()
