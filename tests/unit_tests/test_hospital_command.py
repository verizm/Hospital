from unittest.mock import MagicMock

from domain.hospital_commands import HospitalCommands
from exceptions.hospital_exception import (
    PatientIsNotExistsError,
    PatientIdIsNotPositiveIntegerError,
)


class TestHospitalCommandUnit:
    def test_status_up(self):
        io_mock = MagicMock()
        hospital_mock = MagicMock()
        hospital_commands = HospitalCommands(hospital_mock, io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)
        hospital_mock.can_status_up = MagicMock(return_value=True)
        hospital_mock.get_status = MagicMock(return_value="Слегка болен")

        hospital_commands.status_up()

        io_mock.request_patient_id.assert_called()
        hospital_mock.can_status_up.assert_called_with(1)
        hospital_mock.status_up.assert_called_with(1)

        hospital_mock.get_status.assert_called_with(1)
        io_mock.report_new_status.assert_called_with("Слегка болен")

    def test_status_up_when_status_too_high_and_patient_not_discharged(self):
        io_mock = MagicMock()
        hospital_mock = MagicMock()
        hospital_commands = HospitalCommands(hospital_mock, io_mock)

        io_mock.request_patient_id = MagicMock(return_value=1)
        hospital_mock.can_status_up = MagicMock(return_value=False)
        io_mock.request_need_to_discharge = MagicMock(return_value=False)

        hospital_commands.status_up()

        io_mock.request_patient_id.assert_called()
        hospital_mock.can_status_up.assert_called_with(1)

        io_mock.request_need_to_discharge.assert_called()
        hospital_mock.get_status.assert_called_with(1)
        io_mock.report_status_not_changed.assert_called()

    def test_status_up_when_status_too_high_and_patient_discharged(self):
        io_mock = MagicMock()
        hospital_mock = MagicMock()
        hospital_commands = HospitalCommands(hospital_mock, io_mock)

        io_mock.request_patient_id = MagicMock(return_value=1)
        hospital_mock.can_status_up = MagicMock(return_value=False)
        io_mock.request_need_to_discharge = MagicMock(return_value=True)

        hospital_commands.status_up()

        io_mock.request_patient_id.assert_called()
        hospital_mock.can_status_up.assert_called_with(1)

        io_mock.request_need_to_discharge.assert_called()
        hospital_mock.discharge.assert_called_with(1)
        io_mock.report_patient_discharged.assert_called()

    def test_status_up_when_patient_not_exists(self):
        io_mock = MagicMock()
        hospital_mock = MagicMock()
        hospital_commands = HospitalCommands(hospital_mock, io_mock)
        io_mock.request_patient_id = MagicMock(return_value=201)
        hospital_mock.can_status_up = MagicMock(side_effect=PatientIsNotExistsError)

        hospital_commands.status_up()

        io_mock.request_patient_id.assert_called()
        hospital_mock.can_status_up.assert_called_with(201)
        io_mock.report_message.assert_called_with(PatientIsNotExistsError().message)

    def test_status_up_when_patient_id_is_not_positive_integer_unit(self):
        io_mock = MagicMock()
        hospital_mock = MagicMock()
        hospital_commands = HospitalCommands(hospital_mock, io_mock)
        io_mock.request_patient_id = MagicMock(side_effect=PatientIdIsNotPositiveIntegerError)

        hospital_commands.status_up()

        io_mock.request_patient_id.assert_called()
        io_mock.report_message.assert_called_with(PatientIdIsNotPositiveIntegerError().message)
