from handlers.abstarct_handler import AbstractHandler
from services.statuse_servise import StatusService
from services.discharge_service import DischargeService
from app_commands import CommandsRu, CommandsEng
from dto.patient import PatientDto


class PatientStatusHandler(AbstractHandler):
    def handle(self, command: str, patient: PatientDto) -> None:
        status_service = StatusService(patient)
        if command == CommandsRu.get_status.value or command == CommandsEng.get_status.value:
            status_service.get_status()

        elif command == CommandsRu.status_up.value or command == CommandsEng.status_up.value:
            need_to_discharge = status_service.status_up()
            if need_to_discharge:
                DischargeService(patient).discharge()

        elif command == CommandsRu.status_down.value or command == CommandsEng.status_down.value:
            status_service.status_down()

        else:
            return super().handle(command, patient)
