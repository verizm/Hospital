from controllers.application import Application
from domain.hospital import Hospital
from controllers.io_helper import IOHelper
from domain.hospital_commands import HospitalCommands

if __name__ == '__main__':
    data_base = [1 for _ in range(200)]
    hospital = Hospital(data_base)
    io_helper = IOHelper()
    hospital_command = HospitalCommands(hospital, io_helper)
    app = Application(hospital_command, io_helper)
    app.run()

