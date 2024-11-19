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


class PatientStatusIsNotExistsError(Exception):
    def __init__(self, statuses: list):
        self.message = f"Ошибка. Статус пациента должен быть один из {statuses}"
        super().__init__(self.message)
