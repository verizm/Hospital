from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda item: item.value, cls))


class CommandsRu(ExtendedEnum):
    GET_STATUS = "узнать статус пациента"
    STATUS_UP = "повысить статус пациента"
    STATUS_DOWN = "понизить статус пациента"
    DISCHARGE = "выписать пациента"
    CALCULATE_STATISTIC = "рассчитать статистику"
    STOP = "стоп"


class CommandsEng(ExtendedEnum):
    GET_STATUS = "get status"
    STATUS_UP = "status up"
    STATUS_DOWN = "status down"
    DISCHARGE = "discharge"
    CALCULATE_STATISTIC = "calculate statistics"
    STOP = "stop"
