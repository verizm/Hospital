from tests.mock_console import MockConsole

from tests.hospital_helper import (
    make_hospital,
    make_application,
    get_actual_hospital_db_as_statuses_list,
)


class TestHospitalScenario:

    def test_ordinary_positive_scenario(self):

        hospital = make_hospital([3, 1, 2, 1])
        console = MockConsole()
        console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '1')
        console.add_expected_output_message("Cтатус пациента: Готов к выписке")

        console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '2')
        console.add_expected_output_message("Новый статус пациента: Слегка болен")

        console.add_expected_request_and_response('Введите команду: ', 'понизить статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '4')
        console.add_expected_output_message("Новый статус пациента: Тяжело болен")

        console.add_expected_request_and_response('Введите команду: ', 'рассчитать статистику')
        console.add_expected_output_message("В больнице на данный момент находится 4 чел., из них:")
        console.add_expected_output_message("- в статусе 'Тяжело болен': 1 чел.")
        console.add_expected_output_message("- в статусе 'Слегка болен': 2 чел.")
        console.add_expected_output_message("- в статусе 'Готов к выписке': 1 чел.")

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        app = make_application(hospital, console)

        app.run()

        console.verify_all_calls_have_been_made()
        assert get_actual_hospital_db_as_statuses_list(hospital) == [3, 2, 2, 0]

    def test_unknown_command(self):

        hospital = make_hospital([])
        console = MockConsole()
        console.add_expected_request_and_response('Введите команду: ', 'сделай что-нибудь...')
        console.add_expected_output_message('Неизвестная команда! Попробуйте ещё раз')

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        make_application(hospital, console).run()

        console.verify_all_calls_have_been_made()

    def test_boundary_cases(self):

        hospital = make_hospital([0, 3, 1, 3])
        console = MockConsole()
        console.add_expected_request_and_response('Введите команду: ', 'понизить статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '1')
        console.add_expected_output_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

        console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '2')
        console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'да')
        console.add_expected_output_message('Пациент выписан из больницы')

        console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '4')
        console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет) ', 'нет')
        console.add_expected_output_message("Пациент остался в статусе 'Готов к выписке'")

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        make_application(hospital, console).run()

        console.verify_all_calls_have_been_made()
        assert get_actual_hospital_db_as_statuses_list(hospital) == [0, None, 1, 3]

    def test_cases_of_invalid_data_entry(self):

        hospital = make_hospital([1, 1])
        console = MockConsole()
        console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', 'два')
        console.add_expected_output_message('Ошибка. ID пациента должно быть числом (целым, положительным)')

        console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '3')
        console.add_expected_output_message('Ошибка. В больнице нет пациента с таким ID')

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        make_application(hospital, console).run()

        console.verify_all_calls_have_been_made()

    def test_discharge_patient(self):

        hospital = make_hospital([1, 3, 1])
        console = MockConsole()
        console.add_expected_request_and_response('Введите команду: ', 'выписать пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '2')
        console.add_expected_output_message('Пациент выписан из больницы')

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        make_application(hospital, console).run()

        console.verify_all_calls_have_been_made()
        assert get_actual_hospital_db_as_statuses_list(hospital) == [1, None, 1]

    def test_add_patient(self):
        hospital = make_hospital([1, 3, 1])
        console = MockConsole()
        console.add_expected_request_and_response('Введите команду: ', 'add patient')
        console.add_expected_request_and_response('Введите статус пациента: ', 'Готов к выписке')
        console.add_expected_output_message('Пациент госпитализирован. Присвоен ID 4')

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        make_application(hospital, console).run()

        console.verify_all_calls_have_been_made()
        assert get_actual_hospital_db_as_statuses_list(hospital) == [1, 3, 1, 3]

    def test_add_patient_when_status_is_not_exists(self):
        hospital = make_hospital([1, 3, 1])
        console = MockConsole()
        console.add_expected_request_and_response('Введите команду: ', 'add patient')
        console.add_expected_request_and_response('Введите статус пациента: ', 'не готов к выписке')
        console.add_expected_output_message(
            "Ошибка. Статус пациента должен быть один из ['Тяжело болен', 'Болен', 'Слегка болен', 'Готов к выписке']"
        )

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        make_application(hospital, console).run()

        console.verify_all_calls_have_been_made()
        assert get_actual_hospital_db_as_statuses_list(hospital) == [1, 3, 1]
