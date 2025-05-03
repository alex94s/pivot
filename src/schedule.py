# -*- coding: utf-8 -*
"""
Module Name: schedule.py

Description:
This script adds events to the macOS Calendar app using AppleScript, 
including dynamic suggestions. It creates a user-defined weekly schedule 
with a nudge appended to the end of each day, as well as a random event 
from a location-specific event scraper on weekends.

Author: elreysausage

Date: 2025-01-25
"""

import datetime
import os
import random
import subprocess

from src.nudge import generate_nudge
from src.pulse import EventScraper


def list_calendar_names() -> None:
    """
    List all calendar names in the macOS Calendar app.
    """
    apple_script = """
    tell application "Calendar"
        name of calendars
    end tell
    """
    result = subprocess.run(
        ["osascript", "-e", apple_script], capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Available calendars:")
        print(result.stdout.strip())
    else:
        print(f"Failed to list calendars. Error: {result.stderr.strip()}")
        

def sanitize_summary(summary: str) -> str:
    """
    Sanitizes the summary text for AppleScript.
    - Replaces newlines with spaces.
    - Escapes double quotes.

    Args:
        summary: The summary text to sanitize.

    Returns:
        str: The sanitized summary text
    """
    return summary.replace("\n", " ").replace('"', '\\"')


def add_event(
        summary: str,
        calendar_name: str,
        year: int,
        month: str,
        day: int,
        start_time: int,
        end_time: int
) -> None:
    """
    Add an event to Apple Calendar with dynamic times.

    Args:
        summary: The event summary.
        calendar_name: The calendar name.
        year: The year of the event.
        month: The month of the event.
        day: The day of the event.
        start_time: The start time of the event.
        end_time: The end time of the event.
    """
    sanitized_summary = sanitize_summary(summary)
    apple_script = f"""
    tell application "Calendar"
        tell calendar "{calendar_name}"
            set start_date to (current date)
            set year of start_date to {year}
            set month of start_date to {month}
            set day of start_date to {day}
            set time of start_date to ({start_time} * hours)
            
            set end_date to (current date)
            set year of end_date to {year}
            set month of end_date to {month}
            set day of end_date to {day}
            set time of end_date to ({end_time} * hours)
            
            make new event at end with properties ¬
                {{summary: "{sanitized_summary}", ¬
                start date: start_date, ¬
                end date: end_date}}
        end tell
    end tell
    """
    result = subprocess.run(
        ["osascript", "-e", apple_script], capture_output=True, text=True
    )
    if result.returncode == 0:
        print(
            f"Event '{summary}' added successfully to calendar '{calendar_name}'!")
    else:
        print(
            f"Failed to add event '{summary}'. Error: {result.stderr.strip()}")


def add_weekly_schedule(
        schedule_weekday: list, 
        schedule_weekend: list, 
        location: str,
        preferences: list | None
) -> None:
    """
    Add a weekly schedule of events to the macOS Calendar app, including dynamic nudges.

    Args:
        schedule_weekday: A list of tuples containing the user-defined weekday schedule.
        schedule_weekend: A list of tuples containing the user-defined weekend schedule.
        location: The city or location for the event scraper.
        preferences: A list of preferred categories for prompts.
    """
    today = datetime.date.today()
    next_monday = today + datetime.timedelta(days=-today.weekday() + 7)
    last_event_title = None 

    for i in range(7):
        print(f"Adding events for {next_monday + datetime.timedelta(days=i)}")
        current_date = next_monday + datetime.timedelta(days=i)
        year = current_date.year
        month = current_date.strftime("%B")
        day = current_date.day
        day_of_week = current_date.weekday()
        schedule = schedule_weekend if day_of_week >= 5 else schedule_weekday
        for summary, start_time, end_time in schedule:
            add_event(
                summary=summary,
                calendar_name="Home",
                year=year,
                month=month,
                day=day,
                start_time=start_time,
                end_time=end_time
            )
        if day_of_week >= 5:
            scraper = EventScraper.get_random_scraper(location, current_date)
            events = scraper.get_events()
            if events:
                random.shuffle(events)
                event = next((e for e in events if e["title"] != last_event_title), events[0])
                last_event_title = event["title"]
                add_event(
                    summary=(
                        event["title"] + " - " + 
                        event.get("description", event.get("link", ""))
                    ),
                    calendar_name="Home",
                    year=year,
                    month=month,
                    day=day,
                    start_time=18,
                    end_time=20
                )
        nudge = generate_nudge(
            openai_api_key = os.environ.get("OPENAI_API_KEY"),
            location=location,
            preferences=preferences
        )
        add_event(
            summary=nudge,
            calendar_name="Home",
            year=year,
            month=month,
            day=day,
            start_time=20,
            end_time=22
        )


if __name__ == "__main__":
    add_weekly_schedule(
        schedule_weekday = [
            ("Budget", 8, 8.5),
            ("Calories", 8.5, 9),
            ("Home", 9, 9.5),
            ("Enhancements", 9.5, 10),
            ("Career", 10, 16),
            ("Calories", 16, 16.5),
            ("Read", 16.5, 17),
            ("Goals", 17, 17.5),
            ("Calories", 17.5, 18),
            ("Athletics", 18, 20),
        ],
        schedule_weekend = [
            ("Budget", 10, 10.5),
            ("Calories", 10.5, 11),
            ("Home", 11, 11.5),
            ("Enhancements", 11.5, 12),
            ("Athletics", 12, 14),
            ("Career", 14, 16),
            ("Calories", 16, 16.5),
            ("Read", 16.5, 17),
            ("Goals", 17, 17.5),
            ("Calories", 17.5, 18),
        ],
        location="London",
        preferences=[
            "intellectual", 
            "social", 
            "physical",
            "exploration",
            "technology",
            "music",
        ]
    )
