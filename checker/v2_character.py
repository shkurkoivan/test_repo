from utils.constants import STATUS_CODE


class Checker:
    def check_get_character(character_name, response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()['result']
        assert len(response) != 0, "The response is empty!"
        assert response['name'] == character_name

    def check_get_characters(response):
        assert response.status_code == STATUS_CODE.OK.value, f"Status code isn't OK!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"
        response = response.json()['result']
        assert len(response) != 0, "The response is empty!"

    def check_get_character_negative(response):
        assert response.status_code == STATUS_CODE.BAD_REQUEST.value, f"Negative test did not passed!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"

    def check_auth(response):
        assert response.status_code == STATUS_CODE.UNAUTHORIZED.value, f"Negative test did not passed!" \
                                                             f"Actual code is {response.status_code}" \
                                                             f"Actual reason is {response.reason}"