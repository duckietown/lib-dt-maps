import os
from abc import abstractmethod, ABC

from types import SimpleNamespace
from typing import TextIO, Iterator, Tuple, Union, Generic, TypeVar, Dict, _KT, Optional, _VT_co

from dt_maps.exceptions import EntityNotFound

Tile = dict
TileCoordinates = Tuple[int, int]
TileMap = dict


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


class MapEntity(dict, ABC):

    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> 'MapEntity':
        pass


MapEntityType = TypeVar("MapEntityType", bound=MapEntity)


class MapLayer(dict, Generic[MapEntityType], Dict[str, MapEntityType]):
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

    def __init__(self, name: str, *args, **kwargs):
        self._name: str = name
        self._cache: Dict[str, MapEntityType] = {}
        super(MapLayer, self).__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> MapEntityType:
        # check cached
        if key in self._cache:
            return self._cache[key]
        # get item from underlying dictionary
        try:
            item: dict = super(MapLayer, self).__getitem__(key)
        except KeyError:
            raise EntityNotFound(self._name, key=key)
        # turn 'dict' into 'T'
        wrapped = MapEntityType.from_dict(**item)
        # cache and return
        self._cache[key] = wrapped
        return wrapped

    def get(self, key: str) -> Optional[MapEntityType]:
        #TODO: this should do something similar to above
        return self.__getitem__(key, *args, **kwargs)

    def as_raw_dict(self):
        """
        Raw representation of the map layer as a Python dictionary.

        Return:
            :obj:`dict`     raw dictionary representing the layer
        """
        return dict(self)


class MapLayerNamespace(SimpleNamespace):

    def has(self, name: str) -> bool:
        return self.__dict__.get(name, None) is not None

    def items(self) -> Iterator[Tuple[str, MapLayer]]:
        return iter([(k, v) for k, v in self.__dict__.items()])

    # known layers ==>

    @property
    def frames(self) -> MapLayer[str]:
        return self.__getitem__("frames")

    # known layers <==

    def __getitem__(self, layer: str) -> MapLayer:
        if layer in self.__dict__:
            return self.__dict__[layer]
        raise KeyError(f"Map has no layer '{layer}'")

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__.keys())

    def __len__(self) -> int:
        return len(self.__dict__)
