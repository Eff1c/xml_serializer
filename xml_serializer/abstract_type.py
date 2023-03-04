from abc import abstractmethod


class AbstractType:
    def __init__(self, nullable=True):
        self.nullable = nullable

    @abstractmethod
    def convert_method(self, value):
        pass

    def convert(self, value):
        if not isinstance(value, str):
            raise TypeError("value argument must be a string!")

        value = value.strip() or None

        if value is None:
            if self.nullable:
                return None

            raise ValueError("Missing required argument!")

        return self.convert_method(value)
