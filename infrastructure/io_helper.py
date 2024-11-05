from exceptions.hospital_exception import UserIdIsNotPositiveIntegerException
from hospital_data.app_commands import (
    CommandsRu,
    CommandsEng,
    UnknownCommand,
)
from hospital_data.patient_statuses import patient_statuses


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
            raise UserIdIsNotPositiveIntegerException
        return int(patient_id)

    @staticmethod
    def response_message(message: str) -> None:
        print(message)

    @staticmethod
    def request_need_to_discharge() -> bool:
        answer_text = input("Желаете этого клиента выписать? (да/нет) ").lower()
        return answer_text == "да"

    @staticmethod
    def response_patient_not_exists() -> None:
        print("Ошибка. В больнице нет пациента с таким ID")

    @staticmethod
    def response_status(status: str) -> None:
        print(f"Cтатус пациента: {status}")

    @staticmethod
    def response_new_status(status: str) -> None:
        print(f"Новый статус пациента: {status}")

    @staticmethod
    def response_status_not_changed(status: str) -> None:
        print(f"Пациент остался в статусе '{status}'")

    @staticmethod
    def response_status_too_low() -> None:
        print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    @staticmethod
    def response_patient_discharged() -> None:
        print("Пациент выписан из больницы")

    @staticmethod
    def response_unknown_command() -> None:
        print("Неизвестная команда! Попробуйте ещё раз")

    @staticmethod
    def response_stop_app() -> None:
        print("Сеанс завершён.")

    @staticmethod
    def response_statistic(total: int, sorted_statistic: dict) -> None:
        print(f"В больнице на данный момент находится {total} чел., из них:")
        for status_id, count_patients in sorted_statistic.items():
            print(f"- в статусе '{patient_statuses[status_id]}': {count_patients} чел.")
