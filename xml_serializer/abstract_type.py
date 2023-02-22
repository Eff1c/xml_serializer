from abc import ABC, abstractmethod


class AbstractType(ABC):
    nullable = None

    def __init__(self, nullable=True):
        self.nullable = nullable

    @abstractmethod
    def convert_method(self, value):
        pass

    def convert(self, value):
        value = value.strip() or None

        if value is None:
            if self.nullable:
                return None

            raise TypeError("Missing required argument!")

        return self.convert_method(value)
