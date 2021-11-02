from typing import Type, Union, Any, Iterable, Optional


class EntityNotFound(Exception):

    def __init__(self, layer: str, **kwargs):
        super(EntityNotFound, self).__init__(
            f"Entity with properties '{str(kwargs)}' not found in '{layer}' layer"
        )


def assert_type(value: Any, types: Union[type, Iterable[type]], field: Optional[str] = None):
    if not isinstance(value, types):
        msg = "Expected "
        msg += f"types {types} " if isinstance(types, (list, set, tuple)) else f"type {types} "
        msg += f"for field '{field}' " if field else ""
        msg += f", received {type(value)} instead."
        raise ValueError(msg)