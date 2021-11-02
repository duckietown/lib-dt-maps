from enum import Enum
from typing import Tuple

from dt_maps import Map
from dt_maps.exceptions import assert_type
from dt_maps.types.commons import EntityHelper
from dt_maps.types.frames import Frame

TileCoordinates = Tuple[int, int]


class TileType(Enum):
    STRAIGHT = "straight"
    CURVE = "curve"
    ASPHALT = "asphalt"
    GRASS = "grass"
    THREE_WAY = "3way"
    FOUR_WAY = "4way"


class TileOrientation(Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"


class Tile(EntityHelper):

    def __init__(self, m: Map, tile_key: str):
        super(Tile, self).__init__(m, tile_key)
        self._map = m
        self._key = tile_key

    def _get_property_types(self, name: str):
        return {
            "i": int,
            "j": int,
            "type": str,
            "orientation": str,
        }[name]

    def _get_layer_name(self) -> str:
        return "tiles"

    @property
    def frame(self) -> Frame:
        return Frame.create(self._map, self._key)

    @property
    def i(self) -> int:
        return self._get_property("i")

    @property
    def j(self) -> int:
        return self._get_property("j")

    @property
    def type(self) -> TileType:
        return TileType(self._get_property("type"))

    @property
    def orientation(self) -> TileOrientation:
        return TileOrientation(self._get_property("orientation"))

    @i.setter
    def i(self, value: int):
        self._set_property("i", int, value)

    @j.setter
    def j(self, value: int):
        self._set_property("j", int, value)

    @type.setter
    def type(self, value: TileType):
        assert_type(value, TileType, "type")
        self._set_property("type", str, value.value)

    @orientation.setter
    def orientation(self, value: TileOrientation):
        assert_type(value, TileOrientation, "orientation")
        self._set_property("orientation", str, value.value)
