from abc import abstractmethod
from typing import Any, Iterable, Union

from dt_maps.exceptions import FieldNotFound, assert_type

FieldPath = Union[str, Iterable[str]]


class EntityHelper:

    # NOTE: lazy instantiation is needed
    _cache = None

    def __init__(self, m, key: str, *_, **__):
        self._map = m
        self._key = key

    def __getitem__(self, key: str):
        return self._get_property(key)

    def __setitem__(self, key: str, value: Any):
        try:
            property_type = self._get_property_types(key)
        except KeyError:
            raise FieldNotFound(self._key, None, key, type(self))
        # ---
        return self._set_property(key, property_type, value)

    @abstractmethod
    def _get_layer_name(self) -> str:
        pass

    @abstractmethod
    def _get_property_types(self, name: str):
        pass

    # @abstractmethod
    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        name = name if isinstance(name, (list, tuple)) else [name]
        assert_type(value, types, str(name))
        layer_name: str = self._get_layer_name()
        layer = self._map.get_layer(layer_name)
        layer.write(self._key, name, value)

    # @abstractmethod
    def _get_property(self, name: FieldPath) -> Any:
        name = name if isinstance(name, (list, tuple)) else [name]
        layer_name: str = self._get_layer_name()
        layer = self._map.get_layer(layer_name)
        return layer.read(self._key, name)

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
