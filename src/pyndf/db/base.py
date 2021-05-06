# -*- coding: utf-8 -*-

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, Integer


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self.__dict__)


Base = declarative_base(cls=Base)
