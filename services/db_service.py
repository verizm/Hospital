from app_exceptions.validators_expection import ValidatorException
from dto.patient import PatientDto


class DbService:
    def __init__(self):
        self.__data_base = None

    def set_db(self, data_base: list) -> None:
        if not self.__data_base:
            self.__data_base = data_base

    @staticmethod
    def _get_patient_index(patient_id: str) -> int:
        patient_index = int(patient_id) - 1
        return patient_index

    def update_patient(self, patient: PatientDto) -> None:
        patient_index = self._get_patient_index(patient.patient_id)
        self.__data_base[patient_index] = patient.status_id

    def get_patient_by_id(self, patient_id: str) -> PatientDto:
        patient_index = self._get_patient_index(patient_id)
        if len(self.__data_base) <= int(patient_index) or self.__data_base[patient_index] is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")

        status = self.__data_base[patient_index]
        return PatientDto(status_id=status, patient_id=patient_id)

    def get_all_patients(self) -> list:
        return self.__data_base
