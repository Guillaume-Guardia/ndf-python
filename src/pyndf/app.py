# -*- coding: utf-8 -*-

import sys
from PyQt6 import QtWidgets, QtCore
from pyndf.logbook import Logger
from pyndf.process.thread import Thread


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, data_file="", output_directory=""):
        super().__init__()
        self.threadpool = QtCore.QThreadPool()

        self.setWindowTitle("pyNDF")
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TitleBarMenuButton))
        self.setMinimumSize(1000, 200)

        self.buttons = {}
        self.texts = {}

        # En entrée, feuille excel
        self.add_button("excel", "(*.xl*)", default=data_file)

        # En sortie, répertoire de sortie
        self.add_button("output", default=output_directory)

        self.generate_btn = QtWidgets.QPushButton("Generate PDF")
        self.generate_btn.pressed.connect(self.generate)

        layout = QtWidgets.QFormLayout()

        for text, button in zip(self.texts.values(), self.buttons.values()):
            layout.addRow(text, button)
        layout.addRow(self.generate_btn)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_button(self, name, _format=None, default=""):
        self.texts[name] = QtWidgets.QLineEdit()
        self.texts[name].setText(default)
        self.texts[name].setMinimumWidth(800)
        self.texts[name].setDisabled(True)  # must use the file finder to select a valid file.

        self.buttons[name] = QtWidgets.QPushButton(f"Select {name.capitalize()}...")
        self.buttons[name].setMaximumWidth(200)
        self.buttons[name].pressed.connect(lambda: self.choose(name, _format))

    def choose(self, name, _format):
        """Method which call the native file dialog to choose file."""
        if _format is None:
            path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a folder")
        else:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Select a file", filter=f"{name.capitalize()} files {_format}"
            )
        if path:
            self.texts[name].setText(path)

    def generate(self):
        """Method triggered with the button to start the generation of pdf."""
        if not all([t.text() for t in self.texts.values()]):
            return None  # If one field is empty, ignore.

        self.generate_btn.setDisabled(True)
        process = Thread(*[t.text() for t in self.texts.values()])
        process.signals.finished.connect(self.generated)
        self.threadpool.start(process)
        return True

    def generated(self):
        """Success methdod"""
        self.generate_btn.setDisabled(False)
        QtWidgets.QMessageBox.information(self, "Finished", "PDFs have been generated")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    file_ = "C:/Users/guill/Documents/Projets/NDF_python/venv/src/ndf-python/data/test.xlsx"
    direct = "C:/Users/guill/Documents/Projets/NDF_python/venv/src/output"
    w = MainWindow(file_, direct)
    w.show()
    sys.exit(app.exec())
