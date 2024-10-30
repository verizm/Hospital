from handlers.abstarct_handler import AbstractHandler
from services.discharge_service import DischargeService
from dto.patient import PatientDto


class DischargePatientHandler(AbstractHandler):
    def handle(self, command: str, patient: PatientDto) -> PatientDto:
        if command == "выписать пациента" or command == "discharge":
            return DischargeService(patient).discharge()
        else:
            return super().handle(command, patient)
