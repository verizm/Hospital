import unittest
from unittest.mock import (
    MagicMock,
)

from domain.hospital_commands import HospitalCommands
from domain.hospital import Hospital


class TestHospitalCommands(unittest.TestCase):

    def test_get_status(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(Hospital([3]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)

        hospital_commands.get_status()

        io_mock.report_status.assert_called_with("Готов к выписке")

    def test_discharge_patient_after_status_up(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(Hospital([3]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)
        io_mock.request_need_to_discharge = MagicMock(return_value=True)

        hospital_commands.status_up()

        io_mock.request_need_to_discharge.assert_called()
        io_mock.report_patient_discharged.assert_called()

    def test_not_discharge_patient_after_status_up(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(Hospital([3]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)
        io_mock.request_need_to_discharge = MagicMock(return_value=False)

        hospital_commands.status_up()

        io_mock.report_status_not_changed.assert_called()

    def test_status_up(self):
        io_mock = MagicMock()
        hospital_commands = HospitalCommands(Hospital([2]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)
        io_mock.request_need_to_discharge = MagicMock(return_value=True)

        hospital_commands.status_up()

        io_mock.report_new_status.assert_called()

    def test_get_statistic(self):
        expected_statistics = {"Тяжело болен": 1, "Болен": 1, "Слегка болен": 1, "Готов к выписке": 1}

        io_mock = MagicMock()
        hospital_commands = HospitalCommands(Hospital([3, 2, 1, 0, None]), io_mock)
        io_mock.request_patient_id = MagicMock(return_value=1)

        hospital_commands.get_statistic()

        io_mock.report_statistic.assert_called_with(4, expected_statistics)
