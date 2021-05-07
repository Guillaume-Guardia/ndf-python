# -*- coding: utf-8 -*-

from PyQt6 import QtCore
from pyndf.reader.excel import ExcelReader
from pyndf.writer.pdf import PdfWriter
from pyndf.process.distance import DistanceMatrixAPI
from pyndf.logbook import Logger, log_time


class WorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.
    """

    finished = QtCore.pyqtSignal()
    progressed = QtCore.pyqtSignal(float)


class Thread(Logger, QtCore.QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, data_file, output_directory):
        super().__init__()
        self.data_file = data_file
        self.output_directory = output_directory
        self.signals = WorkerSignals()

    @log_time
    @QtCore.pyqtSlot()
    def run(self):
        """Run method"""
        try:
            # Read Excel file
            reader = ExcelReader(self.data_file)
            records = reader.read(progress_callback=self.signals.progressed.emit, p=20)

            # Calcul distance between adresse_client and adresse_intervenant with google API
            api = DistanceMatrixAPI()
            n = len(records)
            for index, record in enumerate(records.values()):
                for mission in record["missions"]:
                    status, result = api.run(mission["adresse_client"], record["adresse_intervenant"])
                    mission["status"] = status
                    if result is not None:
                        distance, _ = result

                        mission["nbrkm_mois"] = mission["quantite_payee"] * 2 * distance
                        mission["forfait"] = mission["total"] / mission["nbrkm_mois"]
                self.signals.progressed.emit(20 + (index / n) * 50)

            # Create PDF with data records and distance from the API
            writer = PdfWriter(directory=self.output_directory)
            n = len(records)
            for index, record in enumerate(records.values()):
                writer.write(record)
                self.signals.progressed.emit(70 + (index / n) * 30)

        except Exception as error:
            self.log.exception(error)
        else:
            self.signals.progressed.emit(100)
            self.signals.finished.emit()
