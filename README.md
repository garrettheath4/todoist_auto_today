# 🗓️ Todoist Auto Today
<!-- noinspection MarkdownIncorrectlyNumberedListItem -->

Automatically sets all Todoist tasks labeled `@today` to be due today.

This small Python script uses the [Todoist REST API v2](https://developer.todoist.com/rest/v2/#update-a-task)
to find all tasks with the @today label and update their due date to the current date — adjusted for your desired
timezone.

## ⚙️ How It Works

When run, the script:

1.  Connects to your Todoist account using your personal API token.
1.  Fetches all active tasks with the @today label.
1.  Sets their due date to today’s date in the specified timezone (default: America/New_York).
1.  Prints logs for each update.

It’s designed to be lightweight enough to run automatically via **Cronicle**, **cron**, or any other task scheduler.

## 🧰 Requirements

*   Python 3.9+
*   A Todoist REST API token
*   The following Python packages:
    *   requests
    *   tzdata

## 🪄 Setup

1.  Clone the repo:

    ```shell
    git clone https://github.com/garrettheath4/todoist_auto_today.git
    cd todoist_auto_today
    ```

1.  Install dependencies:

    ```shell
    pip install -r requirements.txt
    ```

    _(If you don’t have a requirements.txt, just run pip install requests tzdata.)_

1.  Set your Todoist token as an environment variable:

    ```shell
    export TODOIST_TOKEN="your_todoist_api_token"
    ```

1.  (Optional) Set your timezone:

    ```shell
    export TZ="America/New_York"
    ```

    If not set, the script defaults to America/New_York.

## ▶️ Usage

Run the script manually:

```shell
./todoist_auto_today.py
```

You’ll see output like:

```
DEBUG:root:Current time zone: America/New_York
DEBUG:root:Fetching tasks with @today label…
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.todoist.com:443
DEBUG:urllib3.connectionpool:https://api.todoist.com:443 "GET /rest/v2/tasks?label=today HTTP/1.1" 200 None
INFO:root:Found 4 tasks. Updating due dates to today (2025-11-10)…
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.todoist.com:443
DEBUG:urllib3.connectionpool:https://api.todoist.com:443 "POST /rest/v2/tasks/9722628406 HTTP/1.1" 200 554
DEBUG:root:Updated: Yesterday
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.todoist.com:443
DEBUG:urllib3.connectionpool:https://api.todoist.com:443 "POST /rest/v2/tasks/9722628471 HTTP/1.1" 200 550
DEBUG:root:Updated: Today
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.todoist.com:443
DEBUG:urllib3.connectionpool:https://api.todoist.com:443 "POST /rest/v2/tasks/9722628613 HTTP/1.1" 200 553
DEBUG:root:Updated: Tomorrow
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.todoist.com:443
DEBUG:urllib3.connectionpool:https://api.todoist.com:443 "POST /rest/v2/tasks/9722628675 HTTP/1.1" 200 552
DEBUG:root:Updated: No Date
INFO:root:Done.
```

## 🕰️ Automation

You can schedule this script to run daily using:

**Cron (Linux / macOS):**

```
0 8 * * * /path/to/todoist_auto_today.py >> /var/log/todoist_auto_today.log 2>&1
```

**Cronicle (Docker):**

*   Use a Docker image that has Cronicle, Python 3, and a Python Script Plugin for Cronicle installed, such as
    [garrettheath4/docker-cronicle-python](https://github.com/garrettheath4/docker-cronicle-python).
*   Create a “Python Script” job.
*   Command: /usr/bin/python3 /path/to/todoist_auto_today.py
*   Environment: set `TODOIST_TOKEN` and (optionally) `TZ`.
*   Schedule: every day after midnight (e.g. `12:01 AM`)
*   Python Package Requirements:
    * `requests`
    * `tzdata`

## 🧪 Example

If you have three Todoist tasks:

*   `Buy groceries @today`
*   `Email project update @today`
*   `Plan weekend trip @today`

After running this script, all three will have their due date set to `today` in Todoist.

## 🪪 License

MIT License © Garrett Heath Koller

See [LICENSE](LICENSE) for details.
