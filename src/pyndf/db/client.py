# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from pyndf.db.base import Base


class Client(Base):
    """Db class"""

    name = Column(String, nullable=False)

    # Employee relation many to many -> backref

    # Measure relation many to one
    measures = relationship("Measure")

    # Real attribute
    address = Column(String, nullable=False)
