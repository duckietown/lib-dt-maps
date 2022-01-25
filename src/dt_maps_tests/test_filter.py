from dt_maps import Map
from dt_maps.types.watchtowers import WatchtowerType

from . import get_asset_path


def _load_map_loop() -> Map:
    map_dir = get_asset_path("maps/loop")
    return Map.from_disk("loop", map_dir)


def _load_map_minimal_autolab() -> Map:
    map_dir = get_asset_path("maps/minimal_autolab")
    return Map.from_disk("minimal_autolab", map_dir)


def test_tiles_num_tiles_i():
    m = _load_map_loop()
    tiles_without_parent = m.layers.tiles.filter(i=0)
    tiles_parent = m.layers.tiles.filter("map_0/", i=0)
    assert len(tiles_without_parent) == 3
    assert len(tiles_parent) == len(tiles_without_parent)


def test_tiles_num_tiles_i_j():
    m = _load_map_loop()
    tiles_without_parent = m.layers.tiles.filter(i=0, j=1)
    tiles_parent = m.layers.tiles.filter("map_0/", i=0, j=1)
    assert len(tiles_without_parent) == 1
    assert len(tiles_parent) == len(tiles_without_parent)


def test_watchtower_configuration():
    m = _load_map_minimal_autolab()
    all_watchtowers = m.layers.watchtowers.filter(configuration=WatchtowerType.WT18)
    assert len(all_watchtowers) == 2

