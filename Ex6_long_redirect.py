import requests

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url, allow_redirects=True)
response.raise_for_status()
redirect_count = len(response.history)
final_url = response.url
print(f"Number of redirects: {redirect_count}")
print(f"Final URL: {final_url}")