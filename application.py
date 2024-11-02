from hospital_creator import HospitalCreator
from app_exceptions.validators_expection import ValidatorException
from hospital_data.app_commands import (
    CommandsRu,
    CommandsEng,
)


class Application:
    def __init__(self, hospital_items: HospitalCreator):
        self.hospital_items = hospital_items
        self.__stop_process = False

    def process(self) -> None:
        command = ""
        try:
            command = self.hospital_items.io_helper.request_command()
        except ValidatorException as error_message:
            print(error_message)

        if command == CommandsRu.stop.value or command == CommandsEng.stop.value:
            self.stop()
        try:
            self.hospital_items.hospital_handler.map_command(command)
        except ValidatorException as error_message:
            print(error_message)

    def stop(self):
        print("Сеанс завершён.")
        self.__stop_process = True

    def run(self):
        while not self.__stop_process:
            self.process()
