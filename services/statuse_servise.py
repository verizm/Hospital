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
        patient_dto = self.db_service.get_patient_by_id(self.patient_id)
        current_status = patient_statuses[patient_dto.status_id]
        print(f"Cтатус пациента: {current_status}")

    def get_new_status(self) -> None:
        patient_dto = self.db_service.get_patient_by_id(self.patient_id)
        current_status = patient_statuses[patient_dto.status_id]
        print(f"Новый статус пациента: {current_status}")

    def status_down(self) -> None:
        patient_dto = self.db_service.get_patient_by_id(self.patient_id)
        if patient_dto.status_id == PatientStatuses.hard_sick.value:
            raise ValidatorException("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
        else:
            patient_dto.status_id -= 1
            self.db_service.update_patient(patient_dto)
            self.get_new_status()

    def status_up(self) -> None:
        patient_dto = self.db_service.get_patient_by_id(self.patient_id)
        if patient_dto.status_id < PatientStatuses.ready_to_discharge.value:
            patient_dto.status_id += 1
            self.db_service.update_patient(patient_dto)
            self.get_new_status()
        else:
            answer = input("Желаете этого клиента выписать? (да/нет) ").lower()

            if answer == "да":
                DischargeService(self.patient_id, self.db_service).discharge()
            else:
                status = patient_statuses[patient_dto.status_id]
                print(f"Пациент остался в статусе '{status}'")
