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

    def update_patient_status_id(self, patient_id: str, status_id: int | None) -> None:
        patient_index = self._get_patient_index(patient_id)
        self.__data_base[patient_index] = status_id

    def get_patient_status_id(self, patient_id: str) -> int:
        patient_index = self._get_patient_index(patient_id)
        if len(self.__data_base) <= int(patient_index) or self.__data_base[patient_index] is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")

        status = self.__data_base[patient_index]
        return status

    def get_all_statuses(self) -> list:
        return self.__data_base
