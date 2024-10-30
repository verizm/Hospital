from collections import Counter
from app_exceptions.validators_expection import ValidatorException
from patient_statuses import STATUSES
from dto.patient import PatientDto


class DbService:
    def __init__(self):
        self.data_base = None

    def set_db(self, data_base: list) -> None:
        if not self.data_base:
            self.data_base = data_base

    def update_patient(self, patient: PatientDto) -> None:
        self.data_base[patient.patient_id] = patient.status_id

    def get_patient_by_id(self, patient_id: int) -> PatientDto:
        if len(self.data_base) < int(patient_id) or patient_id is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")

        status = self.data_base[patient_id]
        return PatientDto(status_id=status, patient_id=patient_id)

    def _exclude_discharged_patients(self) -> list:
        list_current_patients = list(filter(lambda item: item is not None, self.data_base))
        return list_current_patients

    def get_total_patient_count(self) -> int:
        return len(self._exclude_discharged_patients())

    def get_statistic_by_patient(self) -> dict:
        statistic = Counter(self._exclude_discharged_patients())
        return dict(statistic)
