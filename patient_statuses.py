from enum import Enum


class StatusesBoundaryValues(int, Enum):
    HARD_SICK = 0,
    READY_TO_DISCHARGE = 3


STATUSES = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}
