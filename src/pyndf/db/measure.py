# -*- coding: utf-8 -*-

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from pyndf.db.base import Base
from pyndf.db.client import Client
from pyndf.db.employee import Employee


class Measure(Base):
    """Db class"""

    # Client relation one to many
    client_address = Column(String, ForeignKey(f"{Client.__tablename__}.address"))
    client = relationship("Client", back_populates="measures")

    # Employee relation one to many
    employee_address = Column(String, ForeignKey(f"{Employee.__tablename__}.address"))
    employee = relationship("Employee", back_populates="measures")

    # real attributes
    distance = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
