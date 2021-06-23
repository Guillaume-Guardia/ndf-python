# -*- coding: utf-8 -*-

from pyndf.gui.tables.abstract import AbstractTable
from pyndf.db.session import db


class DbTable(AbstractTable):
    def __init__(self, tab, item):
        super().__init__(tab, item)
        with db.session_scope() as session:
            items = session.query(self.custom_item.db_class).all()

            for item in items:
                self.add(self.custom_item(item))
