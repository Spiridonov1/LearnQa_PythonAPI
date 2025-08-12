import requests

class TestCookieMethodRequest:
    def test_request_homework_header(self):

        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        headers = response.headers

        print(f"Headers from response: {headers}")

        assert 'x-secret-homework-header' in headers, "Header 'x-secret-homework-header' is not present in the response"

        expected_value = "Some secret value"
        actual_value = headers['x-secret-homework-header']
        assert actual_value == expected_value, f"Unexpected value for header 'x-secret-homework-header'. Expected: {expected_value}, Actual: {actual_value}"

        print("Test passed: Header 'x-secret-homework-header' found with the correct value.")