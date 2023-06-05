from dt_maps import Map
from dt_maps.types.vehicles import VehicleType, ColorType

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/minimal_autolab")
    return Map.from_disk("minimal_autolab", map_dir)


def test_vehicles_num_vehicles():
    m = _load_map()
    assert len(m.layers.vehicles) == 3


def test_vehicles_vehicle1():
    m = _load_map()
    vehicle = "map_0/duckiebot1"
    assert m.layers.vehicles[vehicle].configuration == VehicleType.DB18
    assert m.layers.vehicles[vehicle].color == ColorType.GREEN
    # TODO: id is optional, but we catch exception: `layer 'vehicles' does not have field 'id'`...
    # assert m.layers.vehicles[vehicle].id is None


def test_vehicles_set_raw():
    m = _load_map()
    vehicle = "map_0/duckiebot1"
    m.layers.vehicles[vehicle].configuration = "DB19"
    m.layers.vehicles[vehicle].color = "red"
    try:
        test_vehicles_vehicle1()
        assert False
    except AssertionError:
        pass
    assert m.layers.vehicles[vehicle].configuration == VehicleType.DB19
    assert m.layers.vehicles[vehicle].color == ColorType.RED


def test_vehicles_set_wrong_raw_configuration():
    m = _load_map()
    vehicle = "map_0/duckiebot1"
    try:
        m.layers.vehicles[vehicle].configuration = "wrong"
        assert False
    except ValueError:
        pass


def test_vehicles_set_wrong_raw_color():
    m = _load_map()
    vehicle = "map_0/duckiebot1"
    try:
        m.layers.vehicles[vehicle].color = "wrong"
        assert False
    except ValueError:
        pass


def test_vehicles_set_setitem_raw():
    m = _load_map()
    vehicle = "map_0/duckiebot1"
    m.layers.vehicles[vehicle]["configuration"] = VehicleType.DB19
    m.layers.vehicles[vehicle]["color"] = ColorType.RED
    try:
        test_vehicles_vehicle1()
        assert False
    except AssertionError:
        pass
    assert m.layers.vehicles[vehicle]["configuration"] == VehicleType.DB19
    assert m.layers.vehicles[vehicle]["color"] == ColorType.RED


def test_vehicles_set_wrong_setitem_raw_configuration():
    m = _load_map()
    vehicle = "map_0/duckiebot1"
    try:
        m.layers.vehicles[vehicle]["configuration"] = "wrong"
        assert False
    except ValueError:
        pass


def test_vehicles_set_wrong_setitem_raw_color():
    m = _load_map()
    vehicle = "map_0/duckiebot1"
    try:
        m.layers.vehicles[vehicle]["color"] = "wrong"
        assert False
    except ValueError:
        pass


def test_vehicles_frames():
    m = _load_map()
    vehicle1 = "map_0/duckiebot1"
    vehicle2 = vehicle1 + "/duckiebot2"
    assert m.layers.vehicles[vehicle1].frame.relative_to == "map_0"
    assert m.layers.vehicles[vehicle2].frame.relative_to == vehicle1
