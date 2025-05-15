import requests
import base64


def request_url(session, url):
    try:
        response = session.get(url)
        if response.status_code == 200:
            return response
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def post_url(session, url, data):
    try:
        response = session.post(url, data=data)
        if response.status_code == 200:
            return response
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    # Create a session
    session = requests.Session()

    # Request URL
    url = "http://124.16.75.117:51003"
    response = request_url(session, url)
    if response:
        # Get segment "Password" in response header
        password = response.headers.get("Password")
        print(password)

        # Base64 decode
        if password is None:
            print("Password not found in response headers.")
            exit(1)

        password = base64.b64decode(password).decode("utf-8")
        print(password)
        password = password[5:-1]
        print(password)
        data = {"password": str(password)}
        response = post_url(session, url, data)

        if response:
            print(response.text)
            # Get segment "Hint" in response header
            hint = response.headers.get("Hint")
            print(hint)
    else:
        print("Failed to get a valid response.")
