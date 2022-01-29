from utils.http_client import HttpClient
from utils.constants import STATUS_CODE, COLLECTION


class Checker:
    def __init__(self, auth=None):
        self.auth = auth

    def _is_character_in_the_collection(self, name):
        request = f"/v2/character?name={name}"
        response = HttpClient(auth=self.auth).get(path=request)
        if "result" in response.json():
            return name == response.json()["result"]["name"]
        else:
            return False

    def _is_collection_full(self):
        request = "/v2/characters"
        response = HttpClient(auth=self.auth).get(path=request)
        return len(response.json()["result"]) == COLLECTION.ITEMS_CAPACITY.value

    def check_get_character(self, character_name, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()["result"]
        assert len(response) != 0, "The response is empty!"
        assert response['name'] == character_name

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
        assert self._is_character_in_the_collection(name=response["name"]) is True

    def check_post_character_negative(self, request, response):
        assert response.status_code == STATUS_CODE.BAD_REQUEST.value, f"Negative test did not passed!" \
                                                                      f"Actual code is {response.status_code}" \
                                                                      f"Actual reason is {response.reason}"
        assert self._is_character_in_the_collection(name=request["name"]) is False

    def check_post_character_overload(self, response):
        assert response.status_code == STATUS_CODE.BAD_REQUEST.value, f"Overload test did not passed!" \
                                                                      f"Actual code is {response.status_code}" \
                                                                      f"Actual reason is {response.reason}"
        assert self._is_collection_full() is True
