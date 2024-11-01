from services.db_service import DbService
from app_exceptions.validators_expection import ValidatorException


class DischargeService:
    def __init__(self, patient_id: str, db_service: DbService):
        self.patient_id = patient_id
        self.db_service = db_service

    def discharge(self) -> None:
        status_id = self.db_service.get_patient_status_id(self.patient_id)
        if status_id is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")
        else:
            self.db_service.update_patient_status_id(self.patient_id, status_id=None)
            print("Пациент выписан из больницы")
