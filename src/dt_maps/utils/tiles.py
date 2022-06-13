from typing import Optional, cast

from dt_maps import Map
from dt_maps.types.tiles import Tile, TileOrientation

TILE_ORIENTATIONS = {
    TileOrientation.E: 0,
    TileOrientation.N: 90,
    TileOrientation.W: 180,
    TileOrientation.S: 270
}


def get_tile(m: Map, i: int, j: int) -> Optional[Tile]:
    for t in m.layers.tiles.values():
        if t["i"] == i and t["j"] == j:
            return cast(Tile, t)
    return None


def orientation2deg(tile_orientation: TileOrientation) -> int:
    return TILE_ORIENTATIONS[tile_orientation]


def deg2orientation(tile_deg: int) -> Optional[TileOrientation]:
    for obj_orientation, deg in TILE_ORIENTATIONS.items():
        if tile_deg == deg:
            return obj_orientation
