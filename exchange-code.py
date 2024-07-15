import requests


url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'


headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE='
}


exchange = input("Enter your exchange: ")

profile_data = {
    'grant_type': 'exchange_code',
    'exchange_code': exchange, 
}


response = requests.post(url, headers=headers, data=profile_data)


if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
