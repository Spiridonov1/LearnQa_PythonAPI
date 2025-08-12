import requests

class TestCookieMethodRequest:
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)

        cookies = response.cookies

        print(f"Cookies from response: {cookies.items()}")  # Выводим все cookie и их значения

        assert 'HomeWork' in cookies, "Cookie 'HomeWork' is not present in the response"

        expected_value = "hw_value"
        actual_value = cookies['HomeWork']
        assert actual_value == expected_value, f"Unexpected value for cookie 'HomeWork'. Expected: {expected_value}, Actual: {actual_value}"

        print("Test passed: Cookie 'HomeWork' found with the correct value.")