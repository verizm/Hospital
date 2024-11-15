class MockConsole:
    def __init__(self):
        self._messages = []

    def add_expected_request_and_response(self, request_message: str, response_message: str):
        self._messages.append((request_message, response_message))

    def add_expected_output_message(self, output_message: str):
        self._messages.append(output_message)

    def verify_all_calls_have_been_made(self):
        if self._messages:
            raise AssertionError

    def _verify_messages_is_not_empty(self):
        if not self._messages:
            raise AssertionError("Console mock has not actual messages")

    @staticmethod
    def _verify_actual_message_as_expected(actual_message: str, expected_message: str):
        if actual_message != expected_message:
            raise AssertionError(f"'{actual_message}' not equal '{expected_message}'")

    def _get_first_message_and_remove(self):
        return self._messages.pop(0)

    def input(self, request_message: str) -> str:
        self._verify_messages_is_not_empty()

        expected_request_message, expected_response_message = self._get_first_message_and_remove()
        self._verify_actual_message_as_expected(request_message, expected_request_message)

        return expected_response_message

    def print(self, output_message: str):
        self._verify_messages_is_not_empty()
        expected_output_message = self._get_first_message_and_remove()
        self._verify_actual_message_as_expected(output_message, expected_output_message)
