from controllers.application import Application
from controllers.io_helper import IOHelper
from domain.hospital import Hospital
from domain.hospital_commands import HospitalCommands


def get_actual_hospital_db_as_statuses_list(hospital):
    return hospital._hospital_db


def make_hospital(hospital_db: list):
    return Hospital(hospital_db, {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"})


def make_application(hospital, console_mock):
    io_helper = IOHelper(console_mock)
    hospital_command = HospitalCommands(hospital, io_helper)
    return Application(hospital_command, io_helper)
