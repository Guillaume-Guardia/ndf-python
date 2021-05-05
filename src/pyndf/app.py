# -*- coding: utf-8 -*-

from PyQt6 import QtWidgets, QtCore
from pyndf.logbook import Logger
from pyndf.process.thread import Thread


class Window(Logger, QtWidgets.QWidget):
    """Main window of the app

    Args:
        QtWidgets (Qobject): Qt object
        Logger (object): For logging
    """

    def __init__(self):
        super().__init__()
        self.threadpool = QtCore.QThreadPool()

        # En entrée, feuille excel
        self.sourcefile_x = QtWidgets.QLineEdit()
        self.sourcefile_x.setText(r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\ndf-python\data\test.xlsx")
        self.sourcefile_x.setDisabled(True)  # must use the file finder to select a valid file.

        self.file_select_x = QtWidgets.QPushButton("Select Excel...")
        self.file_select_x.pressed.connect(self.choose_exl_file)

        # En sortie, répertoire de sortie
        self.output = QtWidgets.QLineEdit()
        self.output.setText(r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\output")
        self.output.setDisabled(True)  # must use the file finder to select a valid file.

        self.file_select_output = QtWidgets.QPushButton("Select output directory...")
        self.file_select_output.pressed.connect(self.choose_output_file)

        self.generate_btn = QtWidgets.QPushButton("Generate PDF")
        self.generate_btn.pressed.connect(self.generate)

        layout = QtWidgets.QFormLayout()
        layout.addRow(self.sourcefile_x, self.file_select_x)
        layout.addRow(self.output, self.file_select_output)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)

    def choose_exl_file(self):
        """Method which call the native file dialog to choose excel file."""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a file", filter="Excel files (*.xl*)")
        if filename:
            self.sourcefile_x.setText(filename)

    def choose_output_file(self):
        """Method which call the native file dialog to choose the output directory."""
        output = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a folder")
        if output:
            self.output.setText(output)

    def generate(self):
        """Method triggered with the button to start the generation of pdf."""
        if not self.sourcefile_x.text() or not self.output.text():
            return None  # If the field is empty, ignore.

        self.generate_btn.setDisabled(True)

        process = Thread(self.sourcefile_x.text(), self.output.text())
        process.signals.finished.connect(self.generated)
        self.threadpool.start(process)
        return True

    def generated(self):
        """Success methdod"""
        self.generate_btn.setDisabled(False)
        QtWidgets.QMessageBox.information(self, "Finished", "PDFs have been generated")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Window()
    w.show()
    app.exec()
