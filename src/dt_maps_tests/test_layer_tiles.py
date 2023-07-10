from dt_maps import Map
from dt_maps.types.tiles import TileType

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/loop")
    return Map.from_disk("loop", map_dir)


def test_tiles_num_tiles():
    m = _load_map()
    assert len(m.layers.tiles) == 9


def test_tiles_map_0_tile_0_1():
    m = _load_map()
    tile = "map_0/tile_0_1"
    assert m.layers.tiles[tile].i == 0
    assert m.layers.tiles[tile].j == 1
    assert m.layers.tiles[tile].type == TileType.STRAIGHT


def test_tiles_set():
    m = _load_map()
    tile = "map_0/tile_0_1"
    test_tiles_map_0_tile_0_1()
    m.layers.tiles[tile].i = 2
    m.layers.tiles[tile].j = 3
    m.layers.tiles[tile].type = TileType.CURVE
    try:
        test_tiles_map_0_tile_0_1()
        assert False
    except AssertionError:
        pass
    assert m.layers.tiles[tile].i == 2
    assert m.layers.tiles[tile].j == 3
    assert m.layers.tiles[tile].type == TileType.CURVE


def test_tiles_set_setitem():
    m = _load_map()
    tile = "map_0/tile_0_1"
    test_tiles_map_0_tile_0_1()
    m.layers.tiles[tile]["type"] = TileType.CURVE
    try:
        test_tiles_map_0_tile_0_1()
        assert False
    except AssertionError:
        pass
    assert m.layers.tiles[tile]["type"] == TileType.CURVE


def test_tiles_set_raw():
    m = _load_map()
    tile = "map_0/tile_0_1"
    test_tiles_map_0_tile_0_1()
    m.layers.tiles[tile].type = "curve"
    try:
        test_tiles_map_0_tile_0_1()
        assert False
    except AssertionError:
        pass
    assert m.layers.tiles[tile].type == TileType.CURVE


def test_tiles_set_setitem_raw():
    m = _load_map()
    tile = "map_0/tile_0_1"
    test_tiles_map_0_tile_0_1()
    m.layers.tiles[tile]["type"] = "floor"
    try:
        test_tiles_map_0_tile_0_1()
        assert False
    except AssertionError:
        pass
    assert m.layers.tiles[tile]["type"] == TileType.FLOOR


def test_tiles_set_wrong_raw():
    m = _load_map()
    tile = "map_0/tile_0_1"
    try:
        m.layers.tiles[tile].type = "wrong"
        assert False
    except ValueError:
        pass
    assert m.layers.tiles[tile].type == TileType.STRAIGHT


def test_tiles_set_wrong_setitem_raw():
    m = _load_map()
    tile = "map_0/tile_0_1"
    try:
        m.layers.tiles[tile]["type"] = "wrong"
        assert False
    except ValueError:
        pass
    assert m.layers.tiles[tile]["type"] == TileType.STRAIGHT
