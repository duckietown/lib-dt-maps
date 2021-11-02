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
    assert m.layers.frames["map_0"].pose.x == 0.0
