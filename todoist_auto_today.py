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


def set_task_due_today(task_id: str, today_date: date) -> None:
    """Set a task's due date to today (ISO format)."""
    post = requests.post(
        f"{API_BASE}/tasks/{task_id}",
        headers=HEADERS,
        json={"due_date": today_date.isoformat()},
    )
    if post.status_code != 200:
        logging.error(f"Failed to update task %s: %s", task_id, post.text)


def main():
    logging.debug("Fetching tasks with @today label…")
    tasks = get_tasks_with_label("today")
    if not tasks:
        logging.warning("No tasks found with the @today label.")
        return

    today_date = datetime.now(ZoneInfo(CURRENT_TIME_ZONE)).date()
    logging.info(f"Found %d tasks. Updating due dates to today (%s)…", len(tasks), today_date.isoformat())
    for task in tasks:
        set_task_due_today(task["id"], today_date)
        logging.debug(f"Updated: %s", task['content'])

    logging.info("Done.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Current time zone: %s", CURRENT_TIME_ZONE)
    main()
