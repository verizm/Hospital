from handlers.abstarct_handler import AbstractHandler
from services.discharge_service import DischargeService
from app_commands import CommandsRu, CommandsEng
from dto.patient import PatientDto


class DischargePatientHandler(AbstractHandler):
    def handle(self, command: str, patient: PatientDto) -> None:
        if command == CommandsRu.discharge.value or command == CommandsEng.discharge.value:
            discharge_service = DischargeService(patient)
            discharge_service.discharge()
        else:
            return super().handle(command, patient)
