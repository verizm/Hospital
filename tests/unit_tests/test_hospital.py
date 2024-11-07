import pytest

from domain.hospital import Hospital
from exceptions.hospital_exception import (
    PatientStatusTooHighError,
    PatientIsNotExistsError,
)

patient_statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}


class TestHospital:

    def test_get_status(self):
        hospital = Hospital([2, 0])
        assert hospital.get_status(patient_id=1) == "Слегка болен"

    def test_status_up(self):
        hospital = Hospital([2, 0])
        hospital.status_up(patient_id=1)
        assert hospital._hospital_db == [3, 0]

    def test_validate_status_too_high(self):
        hospital = Hospital([3])
        with pytest.raises(PatientStatusTooHighError):
            hospital.status_up(patient_id=1)

    def test_validate_discharged_patients_when_get_status(self):
        hospital = Hospital([None])
        with pytest.raises(PatientIsNotExistsError):
            hospital.get_status(patient_id=1)

    def test_validate_patient_not_exists_when_get_status(self):
        hospital = Hospital([])
        with pytest.raises(PatientIsNotExistsError):
            hospital.get_status(patient_id=1)

    def test_calculate_count_current_patients(self):
        hospital = Hospital([None, 1, 0])
        assert hospital.calculate_count_current_patients() == 2

    def test_statistic_by_patients(self):
        hospital = Hospital([None, 3, 3, 0])
        assert hospital.calculate_statistic_by_patients() == {"Тяжело болен": 1, "Готов к выписке": 2}

    def test_statistic_by_patients_sorted(self):
        hospital = Hospital([3, 0, 2, 1])
        expected_statistic = {"Тяжело болен": 1, "Болен": 1, "Слегка болен": 1, "Готов к выписке": 1}
        assert hospital.calculate_statistic_by_patients() == expected_statistic

    def test_statistic_by_patients_exclude_discharged(self):
        hospital = Hospital([None, None])
        assert hospital.calculate_statistic_by_patients() == {}
