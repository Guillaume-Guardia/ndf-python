# -*- coding: utf-8 -*-

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyndf.constants import CONST
from pyndf.logbook import Logger
from pyndf.db.base import Base
from pyndf.db.client import Client
from pyndf.db.employee import Employee
from pyndf.db.measure import Measure
from pyndf.utils import Utils


class Database(Logger):
    DB_ENGINE = {"sqlite": "sqlite:///{DB}"}

    def __init__(self, dbtype, dbname="", base=None, verbose=False):
        super().__init__()
        self.base = base
        if dbtype in self.DB_ENGINE:
            self.engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
        else:
            self.engine_url = "sqlite:///:memory:"
            self.log.warning("DBType is not found in DB_ENGINE")

        self.db_engine = create_engine(self.engine_url, echo=verbose)
        self.session = sessionmaker(bind=self.db_engine)
        with self.session_scope() as session:
            self.base.metadata.create_all(self.db_engine)

            # Create Agence clients
            for value in CONST.FILE.YAML[CONST.TYPE.AGENCE].values():
                name, address = Utils.pretty_split(value)
                if session.query(Client).filter_by(name=name).first() is None:
                    session.add(Client(name=name, address=Utils.format_address(address)))

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        if not self.session:
            return

        db_session = self.session()
        try:
            yield db_session
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()


db = Database(dbtype="sqlite", dbname=CONST.FILE.DB, base=Base)
