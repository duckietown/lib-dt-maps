import os

from dt_maps import Map


def get_test_assets_dir_():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = os.path.join(script_dir, "..", "..", "tests")
    return os.path.abspath(assets_dir)


def get_asset_path_(asset: str) -> str:
    return os.path.abspath(os.path.join(get_test_assets_dir_(), asset))


def _load_map() -> Map:
    map_dir = get_asset_path_("maps/minimal_autolab")
    return Map.from_disk("loop", map_dir)


if __name__ == '__main__':
    m = _load_map()
    for wt in m.layers.tiles.values():
        # create
        print(wt["id"])
        print(wt)
