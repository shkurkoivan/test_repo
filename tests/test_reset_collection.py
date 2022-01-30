from checker.v2_character import Checker
from utils.http_client import HttpClient
import logging

LOGGER = logging.getLogger(__name__)


class TestDeleteCharacter:

    def test_check_reset(self, basic_auth, prepare_data_for_post_character):
        """ Проверяем сброс непустой коллекции.
            Сначала постим одного персонажа, дальше делаем сброс коллекции и проверяем количество элементов в ней
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request, json=prepare_data_for_post_character)
        Checker(auth=basic_auth).check_post_character(prepare_data_for_post_character, response)
        request = "/v2/reset"
        response = HttpClient(auth=basic_auth).post(path=request)
        LOGGER.info(f"{request}, {response.status_code}")
        Checker(auth=basic_auth).check_reset(response)

    def test_check_reset_negative_auth(self):
        """ Негативный тест на отсутствие авторизации
        """
        request = "/v2/reset"
        response = HttpClient(auth=None).post(path=request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_auth(response)
