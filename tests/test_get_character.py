from checker.v2_character import Checker
import pytest
from utils.http_client import HttpClient
import logging

LOGGER = logging.getLogger(__name__)


class TestGetCharacter:

    def test_get_characters(self, basic_auth):
        """ Проверяем получение коллекции.
            По-хорошему, надо бы сделать метод на наполнение в случае пустой базы, но здесь я схалтурил.
        """
        request = "/v2/characters"
        response = HttpClient(auth=basic_auth).get(path=request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_get_characters(response)

    @pytest.mark.parametrize('execution_number', range(3))
    def test_get_random_character(self, basic_auth, character_to_request, execution_number):
        """ Проверяем получение случайного персонажа из непустой коллекци.
            Используем фикстуру character_to_request, чтобы не хардкодить значения для теста
                и прогонять тест с разными именами (в т.ч. и двухсоставными)
            Тест гоняется несколько раз, т.к. коллекция на стейдже достаточно наполнена
                и хардкодить не хочется, 3х раз достаточно чтобы перебрать различные примеры.
        """
        character_name = character_to_request["name"]
        request = f"/v2/character"
        params = {"name": character_name}
        response = HttpClient(auth=basic_auth).get(path=request, params=params)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_get_character(character_to_request, response)

    @pytest.mark.parametrize("name_to_request", ["", "-12301", " ", "1111111111111111111"*100])
    def test_get_random_character_negative(self, basic_auth, name_to_request):
        """ Негативные тесты
        """
        request = f"/v2/character?name={name_to_request}"
        response = HttpClient(auth=basic_auth).get(path=request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_get_character_negative(response)

    def test_get_random_character_negative_auth(self, character_to_request):
        """ Негативный тест на отсутствие авторизации
        """
        request = f"/v2/character?name={character_to_request}"
        response = HttpClient(auth=None).get(path=request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_auth(response)

    def test_get_characters_negative_auth(self):
        """ Негативный тест на отсутствие авторизации
        """
        request = "/v2/characters"
        response = HttpClient(auth=None).get(path=request)
        LOGGER.info(f"{request}, {response.status_code}, {response.json()}")
        Checker().check_auth(response)
