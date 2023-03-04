class BaseField:
    def __init__(self, field_name: str, name: str = None):
        self.field_name = field_name

        if not name:
            name = field_name

        self.name = name


class Tag(BaseField):
    """
    Describes a tag in the serialization scheme
    """
    pass


class TagAttr(BaseField):
    """
    Describes a tag attribute in the serialization scheme
    """
    pass
