# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtGui
from pyndf.constants import CONST
from pyndf.gui.dialogs.manual import ManualDialog


class MainMenu(QtWidgets.QMenuBar):
    """Main window of the app"""

    def __init__(self, window):
        super().__init__(parent=window)
        self.window = window

        # store special actions
        self._actions = {}

        # file
        self.addMenu(self.create_file_menu())

        # views
        self.addMenu(self.create_views_menu())

        # options
        self.addMenu(self.create_options_menu())

        # Help
        self.addMenu(self.create_help_menu())

        self.enable_dev_mode(False)

    def create_file_menu(self):
        menu = QtWidgets.QMenu(self.tr("File"), self)

        string = self.tr("Select")
        for name_env, label in self.window.tabs[CONST.TYPE.PRO].labels.items():
            menu.addAction(
                QtGui.QIcon(getattr(CONST.UI.ICONS, name_env)),
                " ".join([string, label.text()]),
                self.window.tabs[CONST.TYPE.PRO].buttons[name_env].pressed.emit,
            )
        menu.addSeparator()
        menu.addAction(QtGui.QIcon(CONST.UI.ICONS.PDF), self.tr("Generate PDF files"), self.window.generate)

        menu.addSeparator()
        menu.addAction(QtGui.QIcon(CONST.UI.ICONS.CLO), self.tr("Exit"), self.window.close, "Ctrl+Q")

        return menu

    def create_options_menu(self):
        menu = QtWidgets.QMenu(self.tr("Options"), self)

        # Language
        sub_menu = menu.addMenu(self.tr("Select language"))
        sub_menu.setIcon(QtGui.QIcon(CONST.UI.ICONS.LAN))
        for lang in self.window.app.language_available:
            sub_menu.addAction(
                QtGui.QIcon(getattr(CONST.UI.ICONS, lang)), lang, lambda l=lang: self.window.change_language(l)
            )
        menu.addSeparator()

        # PDF
        menu.addAction(QtGui.QIcon(CONST.UI.ICONS.COL), self.tr("Select PDF file color"), self.change_color_pdf)
        self._actions[CONST.TYPE.USE_MULTITHREAGING] = self.create_action_options(
            menu, self.tr("Use multithreading"), CONST.TYPE.USE_MULTITHREAGING
        )
        menu.addSeparator()

        # API
        self._actions[CONST.TYPE.DB] = self.create_action_options(menu, self.tr("Use DB"), CONST.TYPE.DB)
        self._actions[CONST.TYPE.CACHE] = self.create_action_options(menu, self.tr("Use CACHE"), CONST.TYPE.CACHE)
        self._actions[CONST.TYPE.USE_API] = self.create_action_options(menu, self.tr("Use API"), CONST.TYPE.USE_API)
        menu.addSeparator()

        # Dev mode
        action = QtGui.QAction(self.tr("Dev mode"), menu)
        action.setCheckable(True)
        action.setShortcut("Ctrl+D")
        action.toggled.connect(self.enable_dev_mode)
        action.setChecked(False)
        menu.addAction(action)

        return menu

    def enable_dev_mode(self, boolean):
        for analyse in CONST.TAB.ANALYSE + CONST.TAB.DB + CONST.MENU.API_ACTIONS:
            self._actions[analyse].setVisible(boolean)

    def create_views_menu(self):
        menu = QtWidgets.QMenu(self.tr("Views"), self)

        # Process
        self.create_action_views(menu, self.window.tabs[CONST.TYPE.PRO])
        menu.addSeparator()

        # Reader/Writer TAB_RW
        for reader in CONST.TAB.READER:
            self._actions[reader] = self.create_action_views(menu, self.window.tabs[reader])
        menu.addSeparator()

        # Analyse
        for analyse in CONST.TAB.ANALYSE:
            self._actions[analyse] = self.create_action_views(menu, self.window.tabs[analyse])
        menu.addSeparator()

        # DB
        for analyse in CONST.TAB.DB:
            self._actions[analyse] = self.create_action_views(menu, self.window.tabs[analyse])

        return menu

    def create_action_options(self, menu, title, name):
        action = QtGui.QAction(title, menu)
        action.setCheckable(True)
        action.toggled.connect(lambda boolean: setattr(self.window, name, boolean))
        attr = getattr(self.window, name)
        action.setChecked(attr if attr is not None else CONST.FILE.YAML[CONST.TYPE.API][name])
        menu.addAction(action)
        return action

    def create_action_views(self, menu, tab):
        action = QtGui.QAction(tab.title, menu)
        action.setCheckable(True)
        action.toggled.connect(lambda boolean, tab_=tab: self.window.toggled_tab(tab_, boolean))
        action.setChecked(self.window.controller_tab.isTabVisible(self.window.controller_tab.indexOf(tab)))
        menu.addAction(action)
        return action

    def create_help_menu(self):
        menu = QtWidgets.QMenu(self.tr("Help"), self)
        menu.setIcon(QtGui.QIcon(CONST.UI.ICONS.HEL))
        action = QtGui.QAction(QtGui.QIcon(CONST.UI.ICONS.MAN), self.tr("Manual"), self)
        action.setShortcut("F1")
        action.triggered.connect(self.open_manual)
        menu.addAction(action)

        return menu

    # Methods interaction
    def change_color_pdf(self):
        title = self.tr("Select PDF file color")
        try:
            initial = QtGui.QColor(self.window.color)
        except TypeError:
            initial = QtGui.QColor(CONST.WRITER.PDF.COLOR)

        color = QtWidgets.QColorDialog.getColor(initial=initial, title=title)

        if color.isValid():
            self.window.color = color.name()

    def open_manual(self):
        """Read the ReadMe file in package"""
        dialog = ManualDialog(self.window)
        dialog.exec()
