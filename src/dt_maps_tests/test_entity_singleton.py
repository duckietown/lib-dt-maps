from dt_maps import Map
from dt_maps.types.frames import Frame
from dt_maps.types.tiles import Tile

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/loop")
    return Map.from_disk("loop", map_dir)


def test_singleton_multi_create_1():
    m = _load_map()
    f1: Frame = Frame.create(m, "frames", "map_0/tile_0_0")
    f2: Frame = Frame.create(m, "frames", "map_0/tile_0_0")
    assert id(f1) == id(f2)


def test_singleton_multi_create_2():
    m = _load_map()
    t1: Tile = Tile.create(m, "tiles", "map_0/tile_0_0")
    t2: Tile = Tile.create(m, "tiles", "map_0/tile_0_0")
    assert id(t1) == id(t2)


def test_singleton_different_layers_same_key_1():
    m = _load_map()
    f1: Frame = Frame.create(m, "frames", "map_0/tile_0_0")
    t2: Tile = Tile.create(m, "tiles", "map_0/tile_0_0")
    assert id(f1) != id(t2)
