# -*- coding: utf-8 -*-


class Utils:
    @staticmethod
    def type(value: str, decimal: str = "."):
        value = value.replace(decimal, ".")
        try:
            float_value = float(value)
            int_value = int(float_value)

            if float_value == int_value:
                return int_value
            return float_value
        except ValueError:
            return value


class Factory:
    def __new__(cls, type, *args, **kwargs):
        _class = cls.class_dico[type]
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
