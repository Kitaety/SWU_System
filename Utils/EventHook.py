class EventHook(object):
    def __init__(self):
        self.__handlers = []

    def connect(self, handler):
        self.__handlers.append(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)
