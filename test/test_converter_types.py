import pytest

from xml_serializer.converter_types import String, Integer, Float, Boolean


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
