from validators.input_validator import InputValidator
from services.hospital_service import HospitalService
from app_commands import (
    CommandsRu,
    CommandsEng,
)

input_validator = InputValidator()


class HospitalHandler:

    def __init__(self, hospital_service: HospitalService):
        self.hospital_service = hospital_service

    def map_command(self, command: str):
        if command == CommandsRu.calculate_statistics.value or command == CommandsEng.calculate_statistics.value:
            self.hospital_service.get_statistic()

        if command == CommandsRu.discharge.value or command == CommandsEng.discharge.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            self.hospital_service.discharge(patient_id)

        if command == CommandsRu.get_status.value or command == CommandsEng.get_status.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            self.hospital_service.get_status(patient_id)

        if command == CommandsRu.status_up.value or command == CommandsEng.status_up.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            self.hospital_service.status_up(patient_id)

        if command == CommandsRu.status_down.value or command == CommandsEng.status_down.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            self.hospital_service.status_down(patient_id)
