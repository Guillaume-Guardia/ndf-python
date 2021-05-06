# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Float, ForeignKey
from pyndf.db.base import Base
from pyndf.db.client import Client
from pyndf.db.employee import Employee


class Measure(Base):
    """Db class"""

    client_address = Column(Integer, ForeignKey(f"{Client.__tablename__}.address"))
    employee_address = Column(Integer, ForeignKey(f"{Employee.__tablename__}.address"))
    distance = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
