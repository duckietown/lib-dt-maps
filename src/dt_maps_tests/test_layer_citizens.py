from dt_maps import Map
from dt_maps.types.citizens import CitizenType

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/minimal_autolab")
    return Map.from_disk("minimal_autolab", map_dir)


def test_citizens_num_citizens():
    m = _load_map()
    assert len(m.layers.citizens) == 3


def test_citizens_citizen1():
    m = _load_map()
    citizen = "map_0/duckie1"
    assert m.layers.citizens[citizen].color == CitizenType.YELLOW
    # TODO: id is optional, but we catch exception: `layer 'citizens' does not have field 'id'`...
    # assert m.layers.citizens[citizen].id is None


def test_citizens_set_raw():
    m = _load_map()
    citizen = "map_0/duckie1"
    m.layers.citizens[citizen].color = "red"
    try:
        test_citizens_citizen1()
        assert False
    except AssertionError:
        pass
    assert m.layers.citizens[citizen].color == CitizenType.RED


def test_citizens_set_wrong_raw():
    m = _load_map()
    citizen = "map_0/duckie1"
    try:
        m.layers.citizens[citizen].color = "wrong"
        assert False
    except ValueError:
        pass


def test_citizens_set_setitem_raw():
    m = _load_map()
    citizen = "map_0/duckie1"
    m.layers.citizens[citizen]["color"] = CitizenType.GREEN
    try:
        test_citizens_citizen1()
        assert False
    except AssertionError:
        pass
    assert m.layers.citizens[citizen]["color"] == CitizenType.GREEN


def test_citizens_set_wrong_setitem_raw():
    m = _load_map()
    citizen = "map_0/duckie1"
    try:
        m.layers.citizens[citizen]["color"] = "wrong"
        assert False
    except ValueError:
        pass


def test_citizens_frames():
    m = _load_map()
    citizen1 = "map_0/duckie1"
    citizen2 = citizen1 + "/duckie2"
    assert m.layers.citizens[citizen1].frame.relative_to == "map_0"
    assert m.layers.citizens[citizen2].frame.relative_to == citizen1
