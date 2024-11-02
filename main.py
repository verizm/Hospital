from application import Application
from hospital_creator import HospitalCreator

if __name__ == '__main__':
    data_base = [1 for _ in range(200)]
    hospital = HospitalCreator(data_base)
    app = Application(hospital)
    app.run()

