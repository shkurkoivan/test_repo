from checker.v2_character import Checker
from utils.http_client import HttpClient
import pytest


class TestPutCharacter:

    def test_put_characters(self, basic_auth, prepare_data_for_put_character):
        """ Проверяем создание нового персонажа, валидируем данные для запроса с возвращенными данными.
        После проверяем, возвращается ли созданный персонаж из коллекции
        """
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).put(path=request, json=prepare_data_for_put_character)
        Checker(auth=basic_auth).check_put_character(prepare_data_for_put_character, response)

    @pytest.mark.parametrize('execution_number', range(6))
    def test_pust_characters_negative(self, basic_auth, execution_number, invalid_data_for_put_character):
        request = "/v2/character"
        response = HttpClient(auth=basic_auth).post(path=request,
                                                    json=invalid_data_for_put_character[execution_number])
        Checker(auth=basic_auth).check_send_invalid_character(invalid_data_for_put_character[execution_number],
                                                              response)

    def test_post_characters_negative_auth(self, basic_auth, prepare_data_for_post_character):
        """ Негативный тест на отсутствие авторизации
        """
        request = "/v2/character"
        response = HttpClient(auth=None).post(path=request, json=prepare_data_for_post_character)
        Checker().check_auth(response)

