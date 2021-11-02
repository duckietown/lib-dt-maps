from dt_maps import Map

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/loop")
    return Map.from_disk("loop", map_dir)


def test_tile_maps_num_tile_maps():
    m = _load_map()
    assert len(m.layers.tile_maps) == 1


def test_tile_maps_tile_map_map_0():
    m = _load_map()
    tile_map = "map_0"
    assert m.layers.tile_maps[tile_map].tile_size.x == 0.585
    assert m.layers.tile_maps[tile_map].tile_size.y == 0.585


def test_tile_maps_tile_map_set():
    m = _load_map()
    tile_map = "map_0"
    test_tile_maps_tile_map_map_0()
    m.layers.tile_maps[tile_map].tile_size.x = 0.6
    m.layers.tile_maps[tile_map].tile_size.y = 0.4
    try:
        test_tile_maps_tile_map_map_0()
        assert m.layers.tile_maps[tile_map].tile_size.x == 0.6
        assert m.layers.tile_maps[tile_map].tile_size.y == 0.4
    except AssertionError:
        pass
    assert m.layers.tile_maps[tile_map].tile_size.x == 0.6
    assert m.layers.tile_maps[tile_map].tile_size.y == 0.4


def test_tile_maps_tile_map_set_setitem():
    m = _load_map()
    tile_map = "map_0"
    test_tile_maps_tile_map_map_0()
    m.layers.tile_maps[tile_map]["tile_size"]["x"] = 0.6
    m.layers.tile_maps[tile_map]["tile_size"]["y"] = 0.4
    try:
        test_tile_maps_tile_map_map_0()
        assert m.layers.tile_maps[tile_map]["tile_size"]["x"] == 0.6
        assert m.layers.tile_maps[tile_map]["tile_size"]["y"] == 0.4
    except AssertionError:
        pass
    assert m.layers.tile_maps[tile_map]["tile_size"]["x"] == 0.6
    assert m.layers.tile_maps[tile_map]["tile_size"]["y"] == 0.4



