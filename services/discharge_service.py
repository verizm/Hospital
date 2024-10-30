from dto.patient import PatientDto
from app_exceptions.validators_expection import ValidatorException


class DischargeService:
    def __init__(self, patient: PatientDto):
        self.patient = patient

    def discharge(self) -> None:
        if self.patient.status_id is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")
        else:
            self.patient.status_id = None
            print("Пациент выписан из больницы")
