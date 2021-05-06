# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from pyndf.db.base import Base


class Client(Base):
    """Db class"""

    address = Column(String, nullable=False, unique=True)
