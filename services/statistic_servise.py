from collections import Counter
from services.db_service import DbService
from patient_statuses import patient_statuses


class StatisticService:
    def __init__(self, db_service: DbService):
        self.db_service = db_service

    def _exclude_discharged(self) -> list:
        patients = self.db_service.get_all_patients()
        return list(filter(lambda item: item is not None, patients))

    def _count_statistic(self) -> dict:
        statistic = dict(Counter(self._exclude_discharged()))
        return statistic

    def _count_total(self) -> int:
        return len(self._exclude_discharged())

    def get_statistic(self):
        total = self._count_total()
        statistic = self._count_statistic()
        sorted_statistic = dict(sorted(statistic.items(), key=lambda item: item[0]))

        print(f"В больнице на данный момент находится {total} чел., из них:")
        for status_id, count_patients in sorted_statistic.items():
            print(f"- в статусе '{patient_statuses[status_id]}': {count_patients} чел.")
