import pytest

from xml_serializer.converter_types import String, Integer, Float, Boolean, NestedType

valid_test_data = [
    (
        String,
        "test string",
        "test string"
    ),
    (
        Integer,
        "123",
        123
    ),
    (
        Float,
        "123.123",
        123.123
    ),
    (
        Boolean,
        "true",
        True
    ),
    (
        Boolean,
        "false",
        False
    ),
]


@pytest.mark.parametrize('converter_type, payload, expected_response', valid_test_data)
def test_common_types(converter_type, payload, expected_response):
    converter = converter_type()

    assert converter.convert(payload) == expected_response


correct_schema = {"test": "test"}


def correct_data_handling_function():
    pass


incorrect_init_test_data = [
    (
        "",
        correct_data_handling_function,
        ValueError,
        "Missing required argument - schema!"
    ),
    (
        None,
        None,
        ValueError,
        "Missing required argument - schema!"
    ),
    (
        {},
        "",
        ValueError,
        "Missing required argument - schema!"
    ),
    (
        correct_schema,
        "",
        ValueError,
        "Missing required argument - data_handling_function!"
    ),
    (
        correct_schema,
        None,
        ValueError,
        "Missing required argument - data_handling_function!"
    ),
    (
        correct_schema,
        "test",
        TypeError,
        "data_handling_function must be callable!"
    ),
    (
        correct_schema,
        {"test": "test"},
        TypeError,
        "data_handling_function must be callable!"
    )
]


class TestNestedType:
    @pytest.mark.parametrize(
        'schema, data_handling_function, expected_error, error_message',
        incorrect_init_test_data
    )
    def test_init_with_incorrect_args(
            self, schema, data_handling_function, expected_error, error_message
    ):
        with pytest.raises(expected_error) as error:
            NestedType(schema, data_handling_function)

        assert error.value.__str__() == error_message

    def test_correct_init(self):
        NestedType(correct_schema, correct_data_handling_function)
