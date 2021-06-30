# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.process.data.progress import Progress
from pyndf.process.reader.factory import Reader
from pyndf.gui.items.factory import Items
from pyndf.process.data.records_manager import RecordsManager
from pyndf.process.writer.factory import Writer
from pyndf.qtlib import QtCore
from pyndf.process.distance import DistanceMatrixAPI
from pyndf.logbook import Logger, log_time
from pyndf.utils import Utils
from pyndf.process.threads.pdf import PdfGenerator


class CancelException(Exception):
    pass


class NdfProcess(Logger, QtCore.QThread, QtCore.QObject):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    class WorkerSignals(QtCore.QObject):
        """
        Defines the signals available from a running worker thread.
        """

        error = QtCore.pyqtSignal(object)
        finished = QtCore.pyqtSignal(object)
        progressed = QtCore.pyqtSignal(float, str)
        analysed = QtCore.pyqtSignal(object)
        cancelled = QtCore.pyqtSignal()

    class Flags:
        cancel = False

    def __init__(self, parent, excel_file, csv_file, output_directory, matricule):
        super().__init__(log_level=parent.log_level)
        self.parent = parent
        self.excel_file = excel_file
        self.csv_file = csv_file
        self.output_directory = output_directory
        self.color = parent.color

        # Distance parameters
        self.use_db = parent.use_db
        self.use_cache = parent.use_cache
        self.use_api = parent.use_api

        # Pdf parameters
        self.overwrite = parent.overwrite
        self.use_multithreading = parent.use_multithreading

        self.signals = self.WorkerSignals()
        self.progress = Progress(self.signals.progressed.emit)
        self.records_manager = RecordsManager(log_level=self.log_level, matricule=matricule)
        self.flags = self.Flags()

    @log_time
    def read_excel(self):
        # Check cancel
        if self.flags.cancel:
            raise CancelException

        self.progress.add_duration(5)
        _, status = Reader(
            self.excel_file,
            progress=self.progress,
            log_level=self.log_level,
            manager=self.records_manager,
        )
        return status

    @log_time
    def read_csv(self):
        # Check cancel
        if self.flags.cancel:
            raise CancelException

        self.progress.add_duration(5)
        _, status = Reader(
            self.csv_file,
            progress=self.progress,
            log_level=self.log_level,
            manager=self.records_manager,
        )
        return status

    @log_time
    def run_api(self):
        self.progress.add_duration(45, len(self.records_manager))

        api = DistanceMatrixAPI(log_level=self.log_level)
        total_status = set()

        for record in self.records_manager:
            for mission in record.missions:
                # Check cancel
                if self.flags.cancel:
                    raise CancelException

                client = mission.client, mission.adresse_client
                employee = record.matricule, record.adresse_intervenant

                (result, status), time_spend = api.run(
                    client,
                    employee,
                    use_db=self.use_db,
                    use_cache=self.use_cache,
                    use_api=self.use_api,
                    analyse=self.signals.analysed.emit,
                )
                mission.status = status
                total_status.add(str(status))

                mission.set_api_result(result)

                self.signals.analysed.emit(
                    Items(
                        CONST.TYPE.API,
                        Utils.type(record.matricule),
                        mission.adresse_client,
                        record.adresse_intervenant,
                        mission.distance,
                        status,
                        time_spend,
                    )
                )

            self.progress.send(msg=self.tr("Get distance from Google API/DB/cache"))

        return Utils.getattr(CONST.STATUS, total_status)

    @log_time
    def create_pdf(self):
        self.progress.add_duration(40, len(self.records_manager))
        total_status = set()

        # Get writer
        date = Utils.get_date_from_file(self.excel_file)

        if not self.use_multithreading:
            writer = Writer(
                CONST.TYPE.PDF,
                date,
                directory=self.output_directory,
                color=self.color,
                log_level=self.log_level,
                overwrite=self.overwrite,
            )

            for record in self.records_manager:
                # Check cancel
                if self.flags.cancel:
                    raise CancelException

                record.prepare_for_pdf()
                (filename, status), time_spend = writer.write(record, filename=record)

                total_status.add(str(status))

                self.progress.send(msg=self.tr("Generate PDF files"))
                self.signals.analysed.emit(
                    Items(
                        CONST.TYPE.PDF,
                        Utils.type(record.matricule),
                        filename,
                        record.nom_intervenant,
                        len(record.missions),
                        len(record.indemnites),
                        status,
                        time_spend,
                    )
                )
        else:
            for record in self.records_manager:
                # Check cancel
                if self.flags.cancel:
                    raise CancelException

                # Create a new thread and start it
                self.parent.processes.append(PdfGenerator(self, record, date, total_status))
                self.parent.processes[-1].start()

            for process in self.parent.processes:
                process.wait()

        return Utils.getattr(CONST.STATUS, total_status)

    @QtCore.pyqtSlot()
    def run(self):
        """Run method"""
        try:
            self.log.info("Start process")
            sender = self.signals.analysed.emit
            # Read Excel file
            status, time_spend = self.read_excel()
            sender(Items(CONST.TYPE.ALL, self.tr("Load EXCEL file"), status, time_spend))

            # Read CSV file
            status, time_spend = self.read_csv()
            sender(Items(CONST.TYPE.ALL, self.tr("Load CSV file"), status, time_spend))

            # Calcul distance between adresse_client and adresse_intervenant with google API
            status, time_spend = self.run_api()
            sender(Items(CONST.TYPE.ALL, self.tr("Get distance from Google API/DB/Cache"), status, time_spend))

            # Create PDF with data records and distance from the API
            status, time_spend = self.create_pdf()
            sender(Items(CONST.TYPE.ALL, self.tr("Generate PDF files"), status, time_spend))

        except CancelException:
            self.signals.cancelled.emit()

        except Exception as error:
            self.log.exception(error)
            self.signals.error.emit(error)
        else:
            self.signals.finished.emit(self.records_manager.matricule)
        finally:
            self.log.info("End process")
