# -*- coding: utf-8 -*-

from PyQt6 import QtCore


class WorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.
    """

    error = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()


class Generator(QtCore.QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.

    :param data: The data to add to the PDF for generating.
    """

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        """Run method"""
        try:
            pass

        except Exception as error:
            self.signals.error.emit(str(error))
        else:
            self.signals.finished.emit()
