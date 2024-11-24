class SingletonClass:
    _instants = None

    def __new__(cls, *arg, **kargs):
        if cls._instants is None:
            cls._instants = super().__new__(cls, *arg, **kargs)
        return cls._instants