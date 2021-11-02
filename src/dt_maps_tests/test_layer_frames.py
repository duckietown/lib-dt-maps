from dt_maps import Map

from . import get_asset_path


def _load_map() -> Map:
    map_dir = get_asset_path("maps/loop")
    return Map.from_disk("loop", map_dir)


def test_frames_num_frames():
    m = _load_map()
    assert len(m.layers.frames) == 10


def test_frames_frame_origin():
    m = _load_map()
    frame = "map_0"
    assert m.layers.frames[frame].pose.x == 1.0
    assert m.layers.frames[frame].pose.y == 2.0
    assert m.layers.frames[frame].pose.z == 0.0
    assert m.layers.frames[frame].pose.roll == 0.0
    assert m.layers.frames[frame].pose.pitch == 0.0
    assert m.layers.frames[frame].pose.yaw == 0.0
    assert m.layers.frames[frame].relative_to is None


def test_frames_frame_tile_0_1():
    m = _load_map()
    frame = "map_0/tile_0_1"
    assert m.layers.frames[frame].pose.x == 0.2925
    assert m.layers.frames[frame].pose.y == 0.8775
    assert m.layers.frames[frame].pose.z == 0.0
    assert m.layers.frames[frame].pose.roll == 0.0
    assert m.layers.frames[frame].pose.pitch == 0.0
    assert m.layers.frames[frame].pose.yaw == 0.0
    assert m.layers.frames[frame].relative_to == "map_0"


def test_frames_frame_set():
    m = _load_map()
    frame = "map_0/tile_0_1"
    test_frames_frame_tile_0_1()
    m.layers.frames[frame].pose.x = 1.0
    m.layers.frames[frame].relative_to = "map_99"
    try:
        test_frames_frame_tile_0_1()
        assert m.layers.frames[frame].pose.x == 1.0
        assert m.layers.frames[frame].relative_to == "map_99"
    except AssertionError:
        pass
    assert m.layers.frames[frame].pose.x == 1.0
    assert m.layers.frames[frame].relative_to == "map_99"


def test_frames_frame_set_setitem():
    m = _load_map()
    frame = "map_0/tile_0_1"
    test_frames_frame_tile_0_1()
    m.layers.frames[frame].pose["x"] = 1.0
    m.layers.frames[frame]["relative_to"] = "map_99"
    try:
        test_frames_frame_tile_0_1()
        assert m.layers.frames[frame].pose["x"] == 1.0
        assert m.layers.frames[frame]["relative_to"] == "map_99"
    except AssertionError:
        pass
    assert m.layers.frames[frame].pose["x"] == 1.0
    assert m.layers.frames[frame]["relative_to"] == "map_99"


