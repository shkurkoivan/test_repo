from checker.v2_character import Checker
import copy
import pytest
import random
from utils.http_client import HttpClient
from utils.data_utils import prepare_invalid_data_for_post_character


class TestPostCharacter:

    @pytest.fixture(scope="class")
    def prepare_data(self, basic_auth):
        request_data = {"name": "TestUser" + str(random.choice([0, 10000000])), "universe": "Marvel Universe",
                        "education": "High school (unfinished)", "weight": random.choice([60, 150]),
                        "height": random.choice([1.93, 2.5]), "identity": "Secret (known to the U.S. government)"}
        yield request_data
        HttpClient(auth=basic_auth).post(path="/v2/reset")  # Очищаем коллекцию после тестов

    def test_post_characters(self, basic_auth, prepare_data):
        """ Проверяем создание нового персонажа, валидируем данные для запроса с возвращенными данными.
        После проверяем, возвращается ли созданный персонаж из коллекции
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request, json=prepare_data)
        Checker(auth=basic_auth).check_post_character(prepare_data, response)

    @pytest.mark.parametrize("invalid_data", prepare_invalid_data_for_post_character())
    def test_post_characters_negative(self, basic_auth, invalid_data):
        """ Проверяем, что с невалидными данными персонаж не создается.
            После проверяем, что персонаж не возвращается из коллекции
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request, json=invalid_data)
        Checker(auth=basic_auth).check_post_character_negative(invalid_data, response)

    @pytest.fixture(scope="function")
    def prepare_data_for_overload_post_character(self, basic_auth):
        list_with_data = []
        valid_data = {"name": "TestUserOverload", "universe": "Marvel Universe",
                      "education": "High school (unfinished)", "weight": random.choice([60, 150]),
                      "height": random.choice([1.93, 2.5]), "identity": "Publicly known"}

        for i in range(0, 500):
            list_with_data.append((copy.deepcopy(valid_data)))
            list_with_data[i]["name"] += str(i + 1)

        yield list_with_data
        HttpClient(auth=basic_auth).post(path="/v2/reset")  # Очищаем коллекцию после тестов

    def test_overload_post_characters(self, basic_auth, prepare_data_for_overload_post_character):
        """ Проверяем ограничение на количество персонажей"
        """
        response_list = []
        for i in range(0, 201):
            request = "/v2/character"
            response = HttpClient(auth=basic_auth).post(path=request, json=prepare_data_for_overload_post_character[i])
            if i == 200:
                response_list.append(response)
        Checker(auth=basic_auth).check_post_character_overload(response_list[0])

    def test_post_characters_negative_auth(self, basic_auth, prepare_data):
        """ Негативный тест на отсутствие авторизации
        """
        request = "/v2/character"
        response = HttpClient(auth=None).post(path=request, json=prepare_data)
        Checker().check_auth(response)
