from services.hospital_service import HospitalService
from app_commands import (
    CommandsRu,
    CommandsEng,
)


class HospitalHandler:

    def __init__(self, hospital_service: HospitalService):
        self.hospital_service = hospital_service

    def map_command(self, command: str):
        if command == CommandsRu.calculate_statistics.value or command == CommandsEng.calculate_statistics.value:
            self.hospital_service.get_statistic()

        if command == CommandsRu.discharge.value or command == CommandsEng.discharge.value:
            self.hospital_service.discharge()

        if command == CommandsRu.get_status.value or command == CommandsEng.get_status.value:
            self.hospital_service.get_status()

        if command == CommandsRu.status_up.value or command == CommandsEng.status_up.value:
            self.hospital_service.status_up()

        if command == CommandsRu.status_down.value or command == CommandsEng.status_down.value:
            self.hospital_service.status_down()
