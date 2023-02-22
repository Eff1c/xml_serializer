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
    schema = None
    data_handling_function = None

    def __init__(self, schema, data_handling_function=None, *args, **kwargs):
        super(NestedType, self).__init__(*args, **kwargs)
        self.schema = schema
        self.data_handling_function = data_handling_function

    def data_handle(self, data):
        if self.data_handling_function:
            return self.data_handling_function(data)

        return data

    def _serialize(self, tag):
        return serialize_by_inner_schema(self.schema, tag)

    def convert_method(self, tag):
        data = self._serialize(tag)
        response = self.data_handle(data)

        return response
