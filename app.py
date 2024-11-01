from services.hospital_service import HospitalService
from handlers.hospital_handler import HospitalHandler
from app_exceptions.validators_expection import ValidatorException
from validators.input_validator import InputValidator
from app_commands import (
    CommandsRu,
    CommandsEng,
)


def generate_data_base() -> list:
    return [1 for _ in range(200)]


input_validator = InputValidator()
data_base = generate_data_base()
hospital_service = HospitalService(data_base)
hospital_handler = HospitalHandler(hospital_service)


def main_process() -> None:
    global stop_process
    command = input(f"Введите команду: ").strip()
    if command == CommandsRu.stop.value or command == CommandsEng.stop.value:
        print("Сеанс завершён.")
        stop_process = True
    try:
        input_validator.check_command(command)
        hospital_handler.map_command(command)
    except ValidatorException as error_message:
        print(error_message)


if __name__ == '__main__':
    stop_process = False
    while not stop_process:
        main_process()
