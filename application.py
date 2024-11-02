from hospital_creator import HospitalCreator
from app_exceptions.validators_expection import ValidatorException


class Application:

    def __init__(self, hospital_creator: HospitalCreator):
        self.hospital_creator = hospital_creator
        self.__stop_process = False

        self.commands = {
            "стоп": lambda: self.stop(),
            "stop": lambda: self.stop(),
            "get status": lambda: self.hospital_creator.hospital_command.get_status(),
            "status up": lambda: self.hospital_creator.hospital_command.status_up(),
            "status down": lambda: self.hospital_creator.hospital_command.status_down(),
            "discharge": lambda: self.hospital_creator.hospital_command.discharge(),
            "calculate statistics": lambda: self.hospital_creator.hospital_command.get_statistic(),
        }

    def process(self) -> None:
        input_value = self.hospital_creator.io_helper.request_command()
        command = self.commands.get(input_value)
        if command:
            try:
                command()
            except ValidatorException as error_message:
                print(error_message)
        else:
            self.hospital_creator.io_helper.response_unknown_command()

    def stop(self):
        self.hospital_creator.io_helper.response_finish()
        self.__stop_process = True

    def run(self):
        while not self.__stop_process:
            self.process()
