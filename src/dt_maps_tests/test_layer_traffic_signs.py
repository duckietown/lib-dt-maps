from dt_maps import Map
from dt_maps.types.traffic_signs import TrafficSignType

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/minimal_autolab")
    return Map.from_disk("minimal_autolab", map_dir)


def test_traffic_signs_num_traffic_signs():
    m = _load_map()
    assert len(m.layers.traffic_signs) == 3


def test_traffic_signs_traffic_sign1():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    assert m.layers.traffic_signs[traffic_sign].type == TrafficSignType.STOP
    assert m.layers.traffic_signs[traffic_sign].id == 1
    assert m.layers.traffic_signs[traffic_sign].family == "36h11"


def test_traffic_signs_set_raw():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    m.layers.traffic_signs[traffic_sign].type = "yield"
    m.layers.traffic_signs[traffic_sign].id = 2
    m.layers.traffic_signs[traffic_sign].family = "36h12"
    try:
        test_traffic_signs_traffic_sign1()
        assert False
    except AssertionError:
        pass
    assert m.layers.traffic_signs[traffic_sign].type == TrafficSignType.YIELD
    assert m.layers.traffic_signs[traffic_sign].id == 2
    assert m.layers.traffic_signs[traffic_sign].family == "36h12"


def test_traffic_signs_set_wrong_raw_type():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    try:
        m.layers.traffic_signs[traffic_sign].type = "wrong"
        assert False
    except ValueError:
        pass


def test_traffic_signs_set_wrong_raw_id():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    try:
        m.layers.traffic_signs[traffic_sign].id = "wrong"
        assert False
    except ValueError:
        pass


def test_traffic_signs_set_wrong_raw_family():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    try:
        m.layers.traffic_signs[traffic_sign].family = 1
        assert False
    except ValueError:
        pass


def test_traffic_signs_set_setitem_raw():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    m.layers.traffic_signs[traffic_sign]["type"] = TrafficSignType.YIELD
    m.layers.traffic_signs[traffic_sign]["id"] = 2
    m.layers.traffic_signs[traffic_sign]["family"] = "36h12"
    try:
        test_traffic_signs_traffic_sign1()
        assert False
    except AssertionError:
        pass
    assert m.layers.traffic_signs[traffic_sign]["type"] == TrafficSignType.YIELD
    assert m.layers.traffic_signs[traffic_sign]["id"] == 2
    assert m.layers.traffic_signs[traffic_sign]["family"] == "36h12"


def test_traffic_signs_set_wrong_setitem_raw_type():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    try:
        m.layers.traffic_signs[traffic_sign]["type"] = "wrong"
        assert False
    except ValueError:
        pass


def test_traffic_signs_set_wrong_setitem_raw_id():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    try:
        m.layers.traffic_signs[traffic_sign]["id"] = "wrong"
        assert False
    except ValueError:
        pass


def test_traffic_signs_set_wrong_setitem_raw_family():
    m = _load_map()
    traffic_sign = "map_0/sign1"
    try:
        m.layers.traffic_signs[traffic_sign]["family"] = 1
        assert False
    except ValueError:
        pass


def test_traffic_signs_frames():
    m = _load_map()
    traffic_sign1 = "map_0/sign1"
    traffic_sign2 = traffic_sign1 + "/sign2"
    assert m.layers.traffic_signs[traffic_sign1].frame.relative_to == "map_0"
    assert m.layers.traffic_signs[traffic_sign2].frame.relative_to == traffic_sign1
