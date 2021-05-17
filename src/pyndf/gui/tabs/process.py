# -*- coding: utf-8 -*-


from pyndf.qtlib import QtWidgets

from pyndf.constants import CONFIG


class ProcessTab(QtWidgets.QWidget):
    def __init__(self, window, title, excel="", csv="", output=""):
        super().__init__()
        self.window = window
        self.title = title

        # Graphics elements
        self.labels = {}
        self.buttons = {}
        self.texts = {}

        # Explorer buttons
        self.add_button(self.tr("EXCEL file"), "(*.xl* *.XLS)", default=excel)
        self.add_button(self.tr("CSV file"), "(*.csv)", default=csv)
        self.add_button(self.tr("output directory"), default=output)

        # Add grid layout
        grid_layout = QtWidgets.QGridLayout()
        for row, widgets in enumerate(zip(self.labels.values(), self.texts.values(), self.buttons.values())):
            for col, widget in enumerate(widgets):
                grid_layout.addWidget(widget, row, col)
        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(grid_layout)

        # Generate button
        self.buttons["generate"] = QtWidgets.QPushButton(self.tr("Generate PDFs"))
        self.buttons["generate"].pressed.connect(self.window.generate)
        self.buttons["generate"].setMinimumWidth(120)
        self.buttons["generate"].setMinimumHeight(40)
        self.buttons["generate"].setStyleSheet(CONFIG["buttonstyle"])
        generate_widget = self.add_widget([self.buttons["generate"]])

        # Create vertical layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(grid_widget)
        layout.addStretch()
        layout.addWidget(generate_widget)
        layout.addStretch()

        self.setLayout(layout)

    def add_button(self, name, _format=None, default=""):
        """Add label, text + button

        Args:
            name (str): name of the button
            _format (str, optional): format of file. Defaults to None.
            default (str, optional): default text. Defaults to "".
        """
        self.labels[name] = QtWidgets.QLabel(name.capitalize())
        self.texts[name] = QtWidgets.QLineEdit()
        self.texts[name].setText(default)
        self.texts[name].setFixedHeight(30)
        self.texts[name].setDisabled(True)  # must use the file finder to select a valid file.

        self.buttons[name] = QtWidgets.QPushButton("...")
        self.buttons[name].setFixedHeight(30)
        self.buttons[name].pressed.connect(lambda: self.choose(name, _format))

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
