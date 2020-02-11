class Handler:

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        raise NotImplementedError('Handler must have a method "run"')

    @property
    def uid(self):
        return self.__class__
