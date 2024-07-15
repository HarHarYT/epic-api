# this is a device code gen that sends a message to the user when the verify

import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Function to send email notification
def send_email(email, display_name):
    sender_email = ""  # Replace with your email address
    receiver_email = email
    password = ""  # Replace with your email password

    message = MIMEMultipart("alternative")
    message["Subject"] = "New Login Notification"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Hello {display_name},\n\nYou have logged in to a new client."
    html = f"""\
    <html>
      <body>
        <p>Hello {display_name},<br><br>
           You have logged in to a new client.<br><br>
           Best regards,<br>
           Your App
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.example.com", 465) as server:  # Replace with your SMTP server details
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email notification sent successfully to {receiver_email}")
    except Exception as e:
        print(f"An error occurred while sending email: {str(e)}")

# Endpoint URLs and headers
token_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
device_auth_url = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization"

token_payload = "grant_type=client_credentials"
token_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
}

# Step 1: Get Access Token
token_response = requests.post(token_url, data=token_payload, headers=token_headers, verify=False)
print("Token Request Status Code:", token_response.status_code)
print("Token Request Response:", token_response.json())

if token_response.status_code == 200:
    access_token = token_response.json().get("access_token")
    print("Access Token:", access_token)

    # Step 2: Device Authorization
    device_auth_payload = {"prompt": "login"}
    device_auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    device_auth_response = requests.post(device_auth_url, data=device_auth_payload, headers=device_auth_headers, verify=False)
    print("Device Auth Request Status Code:", device_auth_response.status_code)
    print("Device Auth Request Response:", device_auth_response.json())

    if device_auth_response.status_code == 200:
        device_code = device_auth_response.json().get("device_code")
        verification_uri = device_auth_response.json().get("verification_uri")
        user_code = device_auth_response.json().get("user_code")

        print(f"https://www.epicgames.com/id/activate?userCode={user_code}")

        # Polling loop to check if user has authorized
        while True:
            try:
                time.sleep(5)

                # Step 3: Exchange Device Code for Access Token
                token_exchange_response = requests.post(token_url, data={
                    'grant_type': 'device_code',
                    'device_code': device_code,
                    'token_type': 'eg1'
                }, headers={
                    'Authorization': token_headers['Authorization'],
                    'Content-Type': 'application/x-www-form-urlencoded'
                }, verify=False)
                print("Token Exchange Status Code:", token_exchange_response.status_code)
                print("Token Exchange Response:", token_exchange_response.json())

                if token_exchange_response.status_code == 200:
                    logged_in_data = token_exchange_response.json()

                    # Step 4: Get User Information using accid
                    accid = logged_in_data.get('account_id')
                    user_info_url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{accid}"

                    user_info_headers = {
                        "Authorization": f"Bearer {logged_in_data['access_token']}"
                    }

                    user_info_response = requests.get(user_info_url, headers=user_info_headers)
                    print("User Info Request Status Code:", user_info_response.status_code)
                    print("User Info Request Response:", user_info_response.json())

                    if user_info_response.status_code == 200:
                        user_info = user_info_response.json()
                        email = user_info.get('email')
                        display_name = user_info.get('displayName')

                        # Step 5: Send Email Notification
                        send_email(email, display_name)

                        print("Logged in as:", display_name)
                        print("User Info:", user_info)
                        break  # Exit polling loop
                    else:
                        print("Failed to get user information:", user_info_response.status_code)
                else:
                    print("Failed to exchange device code for access token:", token_exchange_response.status_code)

            except Exception as e:
                print("An error occurred:", str(e))

    else:
        print("Failed to get device code:", device_auth_response.status_code)

else:
    print("Failed to get access token:", token_response.status_code)
