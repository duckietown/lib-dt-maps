from dt_maps import Map

from . import get_asset_path


def test_load_map_empty():
    map_dir = get_asset_path("maps/empty")
    m = Map.from_disk("empty", map_dir)
    assert len(m.layers) == 0


def test_load_map_minimal():
    map_dir = get_asset_path("maps/minimal")
    m = Map.from_disk("empty", map_dir)
    # 3 layers
    assert len(m.layers) == 3
    # layers are empty
    assert len(m.layers.frames) == 0
    assert len(m.layers.tile_maps) == 0
    assert len(m.layers.tiles) == 0


def test_load_map_minimal_raw():
    map_dir = get_asset_path("maps/minimal")
    m = Map.from_disk("empty", map_dir)
    # check raw dicts
    assert m.layers.frames.as_raw_dict() == {}
    assert m.layers.tile_maps.as_raw_dict() == {}
    assert m.layers.tiles.as_raw_dict() == {}


