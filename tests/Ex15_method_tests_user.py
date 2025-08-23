import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    requests_parameter = [
        ("123","learnqa", "firstName", "lastName", None),
        ("123","learnqa", "firstName", None, "spiridonov+1@example.com"),
        ("123","learnqa", None, "lastName", "spiridonov+2@example.com"),
        ("123", None, "firstName", "lastName", "spiridonov+3@example.com"),
        (None,"learnqa", "firstName", "lastName", "spiridonov+4@example.com")

    ]

    def test_create_user_witch_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName':'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert  response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_not_valid_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    def test_create_user_short_name(self):
        first_name = 'L'
        email = 'spiridonov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': first_name,
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_long_name(self):
        first_name = 'LongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongNameLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongNameLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongLongName'
        email = 'spiridonov3@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': first_name,
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize(("password", "username", "first_name", "last_name","email"), requests_parameter)
    def test_create_user_no_required_parameter(self, password, username, first_name, last_name, email):
        data = {
            'password': password,
            'username': username,
            'firstName': first_name,
            'lastName': last_name,
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"

        if password is None:
            assert response.content.decode(
                "utf-8") == f"The following required params are missed: password", f"Unexpected response content {response.content}"

        if username is None:
            assert response.content.decode(
                "utf-8") == f"The following required params are missed: username", f"Unexpected response content {response.content}"

        if first_name is None:
            assert response.content.decode(
                "utf-8") == f"The following required params are missed: firstName", f"Unexpected response content {response.content}"

        if last_name is None:
            assert response.content.decode(
                "utf-8") == f"The following required params are missed: lastName", f"Unexpected response content {response.content}"

        if email is None:
            assert response.content.decode(
                "utf-8") == f"The following required params are missed: email", f"Unexpected response content {response.content}"