#!/usr/bin/env python3
import argparse
import datetime
import os
import re


from deputy.auth import get_deputy_session
from deputy.employee import (
    get_current_employee_id,
    get_previous_approvers,
)
from deputy.pager import submit_daily_pager

DEFAULT_NOTIFY = os.environ.get("DEPUTY_DEFAULT_NOTIFY")
DEFAULT_DURATION = os.environ.get("DEPUTY_DEFAULT_DURATION")


def validate_date(date_str: str):
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not pattern.match(date_str):
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
    return date_str


def get_default_start_date():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")


def get_default_duration():
    if DEFAULT_DURATION is None:
        return 7
    try:
        duration = int(DEFAULT_DURATION)
    except ValueError as exc:
        raise ValueError("DEPUTY_DEFAULT_DURATION must be an integer.") from exc
    if duration <= 0:
        raise ValueError("DEPUTY_DEFAULT_DURATION must be greater than zero.")
    return duration


def validate_positive_int(value: str):
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError("Duration must be an integer.") from exc
    if number <= 0:
        raise ValueError("Duration must be greater than zero.")
    return number


def parse_notify_list(value):
    if value is None:
        return None
    if isinstance(value, list):
        return value
    ids = []
    for chunk in str(value).split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            ids.append(int(chunk))
        except ValueError as exc:
            raise ValueError(
                "Notify must be a comma-separated list of employee IDs."
            ) from exc
    return ids


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--dry-run",
        help="Do not submit the pager",
        default=False,
        action="store_true",
    )

    sub_parser = parser.add_subparsers(dest="cmd", required=True)

    # Daily Pager Sub Command
    daily_pager = sub_parser.add_parser(
        "pager", help="Add Daily Pager Leave Request"
    )  # noqa
    daily_pager.add_argument(
        "--start-date",
        "-s",
        help="Start date of the pager {YYYY-MM-DD}, default today",
        default=get_default_start_date(),
        type=validate_date,
    )
    daily_pager.add_argument(
        "--duration",
        "-d",
        help="Number of days carrying the pager",
        default=get_default_duration(),
        type=validate_positive_int,
    )
    daily_pager.add_argument(
        "--comment",
        "-c",
        help="Comment to be added to each daily pager leave request",  # noqa
        type=str,
        default="Daily Pager",
    )
    daily_pager.add_argument(
        "--notify",
        "-n",
        help=(
            "Comma-separated employee IDs to notify. "
            "If not provided, previous approvers will be notified."
        ),
        default=DEFAULT_NOTIFY,
        type=str,
    )

    return parser.parse_args(args)


def main():
    parser = parse_args()
    if parser.dry_run:
        print("********** Dry Run Mode **********")
    deputy_session = get_deputy_session()
    print("Access Token Successfully Obtained")

    if parser.cmd == "pager":
        employee_id = get_current_employee_id(deputy_session)
        notify_list = parse_notify_list(parser.notify)
        if not notify_list:
            notify_list = get_previous_approvers(deputy_session)
        if not notify_list:
            raise ValueError(
                "No notify targets found. Use --notify or set "
                "DEPUTY_DEFAULT_NOTIFY."
            )

        submit_daily_pager(
            deputy_session,
            employee_id=employee_id,
            start_date=parser.start_date,
            duration=parser.duration,
            notify=notify_list,
            comment=parser.comment,
            dry_run=parser.dry_run,
        )


if __name__ == "__main__":
    main()
