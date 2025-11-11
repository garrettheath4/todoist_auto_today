#!/usr/bin/env python3
"""
todoist_today_scheduler.py
----------------------------------------
Sets all Todoist tasks with the '@today' label to be due today.
Requires a Todoist REST API token in the environment variable TODOIST_TOKEN.

Required Packages:
 - requests
 - tzdata
"""

import logging
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests

API_BASE = "https://api.todoist.com/rest/v2"
TOKEN = os.environ.get("TODOIST_TOKEN")
CURRENT_TIME_ZONE = os.environ.get("TZ", "America/New_York")

if not TOKEN:
    raise SystemExit("Error: TODOIST_TOKEN environment variable is not set.")

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def get_tasks_with_label(label: str) -> list[dict]:
    """Fetch all tasks containing the given label ID."""
    resp = requests.get(f"{API_BASE}/tasks", headers=HEADERS, params={"label": label})
    resp.raise_for_status()
    return resp.json()


def set_task_due_today(task: dict, today_date: date) -> None:
    """
    Set a task's due date to today (ISO format).

    Example task dict::
       {'id': '9722671294', 'project_id': '1490560962', 'content': 'Recurring task', 'description': '',
        'is_completed': False, 'labels': ['today'], 'priority': 1, 'created_at': '2025-11-11T04:36:20.496387Z',
        'due': {'date': '2025-11-09', 'string': 'every day', 'lang': 'en', 'is_recurring': True},
        'url': 'https://app.todoist.com/app/task/9722671294', 'duration': None, 'deadline': None}
    """
    post = requests.post(
        f"{API_BASE}/tasks/{task['id']}",
        headers=HEADERS,
        json={
            **({"due_string": task["due"]["string"]}
               if task["due"] and isinstance(task["due"]["string"], str) and task["due"]["is_recurring"]
               else {"due_date": today_date.isoformat()}),
        },
    )
    if post.status_code != 200:
        logging.error(f"Failed to update task %s: %s", task["id"], post.text)


def main():
    logging.debug("Fetching tasks with @today label…")
    tasks = get_tasks_with_label("today")
    if not tasks:
        logging.warning("No tasks found with the @today label.")
        return

    today_date = datetime.now(ZoneInfo(CURRENT_TIME_ZONE)).date()
    logging.info(f"Found %d tasks. Updating due dates to today (%s)…", len(tasks), today_date.isoformat())
    for task in tasks:
        logging.debug("Updating task: %s", task)
        set_task_due_today(task, today_date)
        logging.debug(f"Updated: %s", task['content'])

    logging.info("Done.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Current time zone: %s", CURRENT_TIME_ZONE)
    main()
