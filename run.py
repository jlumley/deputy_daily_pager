#! usr/bin/env python3
import argparse
import json
import re
import requests

from datetime import datetime, date, timedelta

from daily_pager.auth import get_deputy_session, DeputySession


def validate_date(date_str: str):
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not pattern.match(date_str):
        raise ValueError("Invalid date format. Expected {YYYY-MM-DD}")
    return date_str


def parse_args():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(dest="cmd")

    daily_pager = sub_parser.add_parser("pager", help="Add Daily Pager")
    daily_pager.add_argument(
        "--start-date",
        "-s",
        required=True,
        help="Start date of the pager {YYYY-MM-DD}",
        type=validate_date,
    )
    daily_pager.add_argument(
        "--duration",
        "-d",
        required=True,
        help="number of days carrying the pager",
        type=int,
    )
    daily_pager.add_argument(
        "--dry-run",
        help="Do not submit the pager",
        default=False,
        action="store_true",
    )

    return parser.parse_args()


def get_employee(session: DeputySession):
    api_url = f"https://{session.endpoint}/api/v1/my/employee/me"
    headers = {
        "Authorization": f"Bearer {session.access_token}",
    }
    response = requests.get(api_url, headers=headers)
    print(response)
    print(response.content)


# {
#     "Id": 0,
#     "Employee": 1337,
#     "DateStart": "2024-08-05",
#     "DateEnd": "2024-08-05",
#     "LeaveRule": "31",
#     "Comment": "na",
#     "Notify": ["764"],
#     "StartHour": 0,
#     "StartMinute": 0,
#     "EndHour": 1,
#     "EndMinute": 0,
#     "Status": 0,
# }

# notify Danny = 764


def add_employee_leave(
    session: DeputySession,
    employee_id: int,
    date_str: str,
    notify: str,
    comment: str,
):
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
    print(f"Leave added successfully for {date_str}")


def submit_daily_pager(
    session: DeputySession,
    employee_id: int,
    start_date: str,
    duration: int,
    notify: str,
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
                comment="Daily Pager",
            )
        date_obj += timedelta(days=1)


def main():
    parser = parse_args()
    if parser.dry_run:
        access_token = "dummy"
        print("Dry Run Mode")
    else:
        access_token = get_deputy_session()
        print("Access Token Successfully Obtained")

    if parser.cmd == "pager":
        submit_daily_pager(
            access_token,
            employee_id=1337,
            start_date=parser.start_date,
            duration=parser.duration,
            notify="764",
            dry_run=parser.dry_run,
        )


if __name__ == "__main__":
    main()
