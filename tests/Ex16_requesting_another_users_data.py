from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("User get cases")
class TestUserGet(BaseCase):

    @allure.description("Getting information about a user when authorizing for another user")
    def test_get_user_datails_auth_as_same_user(selfs):
        # REGISTER USER 1
        register_data1 = selfs.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)
        Assertions.assert_code_status(response1, 200)
        user_id1 = selfs.get_json_value(response1, "id")
        #print(user_id1)

        data = {

            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        print(response1.text)

        auth_sid = selfs.get_cookie(response1, "auth_sid")
        token = selfs.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = selfs.get_json_value(response1, "user_id")
        #user_id_from_auth_method=3
        print(user_id_from_auth_method)

        response2 = MyRequests.get(
            f"/api/user/{user_id1}",
                headers={"x-csrf-token": token},
                cookies = {"auth_sid": auth_sid}
        )

        print(response2)

        not_expected_fields = ["email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, not_expected_fields)