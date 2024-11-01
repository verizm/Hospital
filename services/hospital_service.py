from collections import Counter
from patient_statuses import patient_statuses
from patient_statuses import PatientStatuses
from app_exceptions.validators_expection import ValidatorException


class HospitalService:
    def __init__(self, hospital_db: list):
        self.hospital_db = hospital_db

    def _request_patient_id(self) -> str:
        patient_id = input(f"Введите ID пациента: ").strip()
        if not patient_id.isdigit() or int(patient_id) <= 0:
            raise ValidatorException("Ошибка. ID пациента должно быть числом (целым, положительным)")

        patient_index = int(patient_id) - 1
        if len(self.hospital_db) <= int(patient_index) or self.hospital_db[patient_index] is None:
            raise ValidatorException("Ошибка. В больнице нет пациента с таким ID")

        return patient_id

    def _get_status_id(self, patient_id: str) -> int:
        patient_index = int(patient_id) - 1
        status_id = self.hospital_db[patient_index]
        return status_id

    def _update_status(self, patient_id: str, status_id: int | None) -> None:
        patient_index = int(patient_id) - 1
        self.hospital_db[patient_index] = status_id

    @staticmethod
    def _get_new_status(status_id: int) -> None:
        print(f"Новый статус пациента: {patient_statuses[status_id]}")

    def get_statistic(self):
        exclude_discharged_statuses = list(filter(lambda item: item is not None, self.hospital_db))
        total = len(exclude_discharged_statuses)
        statistic = dict(Counter(exclude_discharged_statuses))
        sorted_statistic = dict(sorted(statistic.items(), key=lambda item: item[0]))

        print(f"В больнице на данный момент находится {total} чел., из них:")
        for status_id, count_patients in sorted_statistic.items():
            print(f"- в статусе '{patient_statuses[status_id]}': {count_patients} чел.")

    def get_status(self) -> None:
        patient_id = self._request_patient_id()
        status_id = self._get_status_id(patient_id)
        print(f"Cтатус пациента: {patient_statuses[status_id]}")

    def status_down(self) -> None:
        patient_id = self._request_patient_id()
        status_id = self._get_status_id(patient_id)
        if status_id == PatientStatuses.hard_sick.value:
            raise ValidatorException("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")
        else:
            status_id -= 1
            self._update_status(patient_id, status_id)
            self._get_new_status(status_id)

    def discharge(self) -> None:
        patient_id = self._request_patient_id()
        self._update_status(patient_id, status_id=None)
        print("Пациент выписан из больницы")

    def status_up(self) -> None:
        patient_id = self._request_patient_id()
        status_id = self._get_status_id(patient_id)

        if status_id < PatientStatuses.ready_to_discharge.value:
            status_id += 1
            self._update_status(patient_id, status_id)
            self._get_new_status(status_id)
        else:
            answer = input("Желаете этого клиента выписать? (да/нет) ").lower()

            if answer == "да":
                self._update_status(patient_id, status_id=None)
                print("Пациент выписан из больницы")
            else:
                print(f"Пациент остался в статусе '{patient_statuses[status_id]}'")
