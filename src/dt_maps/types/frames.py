from dt_maps import Map
from dt_maps.types.geometry import Pose3D


class Frame:

    def __init__(self, m: Map, key: str):
        self._map = m
        self._key = key

    @property
    def pose(self) -> Pose3D:
        return Pose3D