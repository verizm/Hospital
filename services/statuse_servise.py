from services.db_service import DbService
from patient_statuses import patient_statuses
from services.discharge_service import DischargeService
from app_exceptions.validators_expection import ValidatorException
from patient_statuses import PatientStatuses


class StatusService:

    def __init__(self, patient_id: str, db_service: DbService):
        self.patient_id = patient_id
        self.db_service = db_service

    def get_status(self) -> None:
        status_id = self.db_service.get_patient_status_id(self.patient_id)
        print(f"Cтатус пациента: {patient_statuses[status_id]}")

    @staticmethod
    def _get_new_status(status_id: int) -> None:
        print(f"Новый статус пациента: {patient_statuses[status_id]}")

    def status_down(self) -> None:
        status_id = self.db_service.get_patient_status_id(self.patient_id)
        if status_id == PatientStatuses.hard_sick.value:
            raise ValidatorException("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
        else:
            status_id -= 1
            self.db_service.update_patient_status_id(self.patient_id, status_id)
            self._get_new_status(status_id)

    def status_up(self) -> None:
        status_id = self.db_service.get_patient_status_id(self.patient_id)

        if status_id < PatientStatuses.ready_to_discharge.value:
            status_id += 1
            self.db_service.update_patient_status_id(self.patient_id, status_id)
            self._get_new_status(status_id)
        else:
            answer = input("Желаете этого клиента выписать? (да/нет) ").lower()

            if answer == "да":
                DischargeService(self.patient_id, self.db_service).discharge()
            else:
                print(f"Пациент остался в статусе '{patient_statuses[status_id]}'")
