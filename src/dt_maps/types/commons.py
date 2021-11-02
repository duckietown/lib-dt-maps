from abc import abstractmethod


class EntityHelper:

    # NOTE: lazy instantiation is needed
    _cache = None

    def __init__(self, m, key: str, *_, **__):
        self._map = m
        self._key = key

    @abstractmethod
    def __getitem__(self, item: str):
        pass

    @classmethod
    def create(cls, m, key: str, *args, **kwargs):
        # lazy instantiation
        if cls._cache is None:
            cls._cache = {}
        # try cache
        obj = cls._cache.get((id(m), key), None)
        if obj is None:
            # create new and cache it
            obj = cls(m, key, *args, **kwargs)
            cls._cache[(id(m), key)] = obj
        # ---
        return obj
