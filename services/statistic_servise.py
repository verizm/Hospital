from services.db_service import DbService
from patient_statuses import STATUSES


class StatisticService:
    def __init__(self, db_service: DbService):
        self.db_service = db_service

    def get_total(self):
        return self.db_service.get_total_patient_count()

    def get_statistic(self):
        print(f"В больнице на данный момент находится {self.get_total()} чел., из них:")
        for status_id, count_patients in self.db_service.get_statistic_by_patient().items():
            print(f"- в статусе '{STATUSES[status_id]}': {count_patients} чел.")
