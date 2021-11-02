from typing import Union, Iterable, Any, Optional

from dt_maps import Map
from dt_maps.types.commons import EntityHelper
from . import get_asset_path


class Person(EntityHelper):

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            "name": str,
            "age": int,
        }[name]

    def _get_layer_name(self) -> str:
        return "people"

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            "name": None,
            "age": None,
        }[name]

    @property
    def name(self) -> str:
        return self._get_property("name")

    @property
    def age(self) -> int:
        return self._get_property("age")

    @name.setter
    def name(self, value: str):
        self._set_property("name", str, value)

    @age.setter
    def age(self, value: int):
        self._set_property("age", int, value)


def _load_map() -> Map:
    map_dir = get_asset_path("maps/custom_layers")
    return Map.from_disk("custom_layers", map_dir)


def test_people_num_people():
    m = _load_map()
    assert len(m.layers.people) == 2


def test_people_person_0():
    m = _load_map()
    person = "person_0"
    assert m.layers.people[person]["name"] == "John"
    assert m.layers.people[person]["age"] == 27


def test_people_set_setitem():
    m = _load_map()
    person = "person_0"
    test_people_person_0()
    m.layers.people[person]["name"] = "Mark"
    m.layers.people[person]["age"] = 30
    try:
        test_people_person_0()
        assert False
    except AssertionError:
        pass
    assert m.layers.people[person]["name"] == "Mark"
    assert m.layers.people[person]["age"] == 30


def test_people_set_no_helper():
    m = _load_map()
    person = "person_0"
    try:
        m.layers.people[person].name = "Mark"
        assert False
    except AttributeError:
        pass


def test_people_set_with_helper():
    m = _load_map()
    person = "person_0"
    test_people_person_0()
    # register helper
    m.layers.people.register_entity_helper(Person)
    # test
    m.layers.people[person].name = "Mark"
    m.layers.people[person].age = 30
    try:
        test_people_person_0()
        assert False
    except AssertionError:
        pass
    assert m.layers.people[person].name == "Mark"
    assert m.layers.people[person].age == 30


def test_people_get_with_helper():
    m = _load_map()
    person = "person_0"
    # register helper
    m.layers.people.register_entity_helper(Person)
    assert m.layers.people[person].name == "John"
    assert m.layers.people[person].age == 27
