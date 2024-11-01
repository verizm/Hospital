from services.db_service import DbService
from services.hospital_service import HospitalService
from handlers.hospital_handler import HospitalHandler
from app_exceptions.validators_expection import ValidatorException
from validators.input_validator import InputValidator
from app_commands import (
    CommandsRu,
    CommandsEng,
)

input_validator = InputValidator()
db_service = DbService()
hospital_service = HospitalService(db_service)
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


def generate_data_base() -> list:
    return [1 for _ in range(200)]


if __name__ == '__main__':
    stop_process = False
    data_base = generate_data_base()
    db_service.set_db(data_base)

    while not stop_process:
        main_process()
