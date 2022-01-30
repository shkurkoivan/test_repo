from utils.http_client import HttpClient
from utils.constants import STATUS_CODE, COLLECTION
import logging


class Checker:
    def __init__(self, auth=None):
        self.auth = auth
        self.LOGGER = logging.getLogger(__name__)

    def is_character_in_the_collection(self, name):
        request = f"/v2/character?name={name}"
        response = HttpClient(auth=self.auth).get(path=request)
        if "result" in response.json():
            return name == response.json()["result"]["name"]
        else:
            return False

    def get_collection_length(self):
        request = "/v2/characters"
        response = HttpClient(auth=self.auth).get(path=request)
        return len(response.json()["result"])

    def check_get_character(self, character_to_request, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()["result"]
        assert len(response) != 0, "The response is empty!"
        assert response["name"] == character_to_request["name"]

    def check_get_characters(self, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()["result"]
        assert len(response) != 0, "The response is empty!"

    def check_get_character_negative(self, response):
        assert response.status_code == STATUS_CODE.BAD_REQUEST.value, f"Negative test did not passed!" \
                                                                      f"Actual code is {response.status_code}" \
                                                                      f"Actual reason is {response.reason}"

    def check_auth(self, response):
        assert response.status_code == STATUS_CODE.UNAUTHORIZED.value, f"Negative test did not passed!" \
                                                                       f"Actual code is {response.status_code}" \
                                                                       f"Actual reason is {response.reason}"

    def check_post_character(self, request, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()["result"]
        assert len(response) != 0, "The response is empty!"
        assert len(request) == len(response)
        assert response["name"] == request["name"]
        assert response["universe"] == request["universe"]
        assert response["education"] == request["education"]
        assert response["weight"] == request["weight"]
        assert response["height"] == request["height"]
        assert response["identity"] == request["identity"]
        # проверяем наличие персонажа в колллекции
        assert self.is_character_in_the_collection(name=response["name"]) is True

    def check_send_invalid_character(self, request, response):
        assert response.status_code == STATUS_CODE.BAD_REQUEST.value, f"Negative test did not passed!" \
                                                                      f"Actual code is {response.status_code}" \
                                                                      f"Actual reason is {response.reason}"
        assert self.is_character_in_the_collection(name=request["name"]) is False

    def check_post_character_overload(self, response):
        assert response.status_code == STATUS_CODE.BAD_REQUEST.value, f"Overload test did not passed!" \
                                                                      f"Actual code is {response.status_code}" \
                                                                      f"Actual reason is {response.reason}"
        assert self.get_collection_length() == COLLECTION.ITEMS_MAX_CAPACITY.value

    def check_put_character(self, request, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()["result"]
        assert len(response) != 0, "The response is empty!"
        assert len(request) == len(response)
        assert response["name"] == request["name"]
        assert response["universe"] == request["universe"]
        assert response["education"] == request["education"]
        assert response["weight"] == request["weight"]
        assert response["height"] == request["height"]
        assert response["identity"] == request["identity"]

    def check_delete_character(self, request, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()["result"]
        assert len(response) != 0, "The response is empty!"
        assert response == f'Hero {request["name"]} is deleted'
        assert self.is_character_in_the_collection(name=request["name"]) is False

    def check_delete_character_negative(self, response):
        assert response.status_code == STATUS_CODE.BAD_REQUEST.value, f"Negative test did not passed!" \
                                                                      f"Actual code is {response.status_code}" \
                                                                      f"Actual reason is {response.reason}"

    def check_reset(self, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        assert self.get_collection_length() == COLLECTION.ITEMS_MIN_AMOUNT.value
