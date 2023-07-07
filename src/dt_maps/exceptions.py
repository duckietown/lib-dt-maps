import json
from typing import Type, Union, Any, Iterable, Optional


class EntityNotFound(Exception):

    def __init__(self, layer: str, **kwargs):
        super(EntityNotFound, self).__init__(
            f"Entity with properties '{str(kwargs)}' not found in '{layer}' layer"
        )


class FieldNotFound(Exception):

    def __init__(self, key: str, layer: Optional[str], field: str, helper: Optional[type] = None):
        layer_info = f"from layer '{layer}' " if layer else ""
        key_info = key if helper is None else f"{helper.__name__}('{key}')"
        super(FieldNotFound, self).__init__(
            f"Entity {key_info} {layer_info}does not have field '{field}'"
        )


class InvalidMapLayer(Exception):

    def __init__(self, layer: str, reason: str, **kwargs):
        extra: str = ""
        if kwargs:
            extra = f"\nExtras:\n{json.dumps(kwargs, indent=4, sort_keys=True)}"
        super(InvalidMapLayer, self).__init__(f"Layer '{layer}' is not valid. Reason: {reason}.{extra}")


class MissingMapLayer(Exception):

    def __init__(self, layer: str, reason: str, **kwargs):
        extra: str = ""
        if kwargs:
            extra = f"\nExtras:\n{json.dumps(kwargs, indent=4, sort_keys=True)}"
        super(MissingMapLayer, self).__init__(f"Layer '{layer}' does not exist. Reason: {reason}.{extra}")


def assert_type(value: Any, types: Union[type, Iterable[type]], field: Optional[str] = None):
    if not isinstance(value, types):
        msg = "Expected "
        msg += f"types {types} " if isinstance(types, (list, set, tuple)) else f"type {types} "
        msg += f"for field '{field}' " if field else ""
        msg += f", received {type(value)} instead."
        raise ValueError(msg)
