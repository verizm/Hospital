from collections import Counter
from services.db_service import DbService
from patient_statuses import patient_statuses
from patient_statuses import PatientStatuses
from app_exceptions.validators_expection import ValidatorException


class HospitalService:
    def __init__(self, db_service: DbService):
        self.db_service = db_service

    def _exclude_discharged(self) -> list:
        patients = self.db_service.get_all_statuses()
        return list(filter(lambda item: item is not None, patients))

    def get_statistic(self):
        total = len(self._exclude_discharged())
        statistic = dict(Counter(self._exclude_discharged()))
        sorted_statistic = dict(sorted(statistic.items(), key=lambda item: item[0]))

        print(f"В больнице на данный момент находится {total} чел., из них:")
        for status_id, count_patients in sorted_statistic.items():
            print(f"- в статусе '{patient_statuses[status_id]}': {count_patients} чел.")

    @staticmethod
    def _get_new_status(status_id: int) -> None:
        print(f"Новый статус пациента: {patient_statuses[status_id]}")

    def get_status(self, patient_id: str) -> None:
        status_id = self.db_service.get_patient_status_id(patient_id)
        print(f"Cтатус пациента: {patient_statuses[status_id]}")

    def status_down(self, patient_id: str) -> None:
        status_id = self.db_service.get_patient_status_id(patient_id)
        if status_id == PatientStatuses.hard_sick.value:
            raise ValidatorException("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
        else:
            self.db_service.update_patient_status_id(patient_id, status_id=status_id-1)
            self._get_new_status(status_id)

    def discharge(self, patient_id: str) -> None:
        status_id = self.db_service.get_patient_status_id(patient_id)
        if status_id is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")
        else:
            self.db_service.update_patient_status_id(patient_id, status_id=None)
            print("Пациент выписан из больницы")

    def status_up(self, patient_id: str) -> None:
        status_id = self.db_service.get_patient_status_id(patient_id)

        if status_id < PatientStatuses.ready_to_discharge.value:
            self.db_service.update_patient_status_id(patient_id, status_id=status_id+1)
            self._get_new_status(status_id)
        else:
            answer = input("Желаете этого клиента выписать? (да/нет) ").lower()

            if answer == "да":
                self.discharge(patient_id)
            else:
                print(f"Пациент остался в статусе '{patient_statuses[status_id]}'")
