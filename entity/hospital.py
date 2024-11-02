from collections import Counter

from app_exceptions.validators_expection import ValidatorException
from hospital_data.patient_statuses import patient_statuses
from hospital_data.patient_statuses import PatientStatuses


class Hospital:
    def __init__(self, hospital_db: list):
        self.hospital_db = hospital_db

    def _update_status(self, patient_index: int, status_id: int | None) -> None:
        self.hospital_db[patient_index] = status_id

    def _get_patient_index(self, patient_id: int) -> int:
        patient_index = patient_id - 1
        if len(self.hospital_db) <= int(patient_index) or self.hospital_db[patient_index] is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")
        return patient_index

    def get_status(self, patient_id: int) -> str:
        patient_index = self._get_patient_index(patient_id)
        status_id = self.hospital_db[patient_index]
        return patient_statuses[status_id]

    def can_status_down(self, patient_id: int) -> bool:
        patient_index = self._get_patient_index(patient_id)
        status_id = self.hospital_db[patient_index]
        return status_id > PatientStatuses.hard_sick.value

    def can_status_up(self, patient_id: int) -> bool:
        patient_index = self._get_patient_index(patient_id)
        status_id = self.hospital_db[patient_index]
        return status_id < PatientStatuses.ready_to_discharge.value

    def status_up(self, patient_id: int) -> None:
        patient_index = self._get_patient_index(patient_id)
        status_id = self.hospital_db[patient_index]
        self._update_status(patient_index, status_id + 1)

    def status_down(self, patient_id: int) -> None:
        patient_index = self._get_patient_index(patient_id)
        status_id = self.hospital_db[patient_index]
        self._update_status(patient_index, status_id - 1)

    def discharge(self, patient_id: int) -> None:
        patient_index = self._get_patient_index(patient_id)
        self._update_status(patient_index, status_id=None)

    def _exclude_discharged_statuses(self) -> list:
        result = list(filter(lambda item: item is not None, self.hospital_db))
        return result

    def get_statistic_by_patients(self) -> dict:
        current_statuses = self._exclude_discharged_statuses()
        statistic = dict(Counter(current_statuses))
        sorted_statistic = dict(sorted(statistic.items(), key=lambda item: item[0]))
        return sorted_statistic

    def get_count_current_patients(self) -> int:
        total_count = len(self._exclude_discharged_statuses())
        return total_count
