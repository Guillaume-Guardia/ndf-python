# -*- coding: utf-8 -*-

from pyndf.gui.tabs.abstract import AbstractTab
from pyndf.gui.widgets.combobox import FileSelectComboBox
from pyndf.qtlib import QtWidgets, QtGui
from pyndf.constants import CONST


class ProcessTab(AbstractTab):
    def __init__(self, window, title):
        super().__init__(window, title)

        # Graphics elements
        self.icons = {}
        self.labels = {}
        self.buttons = {}
        self.combos = {}

        # Explorer buttons
        self.add_button(CONST.TYPE.EXC, self.tr("EXCEL file"), "(*.xl* *.XLS)", default=window.excel)
        self.add_button(CONST.TYPE.CSV, self.tr("CSV file"), "(*.csv)", default=window.csv)
        self.add_button(CONST.TYPE.OUT, self.tr("Save directory"), default=window.output)

        # Add grid layout
        grid_layout = QtWidgets.QGridLayout()
        for row, widgets in enumerate(
            zip(self.icons.values(), self.labels.values(), self.combos.values(), self.buttons.values())
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
        generate_widget = ProcessTab.add_widget([self.buttons[CONST.TYPE.PDF]])

        # Create vertical layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(grid_widget)
        layout.addStretch()
        layout.addWidget(generate_widget)
        layout.addStretch()

        self.setLayout(layout)

    def add_button(self, name_env, name, _format=None, default=None):
        """Add label, text + button

        Args:
            name_env (str): name of button in app
            name (str): name of the button
            _format (str, optional): format of file. Defaults to None.
            default (list, optional): default list text in memory. Defaults to None.
        """
        # Icon
        self.icons[name_env] = QtWidgets.QLabel(name)
        pix = QtGui.QPixmap(getattr(CONST.UI.ICONS, name_env))
        if pix:
            self.icons[name_env].setPixmap(pix.scaledToHeight(15))
        self.icons[name_env].setFixedWidth(20)

        # Name
        self.labels[name_env] = QtWidgets.QLabel(name)
        self.labels[name_env].setFixedWidth(150)

        # Text
        self.combos[name_env] = FileSelectComboBox(self.window, name_env, default)

        # Button explorer
        self.buttons[name_env] = QtWidgets.QPushButton("...")
        self.buttons[name_env].setFixedHeight(30)
        self.buttons[name_env].setFixedWidth(45)
        self.buttons[name_env].pressed.connect(lambda: self.choose(name_env, name, _format))

    @staticmethod
    def add_widget(widgets):
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
            path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Open"))
            if not path:
                return
            paths = [path]
        else:
            paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                self.tr("Open"),
                filter=f"{name} {_format}" + f";;{self.tr('All files')} *" * CONST.READER.CAN_ADD_ALL_FILES,
            )

        self.combos[name_env].add_items(paths)
