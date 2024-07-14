import requests
import time

token_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
token_payload = "grant_type=client_credentials"
token_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
}

token_response = requests.post(token_url, data=token_payload, headers=token_headers, verify=False)

if token_response.status_code == 200:
    access_token = token_response.json().get("access_token")
    print("Access Token:", access_token)

    device_auth_url = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization"
    device_auth_payload = {"prompt": "login"}
    device_auth_headers = {
        "Authorization": f"bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    device_auth_response = requests.post(device_auth_url, data=device_auth_payload, headers=device_auth_headers, verify=False)

    if device_auth_response.status_code == 200:
        device_code = device_auth_response.json().get("device_code")
        verification_uri = device_auth_response.json().get("verification_uri")
        user_code = device_auth_response.json().get("user_code")

        print(f"https://www.epicgames.com/id/activate?userCode={user_code}")

        rqstatus = 0
        stopped = False
        logged_in_data = None
        accid, deviceid, secret = None, None, None

        def save_login(logged_in_data, accid, deviceid, secret):
            # This function should save login details to your preferred storage
            # Implement saving logic here
            print(f"Logged in as {logged_in_data['displayName']}")
            print(f"Account ID: {accid}, Device ID: {deviceid}, Secret: {secret}")

        while not stopped:
            try:
                time.sleep(5)
                if stopped:
                    print("Stopped interval")
                    break

                response = requests.post(token_url, data={
                    'grant_type': 'device_code',
                    'device_code': device_code,
                    'token_type': 'eg1'
                }, headers={
                    'Authorization': token_headers['Authorization'],
                    'Content-Type': 'application/x-www-form-urlencoded'
                }, verify=False)

                if response.status_code == 200:
                    logged_in_data = response.json()
                    print(logged_in_data)
                    rqstatus = 1
                    stopped = True

                    device_auth_response = requests.post(f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{logged_in_data['account_id']}/deviceAuth", headers={
                        'Authorization': f"Bearer {logged_in_data['access_token']}"
                    }, verify=False)

                    if device_auth_response.status_code == 200:
                        device_auth_data = device_auth_response.json()
                        accid = device_auth_data['accountId']
                        deviceid = device_auth_data['deviceId']
                        secret = device_auth_data['secret']
                        rqstatus = 2
                        save_login(logged_in_data, accid, deviceid, secret)
                    else:
                        print("Failed to get device auth data:", device_auth_response.status_code)
                else:
                    print("Failed to get logged in data:", response.status_code)

            except Exception as e:
                print("An error occurred:", str(e))

    else:
        print("Failed to get device code:", device_auth_response.status_code)

else:
    print("Failed to get access token:", token_response.status_code)
