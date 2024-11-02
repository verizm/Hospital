from enum import Enum


class PatientStatuses(int, Enum):
    hard_sick = 0,
    sick = 1,
    slightly_sick = 2,
    ready_to_discharge = 3


patient_statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}
