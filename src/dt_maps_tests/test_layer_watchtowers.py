from dt_maps import Map
from dt_maps.types.watchtowers import WatchtowerType

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/minimal_autolab")
    return Map.from_disk("minimal_autolab", map_dir)


def test_watchtowers_num_watchtowers():
    m = _load_map()
    assert len(m.layers.watchtowers) == 2


def test_watchtowers_watchtower1():
    m = _load_map()
    watchtower = "map_1/watchtower1"
    assert m.layers.watchtowers[watchtower].configuration == WatchtowerType.WT18
    # TODO: id is optional, but we catch exception: `layer 'watchtowers' does not have field 'id'`...
    # assert m.layers.watchtowers[watchtower].id is None


def test_watchtowers_set_raw():
    m = _load_map()
    watchtower = "map_1/watchtower1"
    m.layers.watchtowers[watchtower].configuration = "WT19"
    try:
        test_watchtowers_watchtower1()
        assert False
    except AssertionError:
        pass
    assert m.layers.watchtowers[watchtower].configuration == WatchtowerType.WT19
