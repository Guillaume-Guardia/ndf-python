# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.gui.items.factory import Items
from pyndf.process.writer.factory import Writer
from pyndf.qtlib import QtCore
from pyndf.utils import Utils


class PdfGenerator(QtCore.QThread):
    def __init__(self, parent, record, date, total_status):
        super().__init__()
        self.parent = parent
        self.record = record
        self.date = date
        self.total_status = total_status

    def run(self):
        writer = Writer(
            CONST.TYPE.PDF,
            self.date,
            directory=self.parent.output_directory,
            color=self.parent.color,
            log_level=self.parent.log_level,
            overwrite=self.parent.overwrite,
        )

        self.record.prepare_for_pdf()
        (filename, status), time_spend = writer.write(self.record, filename=self.record)

        self.total_status.add(str(status))

        self.parent.progress.send(msg=self.tr("Generate PDF files"))
        self.parent.signals.analysed.emit(
            Items(
                CONST.TYPE.PDF,
                Utils.type(self.record.matricule),
                filename,
                self.record.nom_intervenant,
                len(self.record.missions),
                len(self.record.indemnites),
                status,
                time_spend,
            )
        )
