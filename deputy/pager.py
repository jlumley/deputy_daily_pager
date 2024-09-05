import json
import requests

from datetime import datetime, timedelta

from deputy.auth import DeputySession


def add_employee_leave(
    session: DeputySession,
    employee_id: int,
    date_str: str,
    notify: str,
    comment: str,
):
    if not notify:
        raise ValueError("Notify list is required")

    api_url = f"https://{session.endpoint}/api/v1/my/leave"
    headers = {
        "Authorization": f"Bearer {session.access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
    }
    payload = {
        "Id": 0,
        "Employee": 1337,
        "DateStart": date_str,
        "DateEnd": date_str,
        "LeaveRule": "31",
        "Comment": comment,
        "Notify": [notify],
        "StartHour": 0,
        "StartMinute": 0,
        "EndHour": 1,
        "EndMinute": 0,
        "Status": 0,
    }
    response = requests.post(
        api_url, headers=headers, data=json.dumps(payload), allow_redirects=True  # noqa
    )

    response.raise_for_status()
    leave_request = response.json().get("Id")
    print(f"Leave request {leave_request} added successfully for {date_str}")


def submit_daily_pager(
    session: DeputySession,
    employee_id: int,
    start_date: str,
    duration: int,
    notify: str,
    comment: str,
    dry_run: bool,
):
    """
    Submit daily pager for the given
    employee for the specified duration
    """
    date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    for i in range(duration):
        date_str = date_obj.strftime("%Y-%m-%d")
        print(f"Adding Leave for {date_str}")
        if not dry_run:
            add_employee_leave(
                session=session,
                employee_id=employee_id,
                date_str=date_str,
                notify=notify,
                comment=comment,
            )
        date_obj += timedelta(days=1)
