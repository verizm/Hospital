from exceptions.hospital_exception import (
    PatientIsNotExistsError,
    PatientIdIsNotPositiveIntegerError,
    PatientStatusNotAllowedForHospitalizationError
)


class HospitalCommands:
    def __init__(self, hospital, io_helper):
        self._hospital = hospital
        self._io_helper = io_helper

    def get_statistic(self):
        total_count = self._hospital.calculate_count_current_patients()
        statistics = self._hospital.calculate_statistic_by_patients()
        self._io_helper.report_statistic(total_count, statistics)

    def get_status(self):
        try:
            patient_id = self._io_helper.request_patient_id()
            status = self._hospital.get_status(patient_id)
            self._io_helper.report_status(status)

        except (PatientIdIsNotPositiveIntegerError, PatientIsNotExistsError) as error:
            self._io_helper.report_message(error.message)

    def status_down(self) -> None:
        try:
            patient_id = self._io_helper.request_patient_id()

            if self._hospital.can_status_down(patient_id):
                self._hospital.status_down(patient_id)
                status = self._hospital.get_status(patient_id)
                self._io_helper.report_new_status(status)
            else:
                self._io_helper.report_status_too_low()
        except (PatientIdIsNotPositiveIntegerError, PatientIsNotExistsError) as error:
            self._io_helper.report_message(error.message)

    def discharge(self):
        try:
            patient_id = self._io_helper.request_patient_id()
            self._hospital.discharge(patient_id)
            self._io_helper.report_patient_discharged()

        except (PatientIdIsNotPositiveIntegerError, PatientIsNotExistsError) as error:
            self._io_helper.report_message(error.message)

    def status_up(self):
        try:
            patient_id = self._io_helper.request_patient_id()

            if self._hospital.can_status_up(patient_id):
                self._hospital.status_up(patient_id)
                status = self._hospital.get_status(patient_id)
                self._io_helper.report_new_status(status)
            else:
                if self._io_helper.request_need_to_discharge():
                    self._hospital.discharge(patient_id)
                    self._io_helper.report_patient_discharged()
                else:
                    status = self._hospital.get_status(patient_id)
                    self._io_helper.report_status_not_changed(status)

        except (PatientIdIsNotPositiveIntegerError, PatientIsNotExistsError) as error:
            self._io_helper.report_message(error.message)

    def add_patient(self):
        try:
            status = self._io_helper.request_patient_status()
            patient_id = self._hospital.add_patient(status)
            self._io_helper.report_patient_id(patient_id)
        except PatientStatusNotAllowedForHospitalizationError as error:
            self._io_helper.report_message(error.message)
