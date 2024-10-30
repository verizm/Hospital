from dto.patient import PatientDto
from app_exceptions.validators_expection import ValidatorException
from patient_statuses import StatusesBoundaryValues


class StatusService:

    def __init__(self, patient: PatientDto):
        self.patient = patient

    def get_status(self) -> None:
        print(f"Новый статус пациента: {self.patient.status_value}")

    def status_down(self) -> None:
        if self.patient.status_id == StatusesBoundaryValues.HARD_SICK.value:
            raise ValidatorException("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
        else:
            self.patient.status_id -= 1
            self.get_status()

    def status_up(self) -> bool:
        if self.patient.status_id == StatusesBoundaryValues.READY_TO_DISCHARGE.value:
            print("Желаете этого клиента выписать? (да/нет)")
            answer = input().lower()
            if result := (answer == "да"):
                return result
        else:
            self.patient.status_id += 1
            self.get_status()
