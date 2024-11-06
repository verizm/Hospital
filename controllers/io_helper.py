from exceptions.hospital_exception import PatientIdIsNotPositiveIntegerError
from app_commands import (
    CommandsRu,
    CommandsEng,
    UnknownCommand,
)


class IOHelper:
    COMMANDS = [*CommandsEng.values(), *CommandsRu.values()]

    @staticmethod
    def request_command():
        command = input(f"Введите команду: ").strip()
        if command not in IOHelper.COMMANDS:
            command = UnknownCommand
        return command

    @staticmethod
    def request_patient_id() -> int:
        patient_id = input(f"Введите ID пациента: ").strip()
        if not patient_id.isdigit() or int(patient_id) <= 0:
            raise PatientIdIsNotPositiveIntegerError
        return int(patient_id)

    @staticmethod
    def report_message(message: str):
        print(message)

    @staticmethod
    def request_need_to_discharge() -> bool:
        answer_text = input("Желаете этого клиента выписать? (да/нет) ").lower()
        return answer_text == "да"

    @staticmethod
    def report_patient_not_exists():
        print("Ошибка. В больнице нет пациента с таким ID")

    @staticmethod
    def report_status(status: str):
        print(f"Cтатус пациента: {status}")

    @staticmethod
    def report_new_status(status: str):
        print(f"Новый статус пациента: {status}")

    @staticmethod
    def report_status_not_changed(status: str):
        print(f"Пациент остался в статусе '{status}'")

    @staticmethod
    def report_status_too_low():
        print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    @staticmethod
    def report_patient_discharged():
        print("Пациент выписан из больницы")

    @staticmethod
    def report_unknown_command():
        print("Неизвестная команда! Попробуйте ещё раз")

    @staticmethod
    def report_stop_app():
        print("Сеанс завершён.")

    @staticmethod
    def report_statistic(total: int, statistic: dict):
        print(f"В больнице на данный момент находится {total} чел., из них:")
        for status, count_patients in statistic.items():
            print(f"- в статусе '{status}': {count_patients} чел.")
