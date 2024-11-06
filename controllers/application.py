from domain.hospital_commands import HospitalCommands
from app_commands import (
    UnknownCommand,
    CommandsEng,
    CommandsRu,
)


class Application:
    def __init__(self, hospital_commands: HospitalCommands, io_helper):
        self._hospital_commands = hospital_commands
        self._io_helper = io_helper
        self._stop_process = False

    def _process(self):
        command = self._io_helper.request_command()

        if command == UnknownCommand:
            self._io_helper.report_unknown_command()

        if command == CommandsEng.stop.value or command == CommandsRu.stop.value:
            self._stop()

        if command == CommandsRu.calculate_statistics.value or command == CommandsEng.calculate_statistics.value:
            self._hospital_commands.get_statistic()

        if command == CommandsRu.discharge.value or command == CommandsEng.discharge.value:
            self._hospital_commands.discharge()

        if command == CommandsRu.get_status.value or command == CommandsEng.get_status.value:
            self._hospital_commands.get_status()

        if command == CommandsRu.status_up.value or command == CommandsEng.status_up.value:
            self._hospital_commands.status_up()

        if command == CommandsRu.status_down.value or command == CommandsEng.status_down.value:
            self._hospital_commands.status_down()

    def _stop(self):
        self._io_helper.report_stop_app()
        self._stop_process = True

    def run(self):
        while not self._stop_process:
            self._process()
