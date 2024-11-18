class PatientIsNotExistsError(Exception):
    def __init__(self):
        self.message = "Ошибка. В больнице нет пациента с таким ID"
        super().__init__()


class PatientIdIsNotPositiveIntegerError(Exception):
    def __init__(self):
        self.message = "Ошибка. ID пациента должно быть числом (целым, положительным)"
        super().__init__()


class PatientStatusTooLowError(Exception):
    def __init__(self):
        self.message = "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)"
        super().__init__(self.message)


class PatientStatusTooHighError(Exception):
    def __init__(self):
        self.message = "Ошибка. Нельзя понизить самый высокий статус"
        super().__init__(self.message)


class PatientStatusNotAllowedForHospitalizationError(Exception):
    def __init__(self):
        self.message = "Ошибка. Нельзя госпитализировать пациента с таким статусом."
        super().__init__(self.message)
