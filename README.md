## Deputy Daily Pager Tool


A simple tool to make reporting daily pager easier



# Usage


```bash
pipenv run python run.py pager --help

usage: run.py pager [-h] --start-date START_DATE --duration DURATION [--notify NOTIFY]

options:
  -h, --help            show this help message and exit
  --start-date START_DATE, -s START_DATE
                        Start date of the pager {YYYY-MM-DD}
  --duration DURATION, -d DURATION
                        number of days carrying the pager
  --notify NOTIFY, -n NOTIFY
                        Employee ID to notify, if not provided the set of all previous approvers will be notified
```

