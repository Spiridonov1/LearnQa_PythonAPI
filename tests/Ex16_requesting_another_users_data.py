from unittest import expectedFailure

import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_datails_not_auth(selfs):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_datails_auth_as_same_user(selfs):
        data = {

            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 =requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = selfs.get_cookie(response1, "auth_sid")
        token = selfs.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = selfs.get_json_value(response1, "user_id") + 1

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies = {"auth_sid": auth_sid}
        )

        not_expected_fields = ["email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, not_expected_fields)