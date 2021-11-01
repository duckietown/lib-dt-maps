class EntityNotFound(Exception):

    def __init__(self, layer: str, **kwargs):
        super(EntityNotFound, self).__init__(
            f"Entity with properties '{str(kwargs)}' not found in '{layer}' layer"
        )