import requests
import pytest

class TestUserAgentCheck:

    URL = "https://playground.learnqa.ru/ajax/api/user_agent_check"

    users_agents = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30","Mobile","No","Android"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148","Mobile","Chrome","iOS"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html","Googlebot", "Unknown", "Unknown"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0","Web", "Chrome", "No"),
        ("'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1", "Mobile", "No", "iPhone")

    ]

    @pytest.mark.parametrize(("user_agent","expected_platform","expected_browser","expected_device"),users_agents)
    def test_user_agent_check(self, user_agent, expected_platform, expected_browser, expected_device):

        response = requests.get(
            self.URL,
            headers={"User-Agent": user_agent}
        )

        response.raise_for_status()

        response_data = response.json()
        print(response_data)

        errors = []
        if response_data["platform"] != expected_platform:
            errors.append(f"platform: expected '{expected_platform}', got '{response_data['platform']}'")
        if response_data["browser"] != expected_browser:
            errors.append(f"browser: expected '{expected_browser}', got '{response_data['browser']}'")
        if response_data["device"] != expected_device:
            errors.append(f"device: expected '{expected_device}', got '{response_data['device']}'")

        assert not errors, f"User Agent '{user_agent}' has incorrect values: {', '.join(errors)}"
