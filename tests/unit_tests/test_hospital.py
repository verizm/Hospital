import pytest

from domain.hospital import Hospital
from exceptions.hospital_exception import (
    PatientStatusTooHighError,
)

patient_statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}


class TestHospital:

    def test_get_status(self):
        patient_id = 1
        data_base = [1 for _ in range(200)]
        hospital = Hospital(data_base)

        current_status = data_base[patient_id - 1]
        actual_status = hospital.get_status(patient_id)
        assert actual_status == patient_statuses[current_status]

    def test_status_up(self):
        patient_id = 1
        patient_index = 0
        data_base = [1 for _ in range(200)]
        hospital = Hospital(data_base)

        expected_status = data_base[patient_index] + 1
        hospital.status_up(patient_id)
        actual_status = data_base[patient_index]
        assert actual_status == expected_status

    def test_validate_status_too_high(self):
        patient_id = 1
        data_base = [1 for _ in range(200)]
        hospital = Hospital(data_base)

        data_base[patient_id - 1] = max(patient_statuses)
        with pytest.raises(PatientStatusTooHighError):
            hospital.status_up(patient_id)

    @pytest.mark.parametrize("count_discharged_patients", [0, 1, 199, 200])
    def test_calculate_count_current_patients(self, count_discharged_patients):
        data_base = [1 for _ in range(200)]
        hospital = Hospital(data_base)
        for index in range(count_discharged_patients):
            data_base.pop()
        assert hospital.calculate_count_current_patients() == len(data_base)

    @pytest.mark.parametrize(
        "status_indexes, expected_statistic",
        [
            ([2], {'Болен': 199, 'Слегка болен': 1}),
            ([3], {'Болен': 199, 'Готов к выписке': 1}),
            ([0], {'Болен': 199, 'Тяжело болен': 1}),
            ([1], {'Болен': 200}),
            ([0, 2, 3], {'Болен': 197, 'Готов к выписке': 1, 'Слегка болен': 1, 'Тяжело болен': 1})

        ]
    )
    def test_calculate_statistic_by_patients(self, status_indexes, expected_statistic):
        data_base = [1 for _ in range(200)]
        hospital = Hospital(data_base)
        for patient_index, status in enumerate(status_indexes):
            data_base[patient_index] = status

        statistics = hospital.calculate_statistic_by_patients()
        assert statistics == expected_statistic
