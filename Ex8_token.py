import requests
import time

base_url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(base_url)
response_data = response.json()
print(response_data)
token = response_data["token"]
seconds = response_data["seconds"]

print(f"Задача создана. Token: {token}, Время ожидания: {seconds} секунд")

time.sleep(1)
check_url = f"{base_url}?token={token}"
response_check_before = requests.get(check_url)
response_check_before_data = response_check_before.json()

assert response_check_before_data["status"] == "Job is NOT ready", "Status до готовности должен быть 'Job is NOT ready'"
print("Статус до готовности: OK")

time.sleep(seconds)

response_check_after = requests.get(check_url)
response_check_after_data = response_check_after.json()

assert response_check_after_data["status"] == "Job is ready", "Status после готовности должен быть 'Job is ready'"
assert "result" in response_check_after_data, "Поле 'result' должно присутствовать после готовности"
print("Статус после готовности: OK")
print("Результат получен: OK")

print("Тест успешно пройден!")