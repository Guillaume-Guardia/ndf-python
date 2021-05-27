# -*- coding: utf-8 -*-


class Progress:
    def __init__(self, callback, global_min=0, global_max=0, local_max=100):
        self.callback = callback
        self.global_min = global_min
        self.global_max = global_max
        self.global_value = global_min

        self.local_min = 0
        self.local_max = local_max
        self.local_value = 0

    def add_duration(self, duration, local_max=100):
        self.global_min = self.global_max
        self.global_max += duration

        self.local_min = 0
        self.local_max = local_max
        self.local_value = 0

    @property
    def global_duration(self):
        return self.global_max - self.global_min

    @property
    def local_duration(self):
        return self.local_max - self.local_min

    def set_maximum(self, local_max):
        self.local_max = local_max
        self.local_value = self.local_min
        self.global_min = self.global_value

    def send(self, value=None, msg=""):
        if value is None:
            self.local_value += 1
        else:
            self.local_value = value
        msg += f": {self.local_value} / {self.local_max}"

        self.global_value = self.global_min + (self.local_value / self.local_duration) * self.global_duration

        return self.callback(round(self.global_value), msg)
