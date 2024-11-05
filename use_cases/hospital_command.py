from infrastructure.io_helper import IOHelper
from entity.hospital import Hospital
from exceptions.hospital_exception import (
    UserIdIsNotPositiveIntegerException,
    UserIsNotExistsException,
)


class HospitalCommands:
    def __init__(self, hospital: Hospital, io_helper: IOHelper):
        self._hospital = hospital
        self._io_helper = io_helper

    def get_statistic(self):
        total_count = self._hospital.get_count_current_patients()
        statistics = self._hospital.get_statistic_by_patients()
        self._io_helper.response_statistic(total_count, statistics)

    def get_status(self) -> None:
        try:
            patient_id = self._io_helper.request_patient_id()
            status = self._hospital.get_status(patient_id)
            self._io_helper.response_status(status)

        except UserIdIsNotPositiveIntegerException as id_exception:
            self._io_helper.response_message(id_exception.message)

        except UserIsNotExistsException as user_not_exists_exception:
            self._io_helper.response_message(user_not_exists_exception.message)

    def status_down(self) -> None:
        try:
            patient_id = self._io_helper.request_patient_id()

            if self._hospital.can_status_down(patient_id):
                self._hospital.status_down(patient_id)
                status = self._hospital.get_status(patient_id)
                self._io_helper.response_new_status(status)
            else:
                self._io_helper.response_status_too_low()

        except UserIdIsNotPositiveIntegerException as input_exception:
            self._io_helper.response_message(input_exception.message)

        except UserIsNotExistsException as user_not_exists_exception:
            self._io_helper.response_message(user_not_exists_exception.message)

    def discharge(self) -> None:
        try:
            patient_id = self._io_helper.request_patient_id()
            self._hospital.discharge(patient_id)
            self._io_helper.response_patient_discharged()

        except UserIdIsNotPositiveIntegerException as input_exception:
            self._io_helper.response_message(input_exception.message)

        except UserIsNotExistsException as user_not_exists_exception:
            self._io_helper.response_message(user_not_exists_exception.message)

    def status_up(self) -> None:
        try:
            patient_id = self._io_helper.request_patient_id()

            if self._hospital.can_status_up(patient_id):
                self._hospital.status_up(patient_id)
                status = self._hospital.get_status(patient_id)
                self._io_helper.response_new_status(status)
            else:
                if self._io_helper.request_need_to_discharge():
                    self._hospital.discharge(patient_id)
                    self._io_helper.response_patient_discharged()
                else:
                    status = self._hospital.get_status(patient_id)
                    self._io_helper.response_status_not_changed(status)

        except UserIdIsNotPositiveIntegerException as input_exception:
            self._io_helper.response_message(input_exception.message)

        except UserIsNotExistsException as user_not_exists_exception:
            self._io_helper.response_message(user_not_exists_exception.message)