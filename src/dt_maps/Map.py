import os
import glob
import logging

from pathlib import Path
from types import SimpleNamespace
from typing import Any, TextIO, Iterator, Tuple

import yaml

logging.basicConfig()


class MapAsset:

    def __init__(self, fpath: str):
        self._fpath = fpath

    @property
    def fpath(self) -> str:
        return self._fpath

    def exists(self) -> bool:
        return os.path.isfile(self._fpath)

    def read(self, mode: str):
        with open(self._fpath, mode) as fin:
            return fin.read()

    def write(self, mode: str, data: Any):
        self._make_dirs()
        with open(self._fpath, mode) as fout:
            return fout.write(data)

    def open(self, mode: str) -> TextIO:
        self._make_dirs()
        return open(self._fpath, mode)

    def _make_dirs(self):
        os.makedirs(os.path.dirname(self._fpath), exist_ok=True)


class MapLayer(dict):

    def __init__(self, *args, **kwargs):
        super(MapLayer, self).__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> dict:
        try:
            return super(MapLayer, self).__getitem__(key)
        except KeyError:
            d = dict()
            self[key] = d
            return d

    def as_raw_dict(self):
        return dict(self)


class MapLayerNamespace(SimpleNamespace):

    def __getitem__(self, layer: str) -> MapLayer:
        if layer in self.__dict__:
            return self.__dict__[layer]
        raise KeyError(f"Map has no layer '{layer}'")

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__.keys())

    def has(self, name: str) -> bool:
        return self.__dict__.get(name, None) is not None

    def items(self) -> Iterator[Tuple[str, MapLayer]]:
        return iter([(k, v) for k, v in self.__dict__.items()])


class Map:
    """
    Provides an interface to a Duckietown Map.

    Use the constructor only if you want to create a new map.
    If you want to load a map from disk, use the function
    :py:meth:`dt_maps.Map.from_disk` instead.

    Layers are loaded from the YAML files and stored inside the `.layers` property.
    For example, a map stored in the directory `./my-map/` with layer files `frames.yaml` and
    `tile_maps.yaml` can be loaded and used using the following,

    .. code-block:: python

        from dt_maps import Map

        map = Map.from_disk("my-map", "./my-map/")
        print(map.layers.frames)
        print(map.layers.tile_maps)


    Args:
        name (:obj:`str`): name of the new map
        path (:obj:`str`): path where the map will be stored
    """

    def __init__(self, name: str, path: str, loglevel: int = logging.INFO):
        self.name = name
        self._path = path
        self._assets_dir = os.path.join(self._path, "assets")
        self._logger = logging.getLogger(f"Map[{name}]")
        self._logger.setLevel(loglevel)
        self.layers = MapLayerNamespace()

    @property
    def assets_dir(self) -> str:
        """
        Path to the map's assets directory.
        """
        return self._assets_dir

    def asset(self, key: str, name: str) -> MapAsset:
        asset_fpath = os.path.join(self._assets_dir, key, name)
        return MapAsset(asset_fpath)

    def to_disk(self):
        # dump layers
        for name, layer in self.layers.items():
            fpath = os.path.join(self._path, f"{name}.yaml")
            with open(fpath, "wt") as fout:
                yaml.safe_dump({name: layer.as_raw_dict()}, fout)

    @classmethod
    def from_disk(cls, name: str, maps_dir: str) -> 'Map':
        """
        Loads a map from disk.

        Args:
            name (:obj:`str`):      name of the loaded map
            maps_dir (:obj:`str`):  path to the directory containing the map to load

        Returns:
            :obj:`dt_maps.Map`:   the loaded map

        """
        map_dir = os.path.join(maps_dir, name)
        # make sure the map exists on disk
        if not os.path.isdir(map_dir):
            raise NotADirectoryError(f"The path '{map_dir}' is not a directory.")
        # build empty map
        _map = Map(name, map_dir)
        # find layers
        layer_pattern = os.path.join(map_dir, "*.yaml")
        layer_fpaths = glob.glob(layer_pattern)
        # load layers
        for layer_fpath in layer_fpaths:
            layer_name = str(Path(layer_fpath).name)
            with open(layer_fpath, "rt") as fin:
                try:
                    layer_content = yaml.safe_load(fin)[layer_name]
                except KeyError:
                    raise RuntimeError(f"The layer file '{layer_fpath}' does not have "
                                       f"'{layer_name}' as key to the root object.")
                # turn raw dict into a MapLayer object
                layer = MapLayer(layer_content)
                # populate map
                _map.layers.__dict__[layer_name] = layer
        # ---
        return _map
