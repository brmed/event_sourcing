from django.dispatch import Signal
from django.conf import settings


class Event:

    __signals = dict()

    def __new__(cls, *args, **kwargs):
        if not cls.__signals.get(cls):
            cls.__signals[cls] = Signal(providing_args=[])
        cls.signal = cls.__signals[cls]
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def notify(self):
        if settings.DEBUG:
            response = self.signal.send(
                sender=self.__class__, **self.kwargs)
        else:
            response = self.signal.send_robust(
                sender=self.__class__, **self.kwargs)
        return response

    def connect_signal(self, handler):
        self.signal.connect(handler, dispatch_uid=handler.uid, weak=False)
