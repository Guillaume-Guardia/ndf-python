# -*- coding: utf-8 -*-

import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from pyndf.logbook import Logger
from pyndf.process.thread import Thread
from pyndf.constants import CONFIG


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, data_file="", output_directory="", resolution=None):
        super().__init__()
        self.threadpool = QtCore.QThreadPool()

        self.setWindowTitle("pyNDF")
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TitleBarMenuButton))
        if resolution:
            self.setFixedWidth(int(resolution.width() / 2))
            self.setFixedHeight(int(resolution.height() / 8))

        self.buttons = {}
        self.texts = {}

        # En entrée, feuille excel
        self.add_button("excel", "(*.xl*)", default=data_file)

        # En sortie, répertoire de sortie
        self.add_button("output", default=output_directory)

        self.generate_btn = QtWidgets.QPushButton("Generate PDF")
        self.generate_btn.setStyleSheet(CONFIG["buttonstyle"])
        self.generate_btn.pressed.connect(self.generate)
        self.generate_btn.setFixedWidth(int(self.width() * 0.2))

        layout = QtWidgets.QGridLayout()

        for index, (text, button) in enumerate(zip(self.texts.values(), self.buttons.values())):
            hlay2 = QtWidgets.QHBoxLayout()
            hlay2.setContentsMargins(0, 0, 0, 0)

            hlay2.addWidget(text)
            hlay2.addStretch()
            hlay2.addWidget(button)

            new_widget = QtWidgets.QWidget()
            new_widget.setLayout(hlay2)

            layout.addWidget(new_widget, index, 0)

        hlay2 = QtWidgets.QHBoxLayout()
        hlay2.setContentsMargins(0, 0, 0, 0)
        hlay2.addStretch()
        hlay2.addWidget(self.generate_btn)
        hlay2.addStretch()

        new_widget = QtWidgets.QWidget()
        new_widget.setLayout(hlay2)

        layout.addWidget(new_widget, 2, 0)

        self.progress = QtWidgets.QProgressBar()
        self.progress.hide()
        layout.addWidget(self.progress)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_button(self, name, _format=None, default=""):
        self.texts[name] = QtWidgets.QLineEdit()
        self.texts[name].setText(default)
        self.texts[name].setFixedWidth(int(self.width() * 0.7))
        self.texts[name].setDisabled(True)  # must use the file finder to select a valid file.

        self.buttons[name] = QtWidgets.QPushButton(f"Select {name.capitalize()}...")
        self.buttons[name].setFixedWidth(int(self.width() * 0.2))
        self.buttons[name].pressed.connect(lambda: self.choose(name, _format))
        self.buttons[name].setStyleSheet(CONFIG["buttonstyle"])

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

        self.progress.show()
        self.generate_btn.setDisabled(True)
        process = Thread(*[t.text() for t in self.texts.values()])
        process.signals.finished.connect(self.generated)
        process.signals.progressed.connect(self.progressed)
        self.threadpool.start(process)
        return True

    def progressed(self, value):
        if value <= 100:
            self.progress.setValue(int(value))

    def generated(self):
        """Success methdod"""
        self.progress.hide()
        self.progress.reset()
        self.generate_btn.setDisabled(False)
        QtWidgets.QMessageBox.information(self, "Finished", "PDFs have been generated")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    file_ = "C:/Users/guill/Documents/Projets/NDF_python/venv/src/ndf-python/data/test.xlsx"
    direct = "C:/Users/guill/Documents/Projets/NDF_python/venv/src/output"

    resolution = app.primaryScreen().availableSize()
    w = MainWindow(file_, direct, resolution=resolution)
    w.show()
    sys.exit(app.exec())
