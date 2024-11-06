from collections import Counter
from exceptions.hospital_exception import (
    PatientIsNotExistsError,
    PatientStatusTooHighError,
    PatientStatusTooLowError,
)


class Hospital:
    def __init__(self, hospital_db: list):
        self._hospital_db = hospital_db
        self._patient_statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}
        self._max_status = max(self._patient_statuses)
        self._min_status = min(self._patient_statuses)

    @staticmethod
    def _convert_patient_id_to_patient_index(patient_id: int) -> int:
        return patient_id - 1

    def _check_patient_is_exists(self, patient_index: int):
        if len(self._hospital_db) <= int(patient_index) or self._hospital_db[patient_index] is None:
            raise PatientIsNotExistsError

    def get_status(self, patient_id: int) -> str:
        patient_index = self._convert_patient_id_to_patient_index(patient_id)
        status_id = self._hospital_db[patient_index]
        return self._patient_statuses[status_id]

    def can_status_down(self, patient_id: int) -> bool:
        patient_index = self._convert_patient_id_to_patient_index(patient_id)
        self._check_patient_is_exists(patient_index)
        return self._hospital_db[patient_index] > self._min_status

    def can_status_up(self, patient_id: int) -> bool:
        patient_index = self._convert_patient_id_to_patient_index(patient_id)
        self._check_patient_is_exists(patient_index)
        return self._hospital_db[patient_index] < self._max_status

    def status_up(self, patient_id: int):
        patient_index = self._convert_patient_id_to_patient_index(patient_id)
        self._check_patient_is_exists(patient_index)
        if self._hospital_db[patient_index] == self._max_status:
            raise PatientStatusTooHighError
        self._hospital_db[patient_index] += 1

    def status_down(self, patient_id: int):
        patient_index = self._convert_patient_id_to_patient_index(patient_id)
        self._check_patient_is_exists(patient_index)

        if self._hospital_db[patient_index] == self._min_status:
            raise PatientStatusTooLowError
        self._hospital_db[patient_index] -= 1

    def discharge(self, patient_id: int):
        patient_index = self._convert_patient_id_to_patient_index(patient_id)
        self._check_patient_is_exists(patient_index)
        self._hospital_db[patient_index] = None

    def _exclude_discharged_statuses(self) -> list:
        result = list(filter(lambda item: item is not None, self._hospital_db))
        return result

    def _change_status_id_on_status_value(self, statistic: dict) -> dict:
        return {self._patient_statuses[status_id]: value for status_id, value in statistic.items()}

    def count_statistic_by_patients(self) -> dict:
        current_statuses = self._exclude_discharged_statuses()
        sorted_statistic = dict(sorted(Counter(current_statuses).items(), key=lambda item: item[0]))
        user_readable_statistic = self._change_status_id_on_status_value(sorted_statistic)
        return user_readable_statistic

    def count_current_patients(self) -> int:
        total_count = len(self._exclude_discharged_statuses())
        return total_count
