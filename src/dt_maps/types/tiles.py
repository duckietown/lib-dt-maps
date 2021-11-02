import os
from abc import abstractmethod, ABC

from types import SimpleNamespace
from typing import TextIO, Iterator, Tuple, Union, Generic, TypeVar, Dict, Optional, Any

from dt_maps import Map
from dt_maps.exceptions import EntityNotFound

TileCoordinates = Tuple[int, int]
TileMap = dict


class Tile:

    def __init__(self, m: Map, tile_key: str):
        self._key = tile_key

    @property
    def frame(self):