from patient_statuses import patient_statuses


class PatientDto:
    def __init__(self, status_id: int, patient_id: int):
        self.__status = status_id
        self.__patient_id = patient_id
        self.changed = False

    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value=None):
        self.__patient_id = value
        if not self.changed:
            self.changed = True

    @property
    def status_id(self):
        return self.__status

    @status_id.setter
    def status_id(self, new_status: int):
        self.__status = new_status
        if not self.changed:
            self.changed = True

    @property
    def status_value(self):
        return patient_statuses[self.__status]
