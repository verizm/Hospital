from hospital_creator import HospitalCreator
from app_exceptions.validators_expection import ValidatorException
from hospital_data.app_commands import (
    UnknownCommand,
    CommandsEng,
    CommandsRu,
)


class Application:
    def __init__(self, hospital_creator: HospitalCreator):
        self.hospital_creator = hospital_creator
        self.__stop_process = False

    def process(self) -> None:
        command = self.hospital_creator.io_helper.request_command()
        if command == UnknownCommand:
            self.hospital_creator.io_helper.response_unknown_command()

        elif command == CommandsEng.stop.value or command == CommandsRu.stop.value:
            self.stop()

        else:
            try:
                self.hospital_creator.hospital_handler.map_command(command)
            except ValidatorException as error_message:
                self.hospital_creator.io_helper.response_message(error_message)

    def stop(self):
        self.hospital_creator.io_helper.response_stop_app()
        self.__stop_process = True

    def run(self):
        while not self.__stop_process:
            self.process()
