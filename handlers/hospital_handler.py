from services.statistic_servise import StatisticService
from validators.input_validator import InputValidator

from services.statuse_servise import StatusService
from services.discharge_service import DischargeService
from app_commands import (
    CommandsRu,
    CommandsEng,
)

input_validator = InputValidator()


class HospitalHandler:

    def __init__(self, db_service):
        self.db_service = db_service

    def map_command(self, command: str):
        if command == CommandsRu.calculate_statistics.value or command == CommandsEng.calculate_statistics.value:
            StatisticService(self.db_service).get_statistic()

        if command == CommandsRu.discharge.value or command == CommandsEng.discharge.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            DischargeService(patient_id, self.db_service).discharge()

        if command == CommandsRu.get_status.value or command == CommandsEng.get_status.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            StatusService(patient_id, self.db_service).get_status()

        if command == CommandsRu.status_up.value or command == CommandsEng.status_up.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            StatusService(patient_id, self.db_service).status_up()

        if command == CommandsRu.status_down.value or command == CommandsEng.status_down.value:
            patient_id = input(f"Введите ID пациента: ").strip()
            input_validator.check_patient_id(patient_id)
            StatusService(patient_id, self.db_service).status_down()
