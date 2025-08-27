import json
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("User edit cases")
class TestUserEdit(BaseCase):

    URL="/user/"
    LOGIN_URL = "/user/login"

    @allure.description("Edit just created user")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(self.URL,data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post(self.LOGIN_URL, data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"{self.URL}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"{self.URL}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("Edit user unauthorized")
    def test_edit_user_unauthorized(self):
        user_id = 2
        new_name = "Unauthorized Edit"

        response = MyRequests.put(
            f"{self.URL}{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)

    @allure.description("Edit user by another user")
    def test_edit_user_by_another_user(self):
        # REGISTER USER 1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post(self.URL, data=register_data1)
        Assertions.assert_code_status(response1, 200)
        user_id1 = self.get_json_value(response1, "id")

        # LOGIN USER 1
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response2 = MyRequests.post(self.LOGIN_URL, data=login_data1)
        auth_sid1 = self.get_cookie(response2, "auth_sid")
        token1 = self.get_header(response2, "x-csrf-token")

        # REGISTER USER 2
        register_data2 = self.prepare_registration_data()
        response3 = MyRequests.post(self.URL, data=register_data2)

        Assertions.assert_code_status(response3, 200)
        user_id2 = self.get_json_value(response3, "id")

        # EDIT USER 2 BY USER 1
        new_name = "Hacked Name"
        response4 = MyRequests.put(
            f"{self.URL}{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response4, 400)

    @allure.description("Edit user email invalid format")
    def test_edit_user_email_invalid_format(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(self.URL, data=register_data)

        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response2 = MyRequests.post(self.LOGIN_URL, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        invalid_email = "invalid_email"

        response3 = MyRequests.put(
            f"{self.URL}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": invalid_email}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_has_key(response3, "error")

        response_data = json.loads(response3.text)
        assert "Invalid email format" in response_data["error"]

    @allure.description("Edit user short first name")
    def test_edit_user_short_first_name(self):

        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(self.URL, data=register_data)

        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response2 = MyRequests.post(self.LOGIN_URL, data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        short_name = "A"

        response3 = MyRequests.put(
            f"{self.URL}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": short_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_has_key(response3, "error")

        response_data = json.loads(response3.text)
        assert "The value for field `firstName` is too short" in response_data["error"]
