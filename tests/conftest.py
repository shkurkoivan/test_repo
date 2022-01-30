import pytest
from utils.http_client import HttpClient
from checker.v2_character import Checker
import numpy as np
import random
import copy


@pytest.fixture(scope="session")
def character_to_request(basic_auth):
    request = "/v2/characters"
    response = HttpClient(auth=basic_auth).get(path=request)
    Checker().check_get_characters(response)
    response = response.json()["result"]
    character = np.random.choice(response)
    yield character


@pytest.fixture(scope="class")
def prepare_data_for_post_character(basic_auth):
    request_data = {"name": "TestUser" + str(random.choice([0, 10000000])), "universe": "Marvel Universe",
                    "education": "High school (unfinished)", "weight": random.choice([60, 150]),
                    "height": random.choice([1.93, 2.5]), "identity": "Secret (known to the U.S. government)"}
    yield request_data
    HttpClient(auth=basic_auth).post(path="/v2/reset")  # Очищаем коллекцию после тестов


@pytest.fixture(scope="class")
def invalid_data_for_post_character():
    list_with_ivalid__data = []
    valid_data = {"name": "TestUserInvalid", "universe": "Marvel Universe",
                  "education": "High school (unfinished)", "weight": random.choice([60, 150]),
                  "height": random.choice([1.93, 2.5]), "identity": "Publicly known"}

    #  Создаем список словарей, в каждом случайно удаляя required поле
    for i in range(0, len(valid_data)):
        list_with_ivalid__data.append((copy.deepcopy(valid_data)))
        list_with_ivalid__data[i]["name"] += str(i + 1)
        list_with_ivalid__data[i][random.choice(list(valid_data.keys()))] = ""
    # Для пары полей применяем неверный тип содержимого
    list_with_ivalid__data[2][random.choice(["name", "universe,", "education"])] = random.choice([5, 2.5])
    list_with_ivalid__data[4][random.choice(["height", "weight,"])] = "invalid"
    yield list_with_ivalid__data


@pytest.fixture(scope="class")
def prepare_data_for_overload_post_character(basic_auth):
    list_with_data = []
    valid_data = {"name": "TestUserOverload", "universe": "Marvel Universe",
                  "education": "High school (unfinished)", "weight": random.choice([60, 150]),
                  "height": random.choice([1.93, 2.5]), "identity": "Publicly known"}

    for i in range(0, 500):
        list_with_data.append((copy.deepcopy(valid_data)))
        list_with_data[i]["name"] += str(i + 1)

    yield list_with_data
    HttpClient(auth=basic_auth).post(path="/v2/reset")  # Очищаем коллекцию после тестов


@pytest.fixture(scope="class")
def prepare_data_for_put_character(basic_auth, character_to_request):
    character_to_request[random.choice(["identity", "universe", "education", "other_aliases"])] = "valid_input"
    character_to_request[random.choice(["height", "weight"])] = random.choice([100, 200])
    yield character_to_request
    HttpClient(auth=basic_auth).post(path="/v2/reset")  # Очищаем коллекцию после тестов


@pytest.fixture(scope="class")
def invalid_data_for_put_character(basic_auth, character_to_request):
    list_with_ivalid__data = []
    #  Создаем список словарей, в каждом случайно удаляя required поле
    for i in range(0, len(character_to_request)):
        list_with_ivalid__data.append((copy.deepcopy(character_to_request)))
        list_with_ivalid__data[i]["name"] += str(i + 1)
        list_with_ivalid__data[i][random.choice(list(character_to_request.keys()))] = ""
    # Для пары полей применяем неверный тип содержимого
    list_with_ivalid__data[2][random.choice(["name", "universe,", "education"])] = random.choice([5, 2.5])
    list_with_ivalid__data[4][random.choice(["height", "weight,"])] = "invalid"
    yield list_with_ivalid__data
