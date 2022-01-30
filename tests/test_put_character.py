from checker.v2_character import Checker
from utils.http_client import HttpClient
import pytest
import logging

LOGGER = logging.getLogger(__name__)


class TestPutCharacter:

    def test_put_character(self, basic_auth, prepare_data_for_put_character):
        """ Редактируем персонажа из коллекции, валидируем данные для запроса с возвращенными данными.
        После проверяем, возвращается ли созданный персонаж из коллекции
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).put(path=request, json=prepare_data_for_put_character)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker(auth=basic_auth).check_put_character(prepare_data_for_put_character, response)

    def test_put_character_with_edit(self, basic_auth, character_to_request):
        """ Сохраняем персонажа без изменения данных
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).put(path=request, json=character_to_request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker(auth=basic_auth).check_put_character(character_to_request, response)

    @pytest.mark.parametrize('execution_number', range(6))
    def test_put_character_negative(self, basic_auth, execution_number, invalid_data_for_put_character):
        """ Проверяем, что с невалидными данными персонаж не редактируется и не создается
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request,
                                                    json=invalid_data_for_put_character[execution_number])
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker(auth=basic_auth).check_send_invalid_character(invalid_data_for_put_character[execution_number],
                                                              response)

    def test_put_character_negative_auth(self, basic_auth, prepare_data_for_post_character):
        """ Негативный тест на отсутствие авторизации
        """
        request = "/v2/character"
        response = HttpClient(auth=None).put(path=request, json=prepare_data_for_post_character)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_auth(response)
