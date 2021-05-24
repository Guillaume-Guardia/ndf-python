# -*- coding: utf-8 -*-

import os
from pyndf.gui.tabs.abstract import AbstractTab
from pyndf.process.reader.factory import Reader
from pyndf.qtlib import QtWidgets, QtGui
from pyndf.constants import CONST


class ProcessTab(AbstractTab):
    def __init__(self, window, title, excel="", csv="", output=""):
        super().__init__(window, title)

        # Graphics elements
        self.icons = {}
        self.labels = {}
        self.buttons = {}
        self.texts = {}

        # Explorer buttons
        self.add_button(CONST.TYPE.EXC, self.tr("EXCEL file"), "(*.xl* *.XLS)", default=excel)
        self.add_button(CONST.TYPE.CSV, self.tr("CSV file"), "(*.csv)", default=csv)
        self.add_button(CONST.TYPE.OUT, self.tr("save directory"), default=output)

        # Add grid layout
        grid_layout = QtWidgets.QGridLayout()
        for row, widgets in enumerate(
            zip(self.icons.values(), self.labels.values(), self.texts.values(), self.buttons.values())
        ):
            for col, widget in enumerate(widgets):
                grid_layout.addWidget(widget, row, col)
        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(grid_layout)

        # Generate button
        self.buttons[CONST.TYPE.PDF] = QtWidgets.QPushButton(self.tr("Generate PDF files"))
        self.buttons[CONST.TYPE.PDF].pressed.connect(self.window.generate)
        self.buttons[CONST.TYPE.PDF].setMinimumWidth(120)
        self.buttons[CONST.TYPE.PDF].setMinimumHeight(40)
        self.buttons[CONST.TYPE.PDF].setStyleSheet(CONST.UI.BUTTONSTYLE)
        generate_widget = self.add_widget([self.buttons[CONST.TYPE.PDF]])

        # Create vertical layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(grid_widget)
        layout.addStretch()
        layout.addWidget(generate_widget)
        layout.addStretch()

        self.setLayout(layout)

    def add_data(self, filename, name):
        if not os.path.exists(filename):
            setattr(self.window, name, "")
            self.texts[name].setText("")

        if name not in CONST.TAB.READER:
            return

        self.window.tabs[name].table.init(clear=True)
        Reader(filename, analyse_callback=self.window.tabs[name].table.add, log_level=self.window.log_level)
        self.window.tabs[name].table.finished()

    def add_button(self, name_env, name, _format=None, default=""):
        """Add label, text + button

        Args:
            name_env (str): name of button in app
            name (str): name of the button
            _format (str, optional): format of file. Defaults to None.
            default (str, optional): default text. Defaults to "".
        """
        self.icons[name_env] = QtWidgets.QLabel()
        pix = QtGui.QPixmap(getattr(CONST.UI.ICONS, name_env))
        if pix:
            self.icons[name_env].setPixmap(pix.scaledToHeight(15))
        self.labels[name_env] = QtWidgets.QLabel(name.capitalize())
        self.texts[name_env] = QtWidgets.QLineEdit()
        self.texts[name_env].textChanged.connect(lambda filename: self.add_data(filename, name_env))
        self.texts[name_env].setText(default)
        self.texts[name_env].setFixedHeight(30)
        self.texts[name_env].setDisabled(True)  # must use the file finder to select a valid file.

        self.buttons[name_env] = QtWidgets.QPushButton("...")
        self.buttons[name_env].setFixedHeight(30)
        self.buttons[name_env].pressed.connect(lambda: self.choose(name_env, name, _format))

    def add_widget(self, widgets):
        """add widget in center of Horizontal layout

        Args:
            widgets (list): list of widgets to add

        Returns:
            Widget: Horizontal widget
        """
        # Create Horizontal Layout
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()

        for ind, widget in enumerate(widgets):
            layout.addWidget(widget)
            if ind < len(widgets) - 1:
                layout.addStretch()

        layout.addStretch()

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        return widget

    def choose(self, name_env, name, _format):
        """Method which call the native file dialog to choose file."""
        if _format is None:
            path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select folder"))
        else:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, self.tr("Select file"), filter=f"{name.capitalize()} {_format}"
            )
        if path:
            self.texts[name_env].setText(path)
            setattr(self.window, name_env, path)
