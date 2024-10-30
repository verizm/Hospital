from dto.patient import PatientDto
from app_exceptions.validators_expection import ValidatorException
from patient_statuses import PatientStatuses


class StatusService:

    def __init__(self, patient: PatientDto):
        self.patient = patient

    def get_status(self) -> None:
        print(f"Cтатус пациента: {self.patient.status_value}")

    def get_new_status(self) -> None:
        print(f"Новый статус пациента: {self.patient.status_value}")

    def status_down(self) -> None:
        if self.patient.status_id == PatientStatuses.hard_sick.value:
            raise ValidatorException("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
        else:
            self.patient.status_id -= 1
            self.get_new_status()

    def status_up(self) -> bool:
        if self.patient.status_id < PatientStatuses.ready_to_discharge.value:
            self.patient.status_id += 1
            self.get_new_status()
        else:
            answer = input("Желаете этого клиента выписать? (да/нет) ").lower()

            if answer == "да":
                return True
            else:
                print(f"Пациент остался в статусе '{self.patient.status_value}'")

        return False
