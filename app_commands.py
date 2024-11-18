from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def values(cls):
        return list(map(lambda item: item.value, cls))


UnknownCommand = "unknown"


class CommandsRu(ExtendedEnum):
    get_status = "узнать статус пациента"
    status_up = "повысить статус пациента"
    status_down = "понизить статус пациента"
    discharge = "выписать пациента"
    calculate_statistics = "рассчитать статистику"
    add_patient = "добавить пациента"
    stop = "стоп"


class CommandsEng(ExtendedEnum):
    get_status = "get status"
    status_up = "status up"
    status_down = "status down"
    discharge = "discharge"
    calculate_statistics = "calculate statistics"
    add_patient = "add patient"
    stop = "stop"
