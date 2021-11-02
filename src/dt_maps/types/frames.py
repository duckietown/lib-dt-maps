from typing import Optional

from dt_maps import Map
from dt_maps.types.commons import EntityHelper
from dt_maps.types.geometry import Pose3D


class Frame(EntityHelper):

    def __init__(self, m: Map, key: str):
        super(Frame, self).__init__(m, key)
        self._map = m
        self._key = key

    def __getitem__(self, item: str):
        return {
            "pose": self.pose,
            "relative_to": self.relative_to,
        }[item]

    @property
    def pose(self) -> Pose3D:
        return Pose3D.create(self._map, self._key)

    @property
    def relative_to(self) -> Optional[str]:
        return self._map.layers.frames[self._key]["relative_to"]

    @relative_to.setter
    def relative_to(self, value: Optional[str]):
        self._map.layers.frames[self._key]["relative_to"] = value
