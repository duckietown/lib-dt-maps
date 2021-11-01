from typing import Optional

from dt_maps import Map
from dt_maps.types import Tile


def get_tile(m: Map, i: int, j: int) -> Optional[Tile]:
    for t in m.layers.tiles.values():
        if t["i"] == i and t["j"] == j:
            return t
    return None
