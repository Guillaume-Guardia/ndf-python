# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from pyndf.db.base import Base, association_table


class Employee(Base):
    """Db class"""

    matricule = Column(String)

    # Client relation many to many
    clients = relationship("Client", secondary=association_table, backref="employees")

    # Measure relation many to one
    measures = relationship("Measure")

    # Real attribute
    address = Column(String, nullable=False, unique=True)
