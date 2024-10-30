from handlers.abstarct_handler import AbstractHandler
from services.statuse_servise import StatusService
from dto.patient import PatientDto


class PatientStatusHandler(AbstractHandler):
    def handle(self, command: str, patient: PatientDto) -> None:
        status_service = StatusService(patient)
        if command == "узнать статус пациента" or command == "get status":
            status_service.get_status()

        elif command == "повысить статус пациента" or command == "status up":
            status_service.status_up()

        elif command == "понизить статус пациента" or command == "status down":
            status_service.status_down()

        else:
            return super().handle(command, patient)
