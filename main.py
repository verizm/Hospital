from controllers.application import Application
from controllers.console import Console
from domain.hospital import Hospital
from controllers.io_helper import IOHelper
from domain.hospital_commands import HospitalCommands

if __name__ == '__main__':
    data_base = [1 for _ in range(200)]
    patient_statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    hospital = Hospital(data_base, patient_statuses)
    io_helper = IOHelper(Console())
    hospital_command = HospitalCommands(hospital, io_helper)
    app = Application(hospital_command, io_helper)

    app.run()

