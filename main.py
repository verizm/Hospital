from application import Application
from entity.hospital import Hospital
from infrastructure.io_helper import IOHelper
from use_cases.hospital_command import HospitalCommands

if __name__ == '__main__':
    data_base = [1 for _ in range(200)]
    hospital = Hospital(data_base)
    io_helper = IOHelper()
    hospital_command = HospitalCommands(hospital, io_helper)
    app = Application(hospital_command, io_helper)
    app.run()

