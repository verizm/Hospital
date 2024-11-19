from exceptions.hospital_exception import PatientIdIsNotPositiveIntegerError
from app_commands import (
    CommandsRu,
    CommandsEng,
    UnknownCommand,
)


class IOHelper:
    _COMMANDS = [*CommandsEng.values(), *CommandsRu.values()]

    def __init__(self, console):
        self._console = console

    def request_command(self) -> str:
        command = self._console.input(f"Введите команду: ").strip()
        if command not in IOHelper._COMMANDS:
            command = UnknownCommand
        return command

    def request_patient_id(self) -> int:
        patient_id = self._console.input(f"Введите ID пациента: ").strip()
        if not patient_id.isdigit() or int(patient_id) <= 0:
            raise PatientIdIsNotPositiveIntegerError
        return int(patient_id)

    def report_message(self, message: str):
        self._console.print(message)

    def request_need_to_discharge(self) -> bool:
        answer_text = self._console.input("Желаете этого клиента выписать? (да/нет) ").lower()
        return answer_text == "да"

    def report_patient_not_exists(self):
        self._console.print("Ошибка. В больнице нет пациента с таким ID")

    def report_status(self, status: str):
        self._console.print(f"Cтатус пациента: {status}")

    def report_new_status(self, status: str):
        self._console.print(f"Новый статус пациента: {status}")

    def report_status_not_changed(self, status: str):
        self._console.print(f"Пациент остался в статусе '{status}'")

    def report_status_too_low(self):
        self._console.print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    def report_patient_discharged(self):
        self._console.print("Пациент выписан из больницы")

    def report_unknown_command(self):
        self._console.print("Неизвестная команда! Попробуйте ещё раз")

    def report_stop_app(self):
        self._console.print("Сеанс завершён.")

    def report_statistic(self, total: int, statistic: dict):
        self._console.print(f"В больнице на данный момент находится {total} чел., из них:")
        for status, count_patients in statistic.items():
            self._console.print(f"- в статусе '{status}': {count_patients} чел.")

    def request_patient_status(self) -> str:
        status = self._console.input("Введите статус пациента: ").strip()
        return status

    def report_patient_id(self, patient_id: int):
        self._console.print(f"Пациент госпитализирован. Присвоен ID {patient_id}")
