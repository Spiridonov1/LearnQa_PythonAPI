from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("User delete cases")
class TestUserDelete(BaseCase):

    URL = "/user/"
    LOGIN_URL = "/user/login"

    @allure.description("Delete user unauthorized")
    def test_delete_user_unauthorized(self):
        user_id_to_delete = 2
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post(self.LOGIN_URL, data=login_data)
        Assertions.assert_code_status(response_login, 200)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        response_delete = MyRequests.delete(
            f"{self.URL}{user_id_to_delete}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_delete, 400)

    @allure.description("Delete user success")
    def test_delete_user_success(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post(self.URL, data=register_data)
        Assertions.assert_code_status(response_register, 200)
        user_id = self.get_json_value(response_register, "id")

        # LOGIN
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = MyRequests.post(self.LOGIN_URL, data=login_data)
        Assertions.assert_code_status(response_login, 200)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response_delete = MyRequests.delete(
            f"{self.URL}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_delete, 200)

        # GET
        response_get = MyRequests.get(
            f"{self.URL}{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_get, 404)

    @allure.description("Delete user by another user")
    def test_delete_user_by_another_user(self):
        # REGISTER USER 1
        register_data1 = self.prepare_registration_data()
        response_register1 = MyRequests.post(self.URL, data=register_data1)
        Assertions.assert_code_status(response_register1, 200)
        user_id1 = self.get_json_value(response_register1, "id")

        # LOGIN USER 1
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response_login1 = MyRequests.post(self.LOGIN_URL, data=login_data1)
        Assertions.assert_code_status(response_login1, 200)
        auth_sid1 = self.get_cookie(response_login1, "auth_sid")
        token1 = self.get_header(response_login1, "x-csrf-token")

        # REGISTER USER 2
        register_data2 = self.prepare_registration_data()
        response_register2 = MyRequests.post(self.URL, data=register_data2)
        Assertions.assert_code_status(response_register2, 200)
        user_id2 = self.get_json_value(response_register2, "id")

        # DELETE USER 2 BY USER 1
        response_delete = MyRequests.delete(
            f"{self.URL}{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1}
        )
        Assertions.assert_code_status(response_delete, 400)