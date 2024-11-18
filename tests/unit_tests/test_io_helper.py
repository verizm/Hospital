import pytest
from exceptions.hospital_exception import (
    PatientIdIsNotPositiveIntegerError,
    PatientStatusNotAllowedForHospitalizationError,
)
from controllers.io_helper import IOHelper
from unittest.mock import MagicMock


class TestIoHelper:

    def test_report_status_too_low(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)

        io_helper.report_status_too_low()
        console_mock.print.assert_called_with("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    def test_report_unknown_command(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)

        io_helper.report_unknown_command()
        console_mock.print.assert_called_with("Неизвестная команда! Попробуйте ещё раз")

    def test_request_command(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = "get status"

        actual_command = io_helper.request_command()

        console_mock.input.assert_called_with("Введите команду: ")
        assert actual_command == "get status"

    def test_request_command_when_command_is_unknown(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = "узнать врача"

        command = io_helper.request_command()

        console_mock.input.assert_called_with("Введите команду: ")
        assert command == "unknown"

    def test_request_patient_id(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = " 3 "

        patient_id_converted_to_int = io_helper.request_patient_id()
        console_mock.input.assert_called_with("Введите ID пациента: ")
        assert patient_id_converted_to_int == 3

    def test_request_patient_id_when_patient_id_is_not_digit(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = "два"

        with pytest.raises(PatientIdIsNotPositiveIntegerError):
            io_helper.request_patient_id()

    def test_request_patient_id_when_patient_id_is_not_positive_integer(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = "-1"

        with pytest.raises(PatientIdIsNotPositiveIntegerError):
            io_helper.request_patient_id()

    def test_request_patient_id_when_patient_id_is_float(self):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = "0.1"

        with pytest.raises(PatientIdIsNotPositiveIntegerError):
            io_helper.request_patient_id()

    @pytest.mark.parametrize(
        "actual_status, expected_status",
        [
            ("Болен", "болен"),
            ("тяжело Болен", "тяжело болен"),
            ("СЛЕГКА БОЛЕН", "слегка болен"),

        ]
    )
    def test_request_patient_status(self, actual_status, expected_status):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = actual_status

        actual_status = io_helper.request_patient_status()

        assert actual_status == expected_status

    @pytest.mark.parametrize(
        "status",
        [
            "not allowed",
            "Готов к выписке"
        ]
    )
    def test_request_patient_status_when_status_not_allowed(self, status):
        console_mock = MagicMock()
        io_helper = IOHelper(console_mock)
        console_mock.input.return_value = status

        with pytest.raises(PatientStatusNotAllowedForHospitalizationError):
            io_helper.request_patient_status()
