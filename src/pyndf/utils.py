# -*- coding: utf-8 -*-

import re
from datetime import datetime


class Utils:
    @staticmethod
    def type(value: str, decimal: str = "."):
        try:
            value = value.replace(decimal, ".")
            if value.lower() == "true":
                return True

            if value.lower() == "false":
                return False

            float_value = float(value)
            int_value = int(float_value)

            if float_value == int_value:
                return int_value
            return float_value
        except ValueError:
            return value
        except AttributeError:
            return value

    @staticmethod
    def getattr(obj, name):
        if isinstance(name, set):
            name = list(name)

        if isinstance(name, list):
            name = "/".join(name)

        return getattr(obj, name)

    @staticmethod
    def insert(l: list, index: int, value: str):
        return l[:index] + str(value) + l[index:]

    @staticmethod
    def pretty_join(string: str):
        return " ".join(string.split())

    @staticmethod
    def pretty_split(string: str):
        split = string.split("|")
        if len(split) > 0:
            return split[0], split[1]
        return split

    @staticmethod
    def get_date_from_file(path: str):
        regex = re.compile(r"^.*_(?P<date>\d{6}).*$")

        match = regex.match(path)
        if match is not None:
            date = match.groupdict()["date"]
            return datetime(year=int(date[:4]), month=int(date[4:6]), day=1)
        return None


class Factory:
    def __new__(cls, type_, *args, **kwargs):
        _class = cls.class_dico[type_]
        if len(args) + len(kwargs) <= 0:
            return _class
        instance = _class.__new__(_class, *args, **kwargs)
        instance.__init__(*args, **kwargs)
        return instance


if __name__ == "__main__":
    # Check int
    a = "5"

    assert Utils.type(a) == 5

    # Check float
    a = "5.1"

    assert Utils.type(a) == 5.1

    # Check float
    a = "dhgidsgisc"

    assert Utils.type(a) == a
