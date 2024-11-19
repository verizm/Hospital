import pytest

from domain.hospital import Hospital
from tests.hospital_helper import (
    make_hospital,
    get_actual_hospital_db_as_statuses_list,
)
from exceptions.hospital_exception import (
    PatientStatusTooHighError,
    PatientIsNotExistsError,
    PatientStatusIsNotExistsError,
)


class TestHospital:

    def test_get_status(self):
        hospital = make_hospital([2, 0])
        assert hospital.get_status(patient_id=1) == "Слегка болен"

    def test_get_status_when_patient_discharged(self):
        hospital = make_hospital([None, 0])
        with pytest.raises(PatientIsNotExistsError):
            hospital.get_status(patient_id=1)

    def test_get_status_when_patient_not_exists(self):
        hospital = make_hospital([2, 2, 1])
        with pytest.raises(PatientIsNotExistsError):
            hospital.get_status(patient_id=4)

    def test_status_up(self):
        hospital = Hospital([10, 30], {10: "Тяжело болен", 20: "Болен", 30: "Слегка болен"})

        hospital.status_up(patient_id=1)
        assert hospital._hospital_db == [20, 30]

    def test_status_up_when_status_too_high(self):
        hospital = make_hospital([3, 2])

        with pytest.raises(PatientStatusTooHighError):
            hospital.status_up(patient_id=1)

        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 2]

    def test_calculate_count_current_patients(self):
        hospital = make_hospital([None, 1, None, 0, 1, None])
        assert hospital.calculate_count_current_patients() == 3

    def test_calculate_statistic_by_patients(self):
        hospital = make_hospital([None, 3, 0, 3, 2, 0])
        expected_statistic = {"Тяжело болен": 2, "Слегка болен": 1, "Готов к выписке": 2}
        assert hospital.calculate_statistic_by_patients() == expected_statistic

    def test_calculate_statistic_by_patients_when_db_is_empty(self):
        hospital = make_hospital([])
        assert hospital.calculate_statistic_by_patients() == {}

    def test_add_patient(self):
        hospital = make_hospital([3, 2, None])

        patient_id = hospital.add_patient("Тяжело болен")

        assert patient_id == 4
        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 2, None, 0]

    def test_add_patient_when_status_is_not_exists(self):
        hospital = make_hospital([2, 2, 1])

        with pytest.raises(PatientStatusIsNotExistsError):
            hospital.add_patient(status="Здоров")
        assert get_actual_hospital_db_as_statuses_list(hospital) == [2, 2, 1]

    def test_convert_status_value_to_status_id(self):
        hospital = make_hospital([2, 2, 1])

        status_id = hospital._convert_status_value_to_status_id("Болен")

        assert status_id == 1

    def test_convert_status_value_to_status_id_when_status_is_not_exists(self):
        hospital = make_hospital([])

        with pytest.raises(PatientStatusIsNotExistsError):
            hospital._convert_status_value_to_status_id(status="Sick")

    def test_calculate_new_patient_id(self):
        hospital = make_hospital([2, 2, 1])

        assert hospital._calculate_new_patient_id() == 4
