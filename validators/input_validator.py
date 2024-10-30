
from app_commands import (
    CommandsEng,
    CommandsRu,
)
from app_exceptions.validators_expection import ValidatorException


class InputValidator:
    COMMANDS = [*CommandsEng.values(), *CommandsRu.values()]

    @staticmethod
    def check_command(command: str) -> None:
        if command not in InputValidator.COMMANDS:
            raise ValidatorException("Неизвестная команда! Попробуйте ещё раз")

    @staticmethod
    def check_patient_id(patient_id: str):
        if not patient_id.isdigit() or int(patient_id) <= 0:
            raise ValidatorException("Ошибка. ID пациента должно быть числом (целым, положительным)")
