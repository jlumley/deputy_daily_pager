#! usr/bin/env python3
import argparse
import re


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


def parse_args():
    parser = argparse.ArgumentParser()
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
        approvers = parser.notify
        if not approvers:
            approvers = get_previous_approvers(deputy_session)

        submit_daily_pager(
            deputy_session,
            employee_id=employee_id,
            start_date=parser.start_date,
            duration=parser.duration,
            notify=approvers,
            dry_run=parser.dry_run,
        )


if __name__ == "__main__":
    main()
