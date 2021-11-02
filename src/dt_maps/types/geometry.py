from dt_maps import Map
from dt_maps.types.commons import EntityHelper


class Pose3D(EntityHelper):

    def __init__(self, m: Map, key: str):
        super(Pose3D, self).__init__(m, key)
        self._map = m
        self._key = key

    def __getitem__(self, item: str):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "roll": self.roll,
            "pitch": self.pitch,
            "yaw": self.yaw,
        }[item]

    def _set_property(self, name: str, value: float):
        self._map.layers.frames[self._key]["pose"][name] = value

    def _get_property(self, name: str) -> float:
        return self._map.layers.frames[self._key]["pose"][name]

    @property
    def x(self) -> float:
        return self._get_property("x")

    @property
    def y(self) -> float:
        return self._get_property("y")

    @property
    def z(self) -> float:
        return self._get_property("z")

    @property
    def roll(self) -> float:
        return self._get_property("roll")

    @property
    def pitch(self) -> float:
        return self._get_property("pitch")

    @property
    def yaw(self) -> float:
        return self._get_property("yaw")

    @x.setter
    def x(self, value: float):
        self._set_property("x", value)

    @y.setter
    def y(self, value: float):
        self._set_property("y", value)

    @z.setter
    def z(self, value: float):
        self._set_property("z", value)

    @roll.setter
    def roll(self, value: float):
        self._set_property("roll", value)

    @pitch.setter
    def pitch(self, value: float):
        self._set_property("pitch", value)

    @yaw.setter
    def yaw(self, value: float):
        self._set_property("yaw", value)
