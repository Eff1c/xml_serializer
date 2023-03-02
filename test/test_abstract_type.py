import pytest
from abstract_type import AbstractType
from typing import NamedTuple


class SuccessTestCase(NamedTuple):
    value: str
    abstract_type: AbstractType
    expected_response: any


class FailTestCase(NamedTuple):
    value: str
    abstract_type: AbstractType
    expected_error: Exception
    expected_error_message: str


class TestAbstractType:
    nullable_abstract_type = AbstractType(nullable=True)
    not_nullable_abstract_type = AbstractType(nullable=False)
    correct_value = "test"

    success_test_cases = [
        SuccessTestCase("", nullable_abstract_type, None),
        SuccessTestCase(correct_value, nullable_abstract_type, None),
        SuccessTestCase(correct_value, not_nullable_abstract_type, None),
    ]

    failed_test_cases = [
        FailTestCase(None, nullable_abstract_type, TypeError, "value argument must be a string!"),
        FailTestCase({}, nullable_abstract_type, TypeError, "value argument must be a string!"),
        FailTestCase("", not_nullable_abstract_type, ValueError, "Missing required argument!"),
    ]

    @pytest.mark.parametrize('test_case', success_test_cases)
    def test_success_convert(self, test_case):
        converted_value = test_case.abstract_type.convert(test_case.value)
        assert converted_value == test_case.expected_response

    @pytest.mark.parametrize('test_case', failed_test_cases)
    def test_failed_convert(self, test_case):
        with pytest.raises(test_case.expected_error) as error:
            test_case.abstract_type.convert(test_case.value)

        assert error.value.__str__() == test_case.expected_error_message
