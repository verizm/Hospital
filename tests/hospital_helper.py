from domain.hospital import Hospital


def get_actual_hospital_db_as_statuses_list(hospital):
    return hospital._hospital_db


def make_hospital(hospital_db: list):
    return Hospital(hospital_db, {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"})
