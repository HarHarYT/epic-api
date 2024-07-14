import requests

url = 'https://api.epicgames.dev/epic/oauth/v2/tokenInfo'

headers = {
    'Host': 'api.epicgames.dev',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'Authorization': 'Basic M2UxM2M1YzU3ZjU5NGE1NzhhYmU1MTZlZWNiNjczZmU6NTMwZTMxNmMzMzdlNDA5ODkzYzU1ZWM0NGYyMmNkNjI=',
    'X-Epic-Correlation-ID': 'EOS-AE3g4dhaD0K5tAG_12660A-bVluTGHupUezdY34t7XUIA',
    'User-Agent': 'EOS-SDK/1.16.3020-34326581 (Windows/10.0.22621.3374.64bit) Fortnite/++Fortnite+Release-30.20-CL-34756525',
    'X-EOS-Version': '1.16.3020-34326581',
    'Accept-Encoding': 'identity',
    'Content-Length': '1140',
    'Authorization': 'Bearer eg1 token'
}

payload = {
    'token': 'ur token'
}


encoded_payload = '&'.join([f"{key}={value}" for key, value in payload.items()])

try:
    response = requests.post(url, headers=headers, data=encoded_payload)

    print(f"Response status code: {response.status_code}")
    print("Response body:")
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
