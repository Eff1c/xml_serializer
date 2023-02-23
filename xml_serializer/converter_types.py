from .main import serialize_by_inner_schema
from .abstract_type import AbstractType


class String(AbstractType):
    def convert_method(self, value):
        return str(value)


class Integer(AbstractType):
    def convert_method(self, value):
        return int(value)


class Float(AbstractType):
    def convert_method(self, value):
        value = value.replace(",", ".")

        return float(value)


class Boolean(AbstractType):
    def convert_method(self, value):
        return True if value.lower() == "true" else False


class NestedType(AbstractType):
    """
    Class custom handle nested schema
    """
    def __init__(self, schema, data_handling_function, *args, **kwargs):
        super(NestedType, self).__init__(*args, **kwargs)
        self.schema = schema

        if not callable(data_handling_function):
            raise TypeError(f"{data_handling_function} is not callable!")

        self.data_handling_function = data_handling_function

    def convert_method(self, tag):
        data = serialize_by_inner_schema(self.schema, tag)
        response = self.data_handling_function(data)

        return response
