from unittest.mock import MagicMock

from domain.hospital_commands import HospitalCommands
from tests.hospital_helper import (
    make_hospital,
    get_actual_hospital_db_as_statuses_list,
)

from exceptions.hospital_exception import (
    PatientIdIsNotPositiveIntegerError,
    PatientIsNotExistsError,
    PatientStatusNotAllowedForHospitalizationError,
)


class TestHospitalCommands:

    def test_get_status(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(make_hospital([3, 2]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)

        hospital_commands.get_status()

        io_mock.report_status.assert_called_with("Готов к выписке")

    def test_get_status_when_patient_not_exists(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(make_hospital([None, 2]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)

        hospital_commands.get_status()

        io_mock.report_message.assert_called_with(PatientIsNotExistsError().message)

    def test_get_status_when_patient_id_positive_integer(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(make_hospital([1, 2]), io_mock)
        io_mock.request_patient_id = MagicMock(side_effect=PatientIdIsNotPositiveIntegerError)

        hospital_commands.get_status()

        io_mock.report_message.assert_called_with(PatientIdIsNotPositiveIntegerError().message)

    def test_status_up(self):
        io_mock = MagicMock()
        hospital = make_hospital([2, 3])
        hospital_commands = HospitalCommands(hospital, io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)

        hospital_commands.status_up()

        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 3]
        io_mock.report_new_status.assert_called_with("Готов к выписке")

    def test_status_up_when_status_too_high_and_patient_discharged(self):
        io_mock = MagicMock()
        hospital = make_hospital([3, 2])
        hospital_commands = HospitalCommands(hospital, io_mock)

        io_mock.request_patient_id = MagicMock(return_value=1)
        io_mock.request_need_to_discharge = MagicMock(return_value=True)

        hospital_commands.status_up()

        assert get_actual_hospital_db_as_statuses_list(hospital) == [None, 2]
        io_mock.request_need_to_discharge.assert_called()
        io_mock.report_patient_discharged.assert_called()

    def test_status_up_when_status_too_high_and_patient_not_discharged(self):
        io_mock = MagicMock()
        hospital = make_hospital([3, 0])
        hospital_commands = HospitalCommands(hospital, io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)
        io_mock.request_need_to_discharge = MagicMock(return_value=False)

        hospital_commands.status_up()

        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 0]
        io_mock.report_status_not_changed.assert_called_with("Готов к выписке")

    def test_status_up_when_patient_not_exists(self):
        io_mock = MagicMock()
        hospital = make_hospital([None, 2])
        hospital_commands = HospitalCommands(hospital, io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)

        hospital_commands.status_up()

        io_mock.report_message.assert_called_with(PatientIsNotExistsError().message)

    def test_status_up_when_patient_id_is_not_positive_integer(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(make_hospital([1, 2]), io_mock)
        io_mock.request_patient_id = MagicMock(side_effect=PatientIdIsNotPositiveIntegerError)

        hospital_commands.status_up()

        io_mock.report_message.assert_called_with(PatientIdIsNotPositiveIntegerError().message)

    def test_get_statistic(self):
        expected_statistics = {"Болен": 3, "Слегка болен": 2, "Готов к выписке": 1}

        io_mock = MagicMock()
        hospital_commands = HospitalCommands(make_hospital([1, 2, 3, 1, None, 1, 2]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)

        hospital_commands.get_statistic()

        io_mock.report_statistic.assert_called_with(6, expected_statistics)

    def test_add_patient(self):
        io_mock = MagicMock()

        hospital = make_hospital([3, 2])
        hospital_commands = HospitalCommands(hospital, io_mock)
        io_mock.request_patient_status.return_value = "Болен"
        hospital_commands.add_patient()

        io_mock.report_patient_id.assert_called_with(3)
        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 2, 1]

    def test_add_patient_when_status_not_allowed(self):
        io_mock = MagicMock()

        hospital = make_hospital([3, 2])
        hospital_commands = HospitalCommands(hospital, io_mock)
        io_mock.request_patient_status = MagicMock(side_effect=PatientStatusNotAllowedForHospitalizationError)
        hospital_commands.add_patient()

        io_mock.report_message.assert_called_with(PatientStatusNotAllowedForHospitalizationError().message)
        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 2]


