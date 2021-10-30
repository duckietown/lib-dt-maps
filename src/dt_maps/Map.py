import os
import glob
import logging

from pathlib import Path
from types import SimpleNamespace
from typing import TextIO, Iterator, Tuple, Union

import yaml

logging.basicConfig()


class MapAsset:
    """
    Class representing a map asset.

    Args:
        fpath (:obj:`str`):     path to the asset
    """

    def __init__(self, fpath: str):
        self._fpath = fpath

    @property
    def fpath(self) -> str:
        """
        File path to the asset
        """
        return self._fpath

    def exists(self) -> bool:
        """
        Whether the asset exists on disk
        """
        return os.path.isfile(self._fpath)

    def read(self, mode: str) -> Union[str, bytes]:
        """
        Read the asset file content from disk.

        Args:
            mode (:obj:`str`):     reading mode as in :py:meth:`open`

        Returns:
            :obj:`str,bytes`:      asset file content
        """
        with open(self._fpath, mode) as fin:
            return fin.read()

    def write(self, mode: str, data: Union[str, bytes]):
        """
        Writes the content of ``data`` to the asset file on disk.

        Args:
            mode (:obj:`str`):          write mode as in :py:meth:`open`
            data (:obj:`str,bytes`):    asset content to write to disk
        """
        self._make_dirs()
        with open(self._fpath, mode) as fout:
            return fout.write(data)

    def open(self, mode: str) -> TextIO:
        """
        Wrapper around :py:meth:`open` used to open the file.

        Args:
            mode (:obj:`str`):   mode as in :py:meth:`open`
        """
        self._make_dirs()
        return open(self._fpath, mode)

    def _make_dirs(self):
        """
        Make directories up to the asset location.
        """
        os.makedirs(os.path.dirname(self._fpath), exist_ok=True)


class MapLayer(dict):
    """
    Class representing a map layer.
    It is a subclass of :py:class:`dict`.

    A layer ``X`` accessed on a map ``map`` using the
    syntax ``map.layers.X`` is an object instance of this class.

    Use the ``[]`` operator to access a layer, the same way you would access
    a dictionary. For example, the frame with key ``frame_0`` can be accessed
    using the following code,

    .. code-block:: python

        map.layers.frames["frame_0"]
    """

    def __init__(self, *args, **kwargs):
        super(MapLayer, self).__init__(*args, **kwargs)

    def as_raw_dict(self):
        """
        Raw representation of the map layer as a Python dictionary.

        Return:
            :obj:`dict`     raw dictionary representing the layer
        """
        return dict(self)


class MapLayerNamespace(SimpleNamespace):

    def __getitem__(self, layer: str) -> MapLayer:
        if layer in self.__dict__:
            return self.__dict__[layer]
        raise KeyError(f"Map has no layer '{layer}'")

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__.keys())

    def __len__(self) -> int:
        return len(self.__dict__)

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
        self._name: str = name
        self._path = path
        self._assets_dir = os.path.join(self._path, "assets")
        self._logger = logging.getLogger(f"Map[{name}]")
        self._logger.setLevel(loglevel)
        self._layers: MapLayerNamespace = MapLayerNamespace()

    @property
    def name(self) -> str:
        """
        Name of the map.
        """
        return self._name

    @property
    def layers(self) -> MapLayerNamespace:
        """
        Map layers.
        """
        return self._layers

    @property
    def assets_dir(self) -> str:
        """
        Path to the map's assets directory.
        """
        return self._assets_dir

    def asset(self, key: str) -> MapAsset:
        """
        Creates a MapAsset object representing the asset with ``key``.

        Args:
            key (:obj:`str`)    key of the asset

        Return:
            :obj:`dt_maps.MapAsset`     asset object
        """
        asset_fpath = os.path.join(self._assets_dir, key)
        return MapAsset(asset_fpath)

    def to_disk(self):
        """
        Save map to disk.
        """
        # dump layers
        for name, layer in self.layers.items():
            fpath = os.path.join(self._path, f"{name}.yaml")
            with open(fpath, "wt") as fout:
                yaml.safe_dump({name: layer.as_raw_dict()}, fout)

    @classmethod
    def from_disk(cls, name: str, map_dir: str) -> 'Map':
        """
        Loads a map from disk.

        Args:
            name (:obj:`str`):      name of the loaded map
            map_dir (:obj:`str`):   path to the directory containing the map to load

        Returns:
            :obj:`dt_maps.Map`:   the loaded map
        """
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
            layer_name = str(Path(layer_fpath).stem)
            if layer_name == "main":
                continue
            with open(layer_fpath, "rt") as fin:
                try:
                    layer_content = yaml.safe_load(fin)[layer_name]
                except KeyError:
                    raise RuntimeError(f"The layer file '{layer_fpath}' does not have "
                                       f"'{layer_name}' as key to the root object.")
                # turn raw dict into a MapLayer object
                layer = MapLayer(layer_content)
                # populate map
                _map._layers.__dict__[layer_name] = layer
        # ---
        return _map
