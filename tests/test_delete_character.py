from checker.v2_character import Checker
from utils.http_client import HttpClient
import pytest
import logging

LOGGER = logging.getLogger(__name__)


class TestDeleteCharacter:

    def test_get_random_character(self, basic_auth, character_to_request):
        """ Проверяем удаление случайного персонажа из непустой коллекци.
        """
        character_name = character_to_request["name"]
        request = f"/v2/character"
        params = {"name": character_name}
        response = HttpClient(auth=basic_auth).delete(path=request, params=params)
        Checker().check_delete_character(character_to_request, response)

    @pytest.mark.parametrize("name_to_request", ["", "-12301", " ", "1111111111111111111"*100])
    def test_get_random_character_negative(self, basic_auth, name_to_request):
        """ Негативные тесты на удаление по невалидному имени
        """
        request = f"/v2/character?name={name_to_request}"
        response = HttpClient(auth=basic_auth).delete(path=request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_delete_character_negative(response)

    def test_delete_characters_negative_auth(self, character_to_request):
        """ Негативный тест на отсутствие авторизации
        """
        character_name = character_to_request["name"]
        request = "/v2/character"
        params = {"name": character_name}
        response = HttpClient(auth=None).delete(path=request, params=params)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_auth(response)
