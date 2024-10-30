from app_exceptions.validators_expection import ValidatorException
from dto.patient import PatientDto


class DbService:
    def __init__(self):
        self.__data_base = None

    def set_db(self, data_base: list) -> None:
        if not self.__data_base:
            self.__data_base = data_base

    def update_patient(self, patient: PatientDto) -> None:
        self.__data_base[patient.patient_id] = patient.status_id

    def get_patient_by_id(self, patient_id: int) -> PatientDto:
        if len(self.__data_base) <= int(patient_id) or self.__data_base[patient_id] is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")

        status = self.__data_base[patient_id]
        return PatientDto(status_id=status, patient_id=patient_id)

    def get_all_patients(self) -> list:
        return self.__data_base
