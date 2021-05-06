# -*- coding: utf-8 -*-

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, Integer, Table, ForeignKey


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self.__dict__)


Base = declarative_base(cls=Base)

association_table = Table(
    "association",
    Base.metadata,
    Column("client_id", Integer, ForeignKey("client.id")),
    Column("employee_id", Integer, ForeignKey("employee.id")),
)
