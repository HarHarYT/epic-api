import requests

url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'

headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE='
}

account_id = input("Enter your account ID: ")
device_id = input("Enter your device ID: ")
secret = input("Enter your secret: ")

profile_data = {
    'grant_type': 'device_auth',
    'account_id': account_id,
    'device_id': device_id,
    'secret': secret
}

response = requests.post(url, headers=headers, data=profile_data)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
