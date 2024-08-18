## Deputy Daily Pager Tool


A simple tool to make reporting daily pager easier


# Getting Started

In order to obtain an API token you'll need to set up an oauth client, this can be done [here](https://once.deputy.com/my/oauth_clients)

Give it a name, and set the redirect uri to `http://localhost:8087`

```bash
export DEPUTY_CLIENT_ID="<client_id>"
export DEPUTY_CLIENT_SECRET="<client_secret>"

pipenv install
```





# Usage

```bash
pipenv run python run.py pager --help

usage: run.py pager [-h] [--start-date START_DATE] --duration DURATION [--comment COMMENT] [--notify NOTIFY]

options:
  -h, --help            show this help message and exit
  --start-date START_DATE, -s START_DATE
                        Start date of the pager {YYYY-MM-DD}, default today
  --duration DURATION, -d DURATION
                        Number of days carrying the pager
  --comment COMMENT, -c COMMENT
                        Comment to be added to each daily pager leave request
  --notify NOTIFY, -n NOTIFY
                        Employee ID to notify, if not provided the set of all previous approvers will be notified
```

