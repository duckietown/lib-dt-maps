from dt_maps import Map
from dt_maps.types.commons import EntityHelper


class TileSize(EntityHelper):

    def __init__(self, m: Map, key: str):
        super(TileSize, self).__init__(m, key)
        self._map = m
        self._key = key

    def __getitem__(self, item: str):
        return {
            "x": self.x,
            "y": self.y,
        }[item]

    def _set_property(self, name: str, value: float):
        self._map.layers.tile_maps[self._key]["tile_size"][name] = value

    def _get_property(self, name: str) -> float:
        return self._map.layers.tile_maps[self._key]["tile_size"][name]

    @property
    def x(self) -> float:
        return self._get_property("x")

    @property
    def y(self) -> float:
        return self._get_property("y")

    @x.setter
    def x(self, value: float):
        self._set_property("x", value)

    @y.setter
    def y(self, value: float):
        self._set_property("y", value)


class TileMap(EntityHelper):

    def __init__(self, m: Map, tile_key: str):
        super(TileMap, self).__init__()
        self._map = m
        self._key = tile_key

    @property
    def tile_size(self) -> TileSize:
        return TileSize.create(self._map, self._key)
