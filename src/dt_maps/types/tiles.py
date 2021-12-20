from enum import Enum
from typing import Tuple, Union, Iterable, Any, Optional

from dt_maps.types.commons import EntityHelper, FieldPath
from dt_maps.types.frames import Frame

TileCoordinates = Tuple[int, int]


class TileType(Enum):
    STRAIGHT = "straight"
    CURVE_LEFT = "curve_left"
    CURVE_RIGHT = "curve_right"
    ASPHALT = "asphalt"
    FLOOR = "floor"
    GRASS = "grass"
    THREE_WAY_LEFT = "3way_left"
    THREE_WAY_RIGHT = "3way_right"
    FOUR_WAY = "4way"


class TileOrientation(Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"


class Tile(EntityHelper):

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            "i": int,
            "j": int,
            "type": str,
            "orientation": str,
        }[name]

    def _get_layer_name(self) -> str:
        return "tiles"

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            "i": None,
            "j": None,
            "type": [t.value for t in TileType],
            "orientation": [o.value for o in TileOrientation],
        }[name]

    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        # TileType -> str
        if name == "type" and isinstance(value, TileType):
            value = value.value
        # TileOrientation -> str
        if name == "orientation" and isinstance(value, TileOrientation):
            value = value.value
        # ---
        super(Tile, self)._set_property(name, types, value)

    def _get_property(self, name: FieldPath) -> Any:
        value = super(Tile, self)._get_property(name)
        # str -> TileType
        if name == "type":
            value = TileType(value)
        # str -> TileOrientation
        if name == "orientation":
            value = TileOrientation(value)
        # ---
        return value

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
    def type(self, value: Union[str, TileType]):
        self._set_property("type", str, value)

    @orientation.setter
    def orientation(self, value: Union[str, TileOrientation]):
        self._set_property("orientation", str, value)
