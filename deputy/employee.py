import requests

from deputy.auth import DeputySession


def get_employee_id(session: DeputySession):
    api_url = f"https://{session.endpoint}/api/v1/me"
    headers = {
        "Authorization": f"Bearer {session.access_token}",
    }
    resp = requests.get(api_url, headers=headers)
    json_resp = resp.json()
    print(f"Current User: {json_resp['Name']}")
    print(f"Employee ID: {json_resp['EmployeeId']}")
    return int(json_resp["EmployeeId"])


def get_previous_approvers(session: DeputySession):

    previous_approvers = set()

    api_url = f"https://{session.endpoint}/api/v1/my/leave"
    headers = {
        "Authorization": f"Bearer {session.access_token}",
        "Accept": "application/json",
    }
    response = requests.get(api_url, headers=headers, allow_redirects=True)
    for leave in response.json():
        for manager in leave["NotifyManagerArray"]:
            previous_approvers.add(manager)

    return list(previous_approvers)
