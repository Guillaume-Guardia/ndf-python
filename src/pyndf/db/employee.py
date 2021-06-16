# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from pyndf.db.base import Base, association_table


class Employee(Base):
    """Db class"""

    matricule = Column(Integer, nullable=False, unique=True)

    # Client relation many to many
    clients = relationship("Client", secondary=association_table, backref="employees")

    # Measure relation many to one
    measures = relationship("Measure")

    # Real attribute
    address = Column(String, nullable=False)
