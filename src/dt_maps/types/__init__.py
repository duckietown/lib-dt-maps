from .map import MapLayer, MapAsset
from .tiles import Tile
from .. import Map


class EntityHelper:

    _cache = {}

    def __init__(self, *_, **__):
        pass

    @classmethod
    def create(cls, m: Map, key: str, *args, **kwargs):
        return cls._cache.get((id(m), key), None) or cls(*args, **kwargs)
