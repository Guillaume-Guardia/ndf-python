# -*- coding: utf-8 -*-

from markdown import markdown
from pyndf.qtlib import QtWidgets, QtGui
from pyndf.constants import LOGO, PDF_COLOR, README_FILE, TAB_PRO, TAB_ANA, TITLE_APP, VERSION, DEFAULT_FONT


class MainMenu(QtWidgets.QMenuBar):
    """Main window of the app"""

    def __init__(self, window):
        super().__init__(parent=window)
        self.window = window

        # file
        self.addMenu(self.create_file_menu())

        # views
        self.addMenu(self.create_views_menu())

        # options
        self.addMenu(self.create_options_menu())

        # Help
        self.addMenu(self.create_help_menu())

    def create_file_menu(self):
        menu = QtWidgets.QMenu(self.tr("File"), self)

        string = self.tr("Add")
        for name_env, label in self.window.tabs[TAB_PRO].labels.items():
            menu.addAction(" ".join([string, label.text()]), self.window.tabs[TAB_PRO].buttons[name_env].pressed.emit)

        menu.addSeparator()
        exit_action = QtGui.QAction(self.tr("Exit"), self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.window.close)
        menu.addAction(exit_action)

        return menu

    def create_options_menu(self):
        menu = QtWidgets.QMenu(self.tr("Options"), self)

        # Language
        sub_menu = menu.addMenu(self.tr("Select language"))
        for lang in self.window.app.language_available:
            sub_menu.addAction(lang, lambda l=lang: self.window.change_language(l))

        # Color PDF
        menu.addAction(self.tr("Select Color PDF"), self.change_color_pdf)

        return menu

    def create_views_menu(self):
        menu = QtWidgets.QMenu(self.tr("Views"), self)
        for tab in [self.window.tabs[TAB_PRO]] + list(self.window.tabs[TAB_ANA].values()):
            new_action = QtGui.QAction(tab.title, menu)
            new_action.setCheckable(True)
            new_action.setChecked(True)
            new_action.toggled.connect(lambda boolean, tab_=tab: self.window.toggled_tab(tab_, boolean))
            menu.addAction(new_action)

        return menu

    def create_help_menu(self):
        menu = QtWidgets.QMenu(self.tr("Help"), self)

        manual = QtGui.QAction(self.tr("Manual"), self)
        manual.setShortcut("F1")
        manual.triggered.connect(self.open_manual)
        menu.addAction(manual)

        action = QtGui.QAction(
            self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxQuestion), "Help", self
        )
        action.triggered.connect(self.open_help)
        menu.addAction(action)

        return menu

    # Methods interaction
    def change_color_pdf(self):
        self.window.log.info("Color picker open")

        title = self.tr("Select color for PDF")
        try:
            initial = QtGui.QColor(self.window.color)
        except TypeError:
            initial = QtGui.QColor(PDF_COLOR)

        color = QtWidgets.QColorDialog.getColor(initial=initial, title=title)

        if color.isValid():
            self.window.color = color.name()

    def open_manual(self):
        """Read the ReadMe file in package"""
        self.window.log.info("Manual open")
        dialog = QtWidgets.QDialog(self.window)
        dialog.setWindowTitle(self.tr("Manuel"))
        dialog.setMinimumHeight(400)
        dialog.setMinimumWidth(400)

        scrollAreaWidgetContents = QtWidgets.QWidget()

        layout = QtWidgets.QVBoxLayout()
        with open(README_FILE) as opened_file:
            for line in opened_file.readlines():
                layout.addWidget(QtWidgets.QLabel(markdown(line)))

        scrollAreaWidgetContents.setLayout(layout)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)

        scrollArea.setWidget(scrollAreaWidgetContents)

        layoutV = QtWidgets.QVBoxLayout()
        version = QtWidgets.QLabel(f"{TITLE_APP}")
        version.setFont(QtGui.QFont(DEFAULT_FONT[0], 20))
        layoutV.addWidget(version)
        image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(LOGO)
        pixmap.scaledToWidth(50)
        image.setPixmap(pixmap)
        image.setScaledContents(False)
        layoutV.addWidget(image)
        version = QtWidgets.QLabel(f"version: {VERSION}")
        layoutV.addWidget(version)

        widget = QtWidgets.QWidget()
        widget.setLayout(layoutV)

        layout_main = QtWidgets.QHBoxLayout()
        layout_main.addWidget(widget)
        layout_main.addWidget(scrollArea)
        dialog.setLayout(layout_main)
        dialog.exec()

    def open_help(self):
        self.window.log.info("Help open!")
