# -*- coding: utf-8 -*-

import os
from pyndf.constants import CONST
from pyndf.db.client import Client
from pyndf.process.progress import Progress
from pyndf.process.reader.factory import Reader
from pyndf.gui.items.factory import Items
from pyndf.process.writer.factory import Writer
from pyndf.qtlib import QtCore
from pyndf.process.distance import DistanceMatrixAPI
from pyndf.logbook import Logger, log_time
from pyndf.db.session import db
from pyndf.utils import Utils


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

    def __init__(self, excel_file, csv_file, output_directory, color, use_db, use_cache, **kwargs):
        super().__init__(**kwargs)
        self.excel_file = excel_file
        self.csv_file = csv_file
        self.output_directory = output_directory
        self.color = color
        self.use_db = use_db
        self.use_cache = use_cache
        self.signals = WorkerSignals()
        self.progress = Progress(self.signals.progressed.emit)

    @log_time
    def read_excel(self):
        self.progress.add_duration(5)
        records, status = Reader(
            self.excel_file,
            progress=self.progress,
            log_level=self.log_level,
        )
        return records, status

    @log_time
    def read_csv(self, records):
        self.progress.add_duration(5)
        records_csv, status = Reader(
            self.csv_file,
            progress=self.progress,
            log_level=self.log_level,
        )
        for matricule, record in records.items():
            if matricule and int(matricule) in records_csv:
                record["montant_total"] = records_csv[int(matricule)]
        return records, status

    @log_time
    def run_api(self, records):
        self.progress.add_duration(45, len(records))

        api = DistanceMatrixAPI(log_level=self.log_level)
        total_status = set()

        for record in records.values():
            for mission in record["missions"]:
                distance = None
                client = mission["client"], mission["adresse_client"]
                employee = record["matricule"], record["adresse_intervenant"]
                (result, status), time_spend = api.run(client, employee, use_db=self.use_db, use_cache=self.use_cache)
                mission["status"] = status

                total_status.add(str(status))

                if result is not None:
                    distance, _ = result

                    mission["nbrkm_mois"] = mission["quantite_payee"] * 2 * distance
                    mission["forfait"] = mission["total"] / mission["nbrkm_mois"]

                self.signals.analysed.emit(
                    Items(
                        CONST.TYPE.API,
                        record["matricule"],
                        mission["adresse_client"],
                        record["adresse_intervenant"],
                        distance,
                        status,
                        time_spend,
                    )
                )

            # Check agence d'origine/address are in missions:
            mission_record = {}
            agence_o = record["agence_o"]
            with db.session_scope() as session:
                name, address = Utils.pretty_split(CONST.FILE.YAML[CONST.TYPE.AGENCE][agence_o])
                client = session.query(Client).filter(Client.name == name).first()
                if client:
                    mission_record["client"] = client.name
                    mission_record["adresse_client"] = client.address.replace(",", " ")
                    mission_record["status"] = CONST.STATUS.DB

                    if mission_record["client"] not in [mission["client"] for mission in record["missions"]]:
                        record["missions"].append(mission_record)

                    self.log.info(f"find client in DB -> {client} ")
                else:
                    self.log.warning(f"Doesn't find client in DB -> {name}")

            self.progress.send(msg=self.tr("Get distance from Google API/DB/cache"))

        return records, Utils.getattr(CONST.STATUS, total_status)

    @log_time
    def create_pdf(self, records):
        self.progress.add_duration(40, len(records))

        # Get writer
        date = Utils.get_date_from_file(self.excel_file)
        writer = Writer(
            CONST.TYPE.PDF, date, directory=self.output_directory, color=self.color, log_level=self.log_level
        )

        total_status = set()

        for record in records.values():
            (filename, status), time_spend = writer.write(record, filename=record)

            total_status.add(str(status))

            self.progress.send(msg=self.tr("Generate PDF files"))
            self.signals.analysed.emit(
                Items(
                    CONST.TYPE.PDF,
                    record["matricule"],
                    filename,
                    len(record["missions"]),
                    status,
                    time_spend,
                )
            )

        return Utils.getattr(CONST.STATUS, total_status)

    @QtCore.pyqtSlot()
    def run(self):
        """Run method"""
        self.log.info("Start process")
        try:
            sender = self.signals.analysed.emit
            # Read Excel file
            (records, status), time_spend = self.read_excel()
            sender(Items(CONST.TYPE.ALL, self.tr("Load EXCEL file"), status, time_spend))

            # Read CSV file
            (records, status), time_spend = self.read_csv(records)
            sender(Items(CONST.TYPE.ALL, self.tr("Load CSV file"), status, time_spend))

            # Calcul distance between adresse_client and adresse_intervenant with google API
            (records, status), time_spend = self.run_api(records)
            sender(Items(CONST.TYPE.ALL, self.tr("Get distance from Google API/DB/Cache"), status, time_spend))

            # Create PDF with data records and distance from the API
            (status), time_spend = self.create_pdf(records)
            sender(Items(CONST.TYPE.ALL, self.tr("Generate PDF files"), status, time_spend))

        except Exception as error:
            self.log.exception(error)
            self.signals.error.emit(error)
        else:
            self.signals.finished.emit()
        self.log.info("End process")
