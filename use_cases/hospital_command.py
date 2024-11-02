from infrastructure.io_helper import IOHelper
from entity.hospital import Hospital


class HospitalCommand:
    def __init__(self, hospital: Hospital, io_helper: IOHelper):
        self.hospital = hospital
        self.io_helper = io_helper

    def get_statistic(self):
        total_count = self.hospital.get_count_current_patients()
        statistics = self.hospital.get_statistic_by_patients()
        self.io_helper.response_statistic(total_count, statistics)

    def get_status(self) -> None:
        patient_id = self.io_helper.request_patient_id()
        status = self.hospital.get_status(patient_id)
        self.io_helper.response_status(status)

    def status_down(self) -> None:
        patient_id = self.io_helper.request_patient_id()

        if self.hospital.can_status_down(patient_id):
            self.hospital.status_down(patient_id)
            status = self.hospital.get_status(patient_id)
            self.io_helper.response_new_status(status)
        else:
            self.io_helper.response_status_too_low()

    def discharge(self) -> None:
        patient_id = self.io_helper.request_patient_id()
        self.hospital.discharge(patient_id)
        self.io_helper.response_patient_discharged()

    def status_up(self) -> None:
        patient_id = self.io_helper.request_patient_id()

        if self.hospital.can_status_up(patient_id):
            self.hospital.status_up(patient_id)
            status = self.hospital.get_status(patient_id)
            self.io_helper.response_new_status(status)
        else:
            if self.io_helper.request_need_to_discharge():
                self.hospital.discharge(patient_id)
                self.io_helper.response_patient_discharged()
            else:
                status = self.hospital.get_status(patient_id)
                self.io_helper.response_status_not_changed(status)
