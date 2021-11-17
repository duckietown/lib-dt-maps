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
    watchtower = "map_0/watchtower1"
    assert m.layers.watchtowers[watchtower].configuration == WatchtowerType.WT18
    assert m.layers.watchtowers[watchtower].id is None


def test_watchtowers_set_raw():
    m = _load_map()
    watchtower = "map_0/watchtower1"
    m.layers.watchtowers[watchtower].configuration = "WT19"
    try:
        test_watchtowers_watchtower1()
        assert False
    except AssertionError:
        pass
    assert m.layers.watchtowers[watchtower].configuration == WatchtowerType.WT19


def test_watchtowers_set_wrong_raw():
    m = _load_map()
    watchtower = "map_0/watchtower1"
    try:
        m.layers.watchtowers[watchtower].configuration = "wrong"
        assert False
    except ValueError:
        pass


def test_watchtowers_set_setitem_raw():
    m = _load_map()
    watchtower = "map_0/watchtower1"
    m.layers.watchtowers[watchtower]["configuration"] = WatchtowerType.WT19
    try:
        test_watchtowers_watchtower1()
        assert False
    except AssertionError:
        pass
    assert m.layers.watchtowers[watchtower]["configuration"] == WatchtowerType.WT19


def test_watchtowers_set_wrong_setitem_raw():
    m = _load_map()
    watchtower = "map_0/watchtower1"
    try:
        m.layers.watchtowers[watchtower]["configuration"] = "wrong"
        assert False
    except ValueError:
        pass


def test_watchtowers_frames():
    m = _load_map()
    watchtower1 = "map_0/watchtower1"
    watchtower2 = watchtower1 + "/watchtower2"
    assert m.layers.watchtowers[watchtower1].frame.relative_to == "map_0"
    assert m.layers.watchtowers[watchtower2].frame.relative_to == watchtower1


def test_watchtowers_watchtowers_id():
    m = _load_map()
    watchtower1 = "map_0/watchtower1"
    watchtower2 = watchtower1 + "/watchtower2"
    assert m.layers.watchtowers[watchtower1].id is None
    assert m.layers.watchtowers[watchtower2].id == "test_id"
    m.layers.watchtowers[watchtower1].id = "test2"
    m.layers.watchtowers[watchtower2].id = "test_test"
    assert m.layers.watchtowers[watchtower1].id == "test2"
    assert m.layers.watchtowers[watchtower2].id == "test_test"
    m.layers.watchtowers[watchtower2].id = None
    assert m.layers.watchtowers[watchtower2].id is None
