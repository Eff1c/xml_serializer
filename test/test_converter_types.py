from typing import NamedTuple

import pytest

from xml_serializer.abstract_type import AbstractType
from xml_serializer.converter_types import String, Integer, Float, Boolean, NestedType


class ConverterTypeTestCase(NamedTuple):
    converter_type: AbstractType
    payload: str
    expected_response: any


class TestConverterTypes:
    valid_test_data = [
        ConverterTypeTestCase(
            converter_type=String,
            payload="test string",
            expected_response="test string"
        ),
        ConverterTypeTestCase(
            converter_type=Integer,
            payload="123",
            expected_response=123
        ),
        ConverterTypeTestCase(
            converter_type=Float,
            payload="123.123",
            expected_response=123.123
        ),
        ConverterTypeTestCase(
            converter_type=Boolean,
            payload="true",
            expected_response=True
        ),
        ConverterTypeTestCase(
            converter_type=Boolean,
            payload="false",
            expected_response=False
        ),
    ]

    @pytest.mark.parametrize('test_case', valid_test_data)
    def test_convert(self, test_case: ConverterTypeTestCase):
        converter = test_case.converter_type()

        assert converter.convert(test_case.payload) == test_case.expected_response


class NestedTypeTestCase(NamedTuple):
    schema: dict
    data_handling_function: any
    expected_error: Exception
    error_message: str


class TestNestedType:
    correct_schema = {"test": "test"}

    def correct_data_handling_function():
        pass

    incorrect_init_test_data = [
        NestedTypeTestCase(
            schema="",
            data_handling_function=correct_data_handling_function,
            expected_error=ValueError,
            error_message="Missing required argument - schema!"
        ),
        NestedTypeTestCase(
            schema=None,
            data_handling_function=None,
            expected_error=ValueError,
            error_message="Missing required argument - schema!"
        ),
        NestedTypeTestCase(
            schema={},
            data_handling_function="",
            expected_error=ValueError,
            error_message="Missing required argument - schema!"
        ),
        NestedTypeTestCase(
            schema=correct_schema,
            data_handling_function="",
            expected_error=ValueError,
            error_message="Missing required argument - data_handling_function!"
        ),
        NestedTypeTestCase(
            schema=correct_schema,
            data_handling_function=None,
            expected_error=ValueError,
            error_message="Missing required argument - data_handling_function!"
        ),
        NestedTypeTestCase(
            schema=correct_schema,
            data_handling_function="test",
            expected_error=TypeError,
            error_message="data_handling_function must be callable!"
        ),
        NestedTypeTestCase(
            schema=correct_schema,
            data_handling_function={"test": "test"},
            expected_error=TypeError,
            error_message="data_handling_function must be callable!"
        ),
    ]

    @pytest.mark.parametrize(
        'test_case',
        incorrect_init_test_data,
    )
    def test_init_with_incorrect_args(self, test_case: NestedTypeTestCase):
        with pytest.raises(test_case.expected_error) as error:
            NestedType(test_case.schema, test_case.data_handling_function)

        assert error.value.__str__() == test_case.error_message

    def test_correct_init(self):
        NestedType(self.correct_schema, self.correct_data_handling_function)
