# -*- coding: utf-8 -*-

import os
from pyndf.constants import CONST
from pyndf.db.client import Client
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

    def __init__(self, excel_file, csv_file, output_directory, color, **kwargs):
        super().__init__(**kwargs)
        self.excel_file = excel_file
        self.csv_file = csv_file
        self.output_directory = output_directory
        self.color = color
        self.signals = WorkerSignals()

    @log_time
    def excel_read(self):
        records = Reader(
            self.excel_file,
            progress_callback=self.signals.progressed.emit,
            p=10,
            log_level=self.log_level,
        )

        return records, CONST.STATUS.OK.NAME

    @log_time
    def read_csv(self, records):
        records_csv = Reader(
            self.csv_file,
            progress_callback=self.signals.progressed.emit,
            p=10,
            log_level=self.log_level,
        )
        for matricule, record in records.items():
            if int(matricule) in records_csv:
                record["montant_total"] = records_csv[int(matricule)]
        return records, CONST.STATUS.OK.NAME

    @log_time
    def run_api(self, records):
        api = DistanceMatrixAPI(log_level=self.log_level)
        n = len(records)
        total_status = set()
        for index, record in enumerate(records.values()):
            for mission in record["missions"]:
                distance = None
                client = mission["client"], mission["adresse_client"]
                employee = record["matricule"], record["adresse_intervenant"]
                (status, result), time_spend = api.run(client, employee)
                mission["status"] = status

                total_status.add(status)

                if result is not None:
                    distance, _ = result

                    mission["nbrkm_mois"] = mission["quantite_payee"] * 2 * distance
                    mission["forfait"] = mission["total"] / mission["nbrkm_mois"]

                self.signals.analysed.emit(
                    Items(
                        CONST.TYPE.API,
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
                client = session.query(Client).filter(Client.name.like(Utils.insert(agence_o, -1, "%"))).first()
                if client:
                    mission_record["client"] = client.name
                    mission_record["adresse_client"] = client.address.replace(",", " ")
                    mission_record["status"] = CONST.STATUS.DB.NAME

                    if mission_record["client"] not in [mission["client"] for mission in record["missions"]]:
                        record["missions"].append(mission_record)

            self.signals.progressed.emit(
                20 + (index / n) * 40,
                self.tr("Get distance from Google API/DB/cache: {} / {}").format(index, n),
            )
        total_status = "/".join(list(total_status))
        return records, total_status

    @log_time
    def create_pdf(self, records):
        date = os.path.basename(self.excel_file).split(".")[0].split("_")[1]
        writer = Writer(CONST.TYPE.PDF, date, dir=self.output_directory, color=self.color, log_level=self.log_level)
        n = len(records)
        total_status = set()
        for index, record in enumerate(records.values()):
            (filename, total, status), time_spend = writer.write(record)

            total_status.add(status)

            self.signals.progressed.emit(60 + (index / n) * 40, self.tr("Create PDFs: {} / {}").format(index, n))
            self.signals.analysed.emit(
                Items(
                    CONST.TYPE.PDF,
                    filename,
                    record.get("montant_total", 0),
                    total,
                    len(record["missions"]),
                    status,
                    time_spend,
                )
            )
        total_status = "/".join(list(total_status))
        return total_status

    @QtCore.pyqtSlot()
    def run(self):
        """Run method"""
        self.log.info("Start process")
        try:
            sender = self.signals.analysed.emit
            # Read Excel file
            (records, status), time_spend = self.excel_read()
            sender(Items(CONST.TYPE.ALL, self.tr("Read EXCEL file"), status, time_spend))

            # Read CSV file
            (records, status), time_spend = self.read_csv(records)
            sender(Items(CONST.TYPE.ALL, self.tr("Read CSV file"), status, time_spend))

            # Calcul distance between adresse_client and adresse_intervenant with google API
            (records, status), time_spend = self.run_api(records)
            sender(Items(CONST.TYPE.ALL, self.tr("Get distance from Google API/DB/Cache"), status, time_spend))

            # Create PDF with data records and distance from the API
            (status), time_spend = self.create_pdf(records)
            sender(Items(CONST.TYPE.ALL, self.tr("Write PDFs"), status, time_spend))

        except Exception as error:
            self.log.exception(error)
            self.signals.error.emit(error)
        else:
            self.signals.progressed.emit(100, self.tr("Done!"))
            self.signals.finished.emit()
        self.log.info("End process")
