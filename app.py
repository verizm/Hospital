from handlers.patient_status_handler import PatientStatusHandler
from handlers.discharge_patient_handler import DischargePatientHandler
from services.db_service import DbService
from services.statistic_servise import StatisticService
from app_exceptions.validators_expection import ValidatorException
from validators.input_validator import InputValidator


status_handler = PatientStatusHandler()
discharge_handler = DischargePatientHandler()

input_validator = InputValidator()

db_service = DbService()
statistics_service = StatisticService(db_service)

status_handler.set_next(discharge_handler)


def main_process() -> bool:
    command = input(f"Введите команду: ").strip()
    try:
        input_validator.check_command(command)
    except ValidatorException as error_message:
        print(error_message)
        return True

    if command == "стоп" or command == "stop":
        print("Сеанс завершён.")
        return False
    if command == "рассчитать статистику" or command == "calculate statistics":
        statistics_service.get_statistic()
        return True

    patient_id = input(f"Введите ID пациента: ").strip()
    try:
        input_validator.check_patient_id(patient_id)
    except ValidatorException as error_message:
        print(error_message)
        return True

    try:
        patient_id = int(patient_id) - 1
        patient_dto = db_service.get_patient_by_id(patient_id)
        print(db_service.data_base)
        status_handler.handle(command, patient_dto)
        if patient_dto.changed:
            db_service.update_patient(patient_dto)
            print(db_service.data_base)
    except ValidatorException as error_message:
        print(error_message)
        return True

    return True


def generate_data_base() -> list:
    return [2 for _ in range(200)]


if __name__ == '__main__':
    result = True
    data_base = generate_data_base()
    db_service.set_db(data_base)

    while result:
        result = main_process()
