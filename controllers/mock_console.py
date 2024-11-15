from collections import defaultdict


class MockConsole:
    def __init__(self):
        self._input_calls = []
        self._print_calls = []

    def add_expected_request_and_response(self, request: str, response: str):
        self._input_calls.append((request, response))

    def add_expected_output_message(self, output_message: str):
        self._print_calls.append(output_message)

    def verify_all_calls_have_been_made(self):
        if any([self._input_calls, self._print_calls]):
            raise AssertionError

    def _verify_calls_is_not_empty(self, calls: list):
        if not calls:
            raise AssertionError("Calls is empty")

    def _verify_actual_as_expected(self, actual, expected):
        if actual != expected:
            raise AssertionError(f"'{actual}' не равно '{expected}'")

    def _get_first_value_from_calls(self, calls):
        return calls.pop(0)

    def input(self, request: str):
        self._verify_calls_is_not_empty(self._input_calls)
        expected_request, expected_response = self._get_first_value_from_calls(self._input_calls)
        self._verify_actual_as_expected(request, expected_request)
        return expected_response

    def print(self, output_message: str):
        self._verify_calls_is_not_empty(self._print_calls)
        value = self._get_first_value_from_calls(self._print_calls)
        self._verify_actual_as_expected(value, output_message)
