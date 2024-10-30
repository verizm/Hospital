from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda item: item.value, cls))


class CommandsRu(ExtendedEnum):
    get_status = "узнать статус пациента"
    status_up = "повысить статус пациента"
    status_down = "понизить статус пациента"
    discharge = "выписать пациента"
    calculate_statistics = "рассчитать статистику"
    stop = "стоп"


class CommandsEng(ExtendedEnum):
    get_status = "get status"
    status_up = "status up"
    status_down = "status down"
    discharge = "discharge"
    calculate_statistics = "calculate statistics"
    stop = "stop"
