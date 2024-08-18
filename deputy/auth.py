import http.server
import socketserver
import os
import requests
import webbrowser

from dataclasses import dataclass
from urllib.parse import urlencode, urlparse, parse_qs

# https://developer.deputy.com/deputy-docs/docs/using-a-permanent-token#url
DEPUTY_AUTH_DOMAIN = "https://once.deputy.com"

CLIENT_ID = os.environ.get("DEPUTY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("DEPUTY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8087"
# REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
AUTH_BASE_URL = f"{DEPUTY_AUTH_DOMAIN}/my/oauth/login"
TOKEN_URL = f"{DEPUTY_AUTH_DOMAIN}/my/oauth/access_token"

oauth_code = None


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


class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global oauth_code
        # Parse the query string from the URL
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Assuming the token is passed as "access_token" in the query string
        if "code" in query_params:
            oauth_code = query_params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"OAuth token received. You can close this window."
            )  # noqa
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing access_token in the query string.")


def get_deputy_session():
    get_authorization_url()
    handler = OAuthHandler
    port = 8087
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Waiting for OAuth token on http://localhost:{port}...")
        httpd.handle_request()  # Wait for a single request

        # Retrieve the token from the handler
        httpd.server_close()

    global oauth_code
    return get_access_token(oauth_code)
