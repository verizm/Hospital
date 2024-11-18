from unittest.mock import (
    MagicMock,
    call,
)

from tests.hospital_helper import (
    get_actual_hospital_db_as_statuses_list,
    make_hospital,
    make_application,
)


class TestApplication:

    def test_get_status(self):
        console_mock = MagicMock()
        console_mock.input.side_effect = ["get status", "1", "стоп"]
        make_application(make_hospital([0, 3, 2]), console_mock).run()

        console_mock.assert_has_calls(
            [
                call.input("Введите команду: "),
                call.input("Введите ID пациента: "),
                call.print("Cтатус пациента: Тяжело болен"),
                call.input("Введите команду: "),
                call.print("Сеанс завершён."),
            ]
        )

    def test_status_up(self):
        console_mock = MagicMock()
        console_mock.input.side_effect = ["status up", "1", "стоп"]

        hospital = make_hospital([0, 3, 2])
        make_application(hospital, console_mock).run()

        console_mock.assert_has_calls(
            [
                call.input("Введите команду: "),
                call.input("Введите ID пациента: "),
                call.print("Новый статус пациента: Болен"),
                call.input("Введите команду: "),
                call.print("Сеанс завершён."),
            ]
        )
        assert get_actual_hospital_db_as_statuses_list(hospital) == [1, 3, 2]

    def test_status_up_when_status_too_high_and_patient_discharged(self):
        console_mock = MagicMock()
        console_mock.input.side_effect = ["status up", "1", "ДА", "stop"]

        hospital = make_hospital([3, 1])
        make_application(hospital, console_mock).run()

        console_mock.assert_has_calls(
            [
                call.input("Введите команду: "),
                call.input("Введите ID пациента: "),
                call.input("Желаете этого клиента выписать? (да/нет) "),
                call.print("Пациент выписан из больницы"),
                call.input("Введите команду: "),
                call.print("Сеанс завершён."),
            ]
        )
        assert get_actual_hospital_db_as_statuses_list(hospital) == [None, 1]

    def test_status_up_when_status_too_high_and_patient_not_discharged(self):
        console_mock = MagicMock()
        console_mock.input.side_effect = ["status up", "1", "net", "stop"]

        hospital = make_hospital([3, 1])
        make_application(hospital, console_mock).run()

        console_mock.assert_has_calls(
            [
                call.input("Введите команду: "),
                call.input("Введите ID пациента: "),
                call.input("Желаете этого клиента выписать? (да/нет) "),
                call.print("Пациент остался в статусе 'Готов к выписке'"),
                call.input("Введите команду: "),
                call.print("Сеанс завершён."),
            ]
        )
        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 1]

    def test_status_up_when_patient_not_exists(self):
        console_mock = MagicMock()
        console_mock.input.side_effect = ["status up", "3", "stop"]

        hospital = make_hospital([3, 1])
        make_application(hospital, console_mock).run()

        console_mock.assert_has_calls(
            [
                call.input("Введите команду: "),
                call.input("Введите ID пациента: "),
                call.print("Ошибка. В больнице нет пациента с таким ID"),
                call.input("Введите команду: "),
                call.print("Сеанс завершён."),
            ]
        )

        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 1]

    def test_status_up_when_patient_id_is_not_positive_integer(self):
        console_mock = MagicMock()
        console_mock.input.side_effect = ["status up", "два", "stop"]

        hospital = make_hospital([3, 1])
        make_application(hospital, console_mock).run()

        console_mock.assert_has_calls(
            [
                call.input("Введите команду: "),
                call.input("Введите ID пациента: "),
                call.print("Ошибка. ID пациента должно быть числом (целым, положительным)"),
                call.input("Введите команду: "),
                call.print("Сеанс завершён."),
            ]
        )
        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 1]

    def test_get_statistic(self):
        console_mock = MagicMock()
        console_mock.input.side_effect = ["рассчитать статистику", "stop"]

        make_application(make_hospital([3, 0, 3, 0]), console_mock).run()

        console_mock.assert_has_calls(
            [
                call.input("Введите команду: "),
                call.print(f"В больнице на данный момент находится 4 чел., из них:"),
                call.print(f"- в статусе 'Тяжело болен': 2 чел."),
                call.print(f"- в статусе 'Готов к выписке': 2 чел."),
                call.input("Введите команду: "),
                call.print("Сеанс завершён."),
            ]
        )

