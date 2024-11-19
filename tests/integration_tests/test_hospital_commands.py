from unittest.mock import MagicMock

from domain.hospital_commands import HospitalCommands
from tests.hospital_helper import (
    make_hospital,
    get_actual_hospital_db_as_statuses_list,
)

from exceptions.hospital_exception import (
    PatientIdIsNotPositiveIntegerError,
    PatientIsNotExistsError,
    PatientStatusIsNotExistsError
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
        io_mock.report_new_status.assert_called()

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
        io_mock.report_status_not_changed.assert_called()

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
        hospital = make_hospital([3, 0])
        hospital_commands = HospitalCommands(hospital, io_mock)
        io_mock.request_patient_status = MagicMock(return_value="Болен")

        hospital_commands.add_patient()

        io_mock.report_patient_id.assert_called_with(3)

        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 0, 1]

    def test_add_patient_when_status_not_exists(self):
        io_mock = MagicMock()

        hospital = make_hospital([3, 2])
        statuses = list(hospital._patient_statuses.values())
        hospital_commands = HospitalCommands(hospital, io_mock)

        io_mock.request_patient_status = MagicMock(return_value="Not Valid")
        hospital_commands.add_patient()

        io_mock.report_message.assert_called_with(PatientStatusIsNotExistsError(statuses).message)
        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 2]

    def test_status_up_unit(self):
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

    def test_status_up_when_status_too_high_and_patient_not_discharged_unit(self):
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

    def test_status_up_when_status_too_high_and_patient_discharged_unit(self):
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

    def test_status_up_when_patient_not_exists_unit(self):
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
