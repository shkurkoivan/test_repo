import pytest
from utils.http_client import HttpClient
from checker.v2_character import Checker

import numpy as np


@pytest.fixture(scope="function")
def character_to_request(basic_auth):
    request = "/v2/characters"
    response = HttpClient(auth=basic_auth).get(path=request)
    Checker.check_get_characters(response)
    response = response.json()['result']
    name = np.random.choice(response)['name']
    name.replace(" ", "+")
    return name


def test_get_characters(basic_auth):
    """ Проверяем, получение коллекции.
        По хорошему, надо бы сделать метод на наполнение в случае пустой базы, но здесь я схалтурил.
    """
    request = "/v2/characters"
    response = HttpClient(auth=basic_auth).get(path=request)
    Checker().check_get_characters(response)


def test_get_random_character(basic_auth, character_to_request):
    """ Проверяем получение случайного персонажа из непустой коллекци.
        Используем фикстуру character_to_request, чтобы не харкодить значения для теста
        и прогонять тест с разными именами (в т.ч. и двухсоставными)
    """
    request = f"/v2/character?name={character_to_request}"
    response = HttpClient(auth=basic_auth).get(path=request)
    Checker().check_get_character(character_to_request, response)


@pytest.mark.parametrize("name_to_request", ["", "-12301", " ", "1111111111111111111"*100])
def test_get_random_character_negative(basic_auth, name_to_request):
    """ Негативные тесты
    """
    request = f"/v2/character?name={name_to_request}"
    response = HttpClient(auth=basic_auth).get(path=request)
    Checker().check_get_character_negative(response)


def test_get_random_character_negative_auth(character_to_request):
    """ Негативный тест на отсутствие авторизации
    """
    request = f"/v2/character?name={character_to_request}"
    response = HttpClient(auth=None).get(path=request)
    Checker().check_auth(response)


def test_get_characters_negative_auth(basic_auth):
    """ Негативный тест на отсутствие авторизации
    """
    request = "/v2/characters"
    response = HttpClient(auth=None).get(path=request)
    Checker().check_auth(response)
