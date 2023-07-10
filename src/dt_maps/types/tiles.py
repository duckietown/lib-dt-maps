from enum import Enum
from typing import Tuple, Union, Iterable, Any, Optional

from dt_maps.types.commons import EntityHelper, FieldPath
from dt_maps.types.frames import Frame
from dt_maps.types.tile_maps import TileMap

TileCoordinates = Tuple[int, int]


class TileType(Enum):
    STRAIGHT = "straight"
    CURVE = "curve"
    ASPHALT = "asphalt"
    FLOOR = "floor"
    GRASS = "grass"
    THREE_WAY = "3way"
    FOUR_WAY = "4way"


class Tile(EntityHelper):
    LAYER_NAME: str = "tiles"

    def _get_layer_name(self) -> str:
        return self.LAYER_NAME

    def __init__(self, map, layer: str, key: str, *_, **__):
        super(Tile, self).__init__(map=map, layer=layer, key=key, *_, **__)
        self._tile_map: Optional[TileMap] = None

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            "type": str
        }[name]

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            "type": [t.value for t in TileType]
        }[name]

    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        # TileType -> str
        if name == "type" and isinstance(value, TileType):
            value = value.value
        # TileOrientation -> str
        super(Tile, self)._set_property(name, types, value)

    def _get_property(self, name: FieldPath) -> Any:
        value = super(Tile, self)._get_property(name)
        # str -> TileType
        if name == "type":
            value = TileType(value)
        return value

    @property
    def frame(self) -> Frame:
        return Frame.create(self._map, "frames", self._key)

    @property
    def tile_map(self) -> TileMap:
        # return one if we have it cached already
        if self._tile_map is None:
            # no tile_map found yet, let's lazy init
            tile_map_key: str = "/".join(self.key.split("/")[:-1])
            tile_map: TileMap = self._map.layers.tile_maps.get(tile_map_key)
            self._tile_map = tile_map
        # ---
        return self._tile_map

    @property
    def i(self) -> int:
        ts: float = self.tile_map.tile_size.x
        return int(round((self.frame.pose.x / ts) - 0.5))

    @i.setter
    def i(self, value: int):
        ts: float = self.tile_map.tile_size.x
        self.frame.pose.x = (value + 0.5) * ts

    @property
    def j(self) -> int:
        ts: float = self.tile_map.tile_size.y
        return int(round((self.frame.pose.y / ts) - 0.5))

    @j.setter
    def j(self, value: int):
        ts: float = self.tile_map.tile_size.y
        self.frame.pose.y = (value + 0.5) * ts

    @property
    def type(self) -> TileType:
        return TileType(self._get_property("type"))

    @type.setter
    def type(self, value: Union[str, TileType]):
        self._set_property("type", str, value)

    def __contains__(self, key):
        return super(Tile, self).__contains__(key) or key in ["i", "j"]

    def __getitem__(self, key: str):
        if key == "i":
            return self.i
        if key == "j":
            return self.j
        # ---
        return super(Tile, self).__getitem__(key)

    def __setitem__(self, key: str, value: Any):
        if key == "i":
            self.i = value
        if key == "j":
            self.j = value
        # ---
        super(Tile, self).__setitem__(key, value)
