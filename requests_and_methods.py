import requests

base_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

print("1. Запрос без параметра 'method':")
response = requests.get(base_url)
print(f"GET Response code: {response.status_code}, Content: {response.text}")

print("\n2. Запрос с неподдерживаемым методом (HEAD):")
response = requests.head(base_url, data={'method': 'HEAD'})
print(f"HEAD Response code: {response.status_code}, Content: {response.text}")

print("\n3. Запрос с правильным значением метода (POST):")
response = requests.post(base_url, data={'method': 'POST'})
print(f"POST Response code: {response.status_code}, Content: {response.text}")

print("\n4. Тестирование всех комбинаций типов запросов и значений параметров 'method':")
methods = ["GET", "POST", "PUT", "DELETE"]

for req_method in methods:
  for param_method in methods + [""]:

     print(f"\nТестирование типа запроса: {req_method}, с параметром: {param_method}")
     data = {'method': param_method} if param_method else {}

     if req_method == "GET":
        response = requests.get(base_url, params=data)
     elif req_method == "POST":
        response = requests.post(base_url, data=data)
     elif req_method == "PUT":
        response = requests.put(base_url, data=data)
     elif req_method == "DELETE":
        response = requests.delete(base_url, data=data)

     print(f"Response code: {response.status_code}, Content: {response.text}")

     if req_method != param_method and "success" in response.text:
      print(f"НЕСООТВЕТСТВИЕ: Тип запроса {req_method} и параметр {param_method} не совпадают, но сервер вернул сообщение об успешном завершении.")

     elif req_method == param_method and "Wrong method provided" in response.text:
      print(f"НЕСООТВЕТСТВИЕ: Тип запроса {req_method} и параметр {param_method}, СООТВЕТСТВУЕТ, но сервер вернул: 'WRONG METHOD'.")