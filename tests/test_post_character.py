from checker.v2_character import Checker
import pytest
from utils.http_client import HttpClient
import logging

LOGGER = logging.getLogger(__name__)


class TestPostCharacter:

    def test_post_character(self, basic_auth, prepare_data_for_post_character):
        """ Проверяем создание нового персонажа, валидируем данные для запроса с возвращенными данными.
        После проверяем, возвращается ли созданный персонаж из коллекции
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request, json=prepare_data_for_post_character)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker(auth=basic_auth).check_post_character(prepare_data_for_post_character, response)

    def test_non_unique_character(self, basic_auth, character_to_request):
        """ Сохраняем персонажа без изменения данных
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request, json=character_to_request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker(auth=basic_auth).check_post_non_unique_character(response)

    @pytest.mark.parametrize('execution_number', range(6))
    def test_post_character_negative(self, basic_auth, invalid_data_for_post_character, execution_number):
        """ Проверяем, что с невалидными данными персонаж не создается.
            После проверяем, что персонаж не возвращается из коллекции
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request,
                                                    json=invalid_data_for_post_character[execution_number])
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker(auth=basic_auth).check_send_invalid_character(invalid_data_for_post_character[execution_number],
                                                              response)

    def test_overload_post_character(self, basic_auth, prepare_data_for_overload_post_character):
        """ Проверяем ограничение на количество персонажей"
        """
        response_list = []
        for i in range(0, 500):
            request = "/v2/character"
            response = HttpClient(auth=basic_auth).post(path=request, json=prepare_data_for_overload_post_character[i])
            LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
            if i == 499:
                response_list.append(response)
        Checker(auth=basic_auth).check_post_character_overload(response_list[0])

    def test_post_character_negative_auth(self, basic_auth, prepare_data_for_post_character):
        """ Негативный тест на отсутствие авторизации
        """
        request = "/v2/character"
        response = HttpClient(auth=None).post(path=request, json=prepare_data_for_post_character)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_auth(response)
