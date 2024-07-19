#! usr/bin/env python3
import requests
import webbrowser

from dataclasses import dataclass
from urllib.parse import urlencode

# https://developer.deputy.com/deputy-docs/docs/using-a-permanent-token#url
DEPUTY_AUTH_DOMAIN = "https://once.deputy.com"

CLIENT_ID = "fbe26525c35c80a441191a9b57b43b0b2e2ecfdc"
CLIENT_SECRET = "b3d7d6f32cc3d237bb415d645b6d42f7797c38e6"
REDIRECT_URI = "http://localhost"
# REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
AUTH_BASE_URL = f"{DEPUTY_AUTH_DOMAIN}/my/oauth/login"
TOKEN_URL = f"{DEPUTY_AUTH_DOMAIN}/my/oauth/access_token"

print(DEPUTY_AUTH_DOMAIN)


@dataclass
class DeputySession:
    endpoint: str
    access_token: str


def get_authorization_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "longlife_refresh_token",
    }
    url = f"{AUTH_BASE_URL}?{urlencode(params)}"
    webbrowser.open_new_tab(url)


def get_access_token(auth_code) -> DeputySession:
    data = {
        "grant_type": "authorization_code",
        "scope": "longlife_refresh_token",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()
    response_data = response.json()
    return DeputySession(
        access_token=response_data.get("access_token"),
        endpoint=response_data.get("endpoint"),
    )


def get_employee_timesheets(session: DeputySession):
    api_url = f"https://{session.endpoint}/api/v1/resource/Timesheet/QUERY"
    headers = {
        "Authorization": f"Bearer {session.access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    query = {"search": {"s1": {"field": "Employee", "type": "eq", "data": 1}}}
    response = requests.post(api_url, headers=headers, data=query, allow_redirects=True)
    print(response)
    print(response.content)


def main():
    get_authorization_url()
    auth_code = input("Enter the authorization code: ")
    access_token = get_access_token(auth_code)
    get_employee_timesheets(access_token)


if __name__ == "__main__":
    main()
