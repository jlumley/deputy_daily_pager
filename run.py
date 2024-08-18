#! usr/bin/env python3
import argparse
import re
import datetime


from deputy.auth import get_deputy_session
from deputy.employee import (
    get_current_employee_id,
    get_previous_approvers,
)
from deputy.pager import submit_daily_pager


def validate_date(date_str: str):
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not pattern.match(date_str):
        raise ValueError("Invalid date format. Expected {YYYY-MM-DD}")
    return date_str


def get_default_start_date():
    today = datetime.date()
    return today.strftime("%Y-%m-%d")


def parse_args():
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
        required=True,
        help="Number of days carrying the pager",
        type=int,
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
        help="Employee ID to notify, if not provided the set of all previous approvers will be notified",  # noqa
        type=int,
    )

    return parser.parse_args()


def main():
    parser = parse_args()
    if parser.dry_run:
        print("********** Dry Run Mode **********")
    deputy_session = get_deputy_session()
    print("Access Token Successfully Obtained")

    if parser.cmd == "pager":
        employee_id = get_current_employee_id(deputy_session)
        if not parser.notify:
            parser.notify = get_previous_approvers(deputy_session)

        submit_daily_pager(
            deputy_session,
            employee_id=employee_id,
            start_date=parser.start_date,
            duration=parser.duration,
            notify=parser.notify,
            comment=parser.comment,
            dry_run=parser.dry_run,
        )


if __name__ == "__main__":
    main()
