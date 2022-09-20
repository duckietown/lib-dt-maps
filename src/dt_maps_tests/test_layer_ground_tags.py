from dt_maps import Map
from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/minimal_autolab")
    return Map.from_disk("minimal_autolab", map_dir)


def test_ground_tags_num_ground_tags():
    m = _load_map()
    assert len(m.layers.ground_tags) == 3


def test_ground_tags_ground_tag1():
    m = _load_map()
    ground_tag = "map_0/tag1"
    assert m.layers.ground_tags[ground_tag].size == 0.1
    assert m.layers.ground_tags[ground_tag].id == 1
    assert m.layers.ground_tags[ground_tag].family == "36h11"


def test_ground_tags_set_raw():
    m = _load_map()
    ground_tag = "map_0/tag1"
    m.layers.ground_tags[ground_tag].size = 0.15
    m.layers.ground_tags[ground_tag].id = 2
    m.layers.ground_tags[ground_tag].family = "36h12"
    try:
        test_ground_tags_ground_tag1()
        assert False
    except AssertionError:
        pass
    assert m.layers.ground_tags[ground_tag].size == 0.15
    assert m.layers.ground_tags[ground_tag].id == 2
    assert m.layers.ground_tags[ground_tag].family == "36h12"


def test_ground_tags_set_wrong_raw_size():
    m = _load_map()
    ground_tag = "map_0/tag1"
    try:
        m.layers.ground_tags[ground_tag].size = "wrong"
        assert False
    except ValueError:
        pass


def test_ground_tags_set_wrong_raw_id():
    m = _load_map()
    ground_tag = "map_0/tag1"
    try:
        m.layers.ground_tags[ground_tag].id = "wrong"
        assert False
    except ValueError:
        pass


def test_ground_tags_set_wrong_raw_family():
    m = _load_map()
    ground_tag = "map_0/tag1"
    try:
        m.layers.ground_tags[ground_tag].family = 1
        assert False
    except ValueError:
        pass


def test_ground_tags_set_setitem_raw():
    m = _load_map()
    ground_tag = "map_0/tag1"
    m.layers.ground_tags[ground_tag]["size"] = 0.15
    m.layers.ground_tags[ground_tag]["id"] = 2
    m.layers.ground_tags[ground_tag]["family"] = "36h12"
    try:
        test_ground_tags_ground_tag1()
        assert False
    except AssertionError:
        pass
    assert m.layers.ground_tags[ground_tag]["size"] == 0.15
    assert m.layers.ground_tags[ground_tag]["id"] == 2
    assert m.layers.ground_tags[ground_tag]["family"] == "36h12"


def test_ground_tags_set_wrong_setitem_raw_size():
    m = _load_map()
    ground_tag = "map_0/tag1"
    try:
        m.layers.ground_tags[ground_tag]["size"] = "wrong"
        assert False
    except ValueError:
        pass


def test_ground_tags_set_wrong_setitem_raw_id():
    m = _load_map()
    ground_tag = "map_0/tag1"
    try:
        m.layers.ground_tags[ground_tag]["id"] = "wrong"
        assert False
    except ValueError:
        pass


def test_ground_tags_set_wrong_setitem_raw_family():
    m = _load_map()
    ground_tag = "map_0/tag1"
    try:
        m.layers.ground_tags[ground_tag]["family"] = 1
        assert False
    except ValueError:
        pass


def test_ground_tags_frames():
    m = _load_map()
    ground_tag1 = "map_0/tag1"
    ground_tag2 = ground_tag1 + "/tag2"
    assert m.layers.ground_tags[ground_tag1].frame.relative_to == "map_0"
    assert m.layers.ground_tags[ground_tag2].frame.relative_to == ground_tag1
