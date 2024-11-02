from use_cases.hospital_command import HospitalCommand
from entity.hospital import Hospital
from infrastructure.io_helper import IOHelper
from infrastructure.hospital_handler import HospitalHandler


class HospitalCreator:
    def __init__(self, data_base: list):
        self.data_base = data_base
        self.hospital = Hospital(self.data_base)
        self.io_helper = IOHelper()
        self.hospital_command = HospitalCommand(self.hospital, self.io_helper)
        self.hospital_handler = HospitalHandler(self.hospital_command)
