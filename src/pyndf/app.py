# -*- coding: utf-8 -*-

import sys
import argparse
from PyQt6 import QtWidgets, QtCore
from pyndf.logbook import Logger
from pyndf.process.thread import Thread
from pyndf.constants import CONFIG, TRANSLATION_DIR


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, data="", output="", resolution=None):
        super().__init__()
        self.threadpool = QtCore.QThreadPool()

        self.setWindowTitle("PYNDF")
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TitleBarMenuButton))
        if resolution:
            self.setMinimumWidth(int(resolution.width() / 1.5))
            self.setMinimumHeight(int(resolution.height() / 3))

        self.tabs = QtWidgets.QTabWidget()
        self.param_tab = QtWidgets.QWidget()
        self.analyse_tab = QtWidgets.QWidget()

        self.labels = {}
        self.buttons = {}
        self.texts = {}

        self.set_param_tab(self.param_tab, data, output)

        self.tabs.addTab(self.param_tab, self.tr("Parameters"))
        self.tabs.addTab(self.analyse_tab, self.tr("Analyse"))

        # Progress Bar in status bar ?
        status_bar = QtWidgets.QStatusBar()
        self.progress = QtWidgets.QProgressBar()
        self.progress.hide()
        status_bar.addPermanentWidget(self.progress, 0)
        self.setStatusBar(status_bar)

        self.setCentralWidget(self.tabs)

    def set_param_tab(self, tab, data, output):
        layout = QtWidgets.QVBoxLayout()

        # Explorer buttons
        self.add_button(self.tr("excel file"), "(*.xl*)", default=data)
        self.add_button(self.tr("output directory"), default=output)

        grid_layout = QtWidgets.QGridLayout()
        for row, widgets in enumerate(zip(self.labels.values(), self.texts.values(), self.buttons.values())):
            for col, widget in enumerate(widgets):
                grid_layout.addWidget(widget, row, col)
        new_widget = QtWidgets.QWidget()
        new_widget.setLayout(grid_layout)
        layout.addWidget(new_widget)

        # Generate button
        self.buttons["generate"] = QtWidgets.QPushButton(self.tr("Generate PDFs"))
        self.buttons["generate"].pressed.connect(self.generate)
        self.buttons["generate"].setMinimumWidth(120)
        self.buttons["generate"].setMinimumHeight(40)
        self.buttons["generate"].setStyleSheet(CONFIG["buttonstyle"])

        widget = self.add_widget([self.buttons["generate"]])
        layout.addStretch()
        layout.addWidget(widget)
        layout.addStretch()

        tab.setLayout(layout)

    def add_widget(self, widgets):
        # Create Horizontal Layout
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()

        for ind, widget in enumerate(widgets):
            layout.addWidget(widget)
            if ind < len(widgets) - 1:
                layout.addStretch()

        layout.addStretch()

        new_widget = QtWidgets.QWidget()
        new_widget.setLayout(layout)
        return new_widget

    def add_button(self, name, _format=None, default=""):
        self.labels[name] = QtWidgets.QLabel(name.capitalize())
        self.texts[name] = QtWidgets.QLineEdit()
        self.texts[name].setText(default)
        self.texts[name].setFixedHeight(30)
        self.texts[name].setDisabled(True)  # must use the file finder to select a valid file.

        self.buttons[name] = QtWidgets.QPushButton("...")
        self.buttons[name].setFixedHeight(30)
        self.buttons[name].pressed.connect(lambda: self.choose(name, _format))

    def choose(self, name, _format):
        """Method which call the native file dialog to choose file."""
        if _format is None:
            path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select a folder"))
        else:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, self.tr("Select a file"), filter=f"{name.capitalize()} {_format}"
            )
        if path:
            self.texts[name].setText(path)

    def generate(self):
        """Method triggered with the button to start the generation of pdf."""
        if not all([t.text() for t in self.texts.values()]):
            return None  # If one field is empty, ignore.

        self.progress.show()
        self.buttons["generate"].setDisabled(True)
        process = Thread(*[t.text() for t in self.texts.values()])
        process.signals.finished.connect(self.generated)
        process.signals.progressed.connect(self.progressed)
        self.threadpool.start(process)
        return True

    def progressed(self, value, text):
        if value <= 100:
            self.progress.setValue(int(value))
            self.statusBar().showMessage(text, 1000)

    def generated(self):
        """Success methdod"""
        self.progress.hide()
        self.progress.reset()
        self.buttons["generate"].setDisabled(False)
        QtWidgets.QMessageBox.information(self, self.tr("Finished"), self.tr("PDFs have been generated !"))


def main(language="", **kwargs):
    app = QtWidgets.QApplication([])

    translator = QtCore.QTranslator()

    # Load translator
    locale = QtCore.QLocale()
    if language:
        locale = QtCore.QLocale(language)

    if translator.load(locale, "pyndf", "_", TRANSLATION_DIR, ".qm"):
        # Install translator
        app.installTranslator(translator)

    res = app.primaryScreen().availableSize()
    w = MainWindow(**kwargs, resolution=res)

    w.show()
    sys.exit(app.exec())


def cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    parser.add_argument("-e", "--excel", help="Excel file to parse", type=str)
    parser.add_argument("-o", "--output", help="Output directory", type=str)
    parser.add_argument("-l", "--language", help="Select language (en, fr)", type=str)

    args = parser.parse_args()

    args.excel = "C:/Users/guill/Documents/Projets/NDF_python/venv/src/ndf-python/data/test.xlsx"
    args.output = "C:/Users/guill/Documents/Projets/NDF_python/venv/src/output"

    main(data=args.excel, output=args.output, language=args.language)


if __name__ == "__main__":
    cmdline()
