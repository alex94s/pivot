# -*- coding: utf-8 -*
"""
Module Name: pulse.py

Description:
This module provides event scraping functionality for various websites to 
gather event information. It includes scrapers for TimeOut, Atlas Obscura, 
Ticketmaster, Eventbrite, and Meetup.

Author: elreysausage

Date: 2025-01-25
"""

import json
import random
import re
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class EventScraper(ABC):
    """
    Abstract class for event scrapers.
    """
    def __init__(self, location: str, date: str):
        """
        Initialize the event scraper with the location and date.
        
        Args:
            location: The location for which to fetch events.
            date: The date for which to fetch events.
        """
        self.location = location.lower().replace(" ", "-")
        self.date = date

    def fetch_page(self):
        """
        Fetch the HTML content of the page.

        Returns:
            BeautifulSoup: Parsed HTML content.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        response = requests.get(self.base_url, headers=headers)

        if response.status_code != 200:
            return None

        return BeautifulSoup(response.text, "html.parser")

    @abstractmethod
    def get_events(self):
        """
        Abstract method to be implemented by subclasses to fetch events.
        """
        pass

    @staticmethod
    def get_random_scraper(location: str, date: str):
        """
        Selects a random scraper from the available scrapers.

        Args:
            location: The location for which to fetch events.
            date: The date for which to fetch events.

        Returns:
            EventScraper: An instance of a randomly chosen scraper.
        """
        scrapers = [
            TimeOutScraper, 
            AtlasObscuraScraper, 
            TicketmasterScraper,
            EventbriteScraper,
            MeetupScraper
        ]
        chosen_scraper = random.choice(scrapers)
        return chosen_scraper(location, date)


class TimeOutScraper(EventScraper):
    """
    Scraper for TimeOut events.
    """
    def __init__(self, location: str, date: str):
        """
        Initialize the TimeOut scraper with the location and date.
        
        Args:
            location: The location for which to fetch events.
            date: The date for which to fetch events.
        """
        super().__init__(location, date)
        self.base_url = (
            f"https://www.timeout.com/{self.location}/things-to-do/"
            f"things-to-do-in-{self.location}-this-week"
        )

    def get_events(self):
        """
        Fetch today's events from TimeOut for the specified location.

        Returns:
            events: A list of dictionaries containing event details.
        """
        soup = self.fetch_page()
        if not soup:
            return f"Failed to fetch data for {self.location}"

        events = []

        for card in soup.find_all("article"):
            title_tag = card.find("h3")
            link_tag = card.find("a", href=True)
            desc_tag = card.find("p")

            title = title_tag.text.strip() if title_tag else "Unknown Event"
            link = link_tag["href"] if link_tag else ""
            description = desc_tag.text.strip() if desc_tag else "No description available."

            if title and title[0].isdigit():
                events.append({
                    "title": title,
                    "description": description,
                    "link": f"https://www.timeout.com{link}" if link else ""
                })

        return events


class AtlasObscuraScraper(EventScraper):
    """
    Scraper for Atlas Obscura places.
    """
    def __init__(self, location: str, date: str):
        """
        Initialize the Atlas Obscura scraper with the location and date.

        Args:
            location: The location for which to fetch events.
            date: The date for which to fetch events.
        """
        super().__init__(location, date)
        self.base_url = (
            f"https://www.atlasobscura.com/things-to-do/{self.location}/places?"
            f"page={random.randint(1, 5)}"
        )

    def get_events(self):
        """
        Fetch places from Atlas Obscura for the specified location.

        Returns:
            events: A list of dictionaries containing place details.
        """
        soup = self.fetch_page()
        if not soup:
            return f"Failed to fetch data for {self.location}"

        events = []

        for card in soup.find_all("div", class_="Card__content-wrap"):
            name_tag = card.find("h3", class_="Card__heading")
            name = name_tag.find("span").text.strip()
            desc_tag = card.find("div", class_="Card__content js-subtitle-content")
            description = desc_tag.text.strip() if desc_tag else "No description available."
            link_tag = name_tag.find("a", href=True) if name_tag else None
            link = f"https://www.atlasobscura.com{link_tag['href']}" if link_tag else ""

            events.append({
                "title": name,
                "description": description,
                "link": link
            })

        return events


class TicketmasterScraper(EventScraper):
    """
    Scraper for Ticketmaster events based on location and date.
    """
    def __init__(self, location: str, date: str):
        """
        Initialize the Ticketmaster scraper with the location and date.

        Args:
            location: The location for which to fetch events.
            date: The date for which to fetch events.
        """
        super().__init__(location, date)
        self.base_url = (
            "https://www.ticketmaster.co.uk/search?"
            f"q={self.location}&sort=date"
            f"&startDate={self.date}&endDate={self.date}"
        )

    def get_events(self):
        """
        Scrape Ticketmaster for events.

        Returns:
            events: A list of dictionaries containing event details.
        """
        soup = self.fetch_page()
        events = []
        for button in soup.find_all("button", class_="sc-12yab8l-0 crscED"):
            spans = button.find_all("span", class_="VisuallyHidden-sc-8buqks-0 lmhoCy")
            if spans:
                event_title = " ".join(span.text.strip() for span in spans)
                event_title = event_title.replace("Open additional information for ", "").strip()
                event_title = re.sub(r"(.+?) \1", r"\1", event_title)
                events.append({
                    "title": event_title
                })
        return events


class EventbriteScraper(EventScraper):
    """
    Scraper for Eventbrite events based on location and date.
    """
    def __init__(self, location: str, date: str):
        """
        Initialize the Eventbrite scraper with the location and date.

        Args:
            location: The location for which to fetch events.
            date: The date for which to fetch events.
        """
        super().__init__(location, date)
        self.base_url = (
            f"https://www.eventbrite.co.uk/d/united-kingdom--{self.location}/all-events/"
        )

    def get_events(self):
        """
        Scrape Eventbrite for events.

        Returns:
            events: A list of dictionaries containing event details.
        """
        soup = self.fetch_page()
        event_cards = soup.find_all("a", class_="event-card-link")
        events = []
        seen_titles = set()
        for event in event_cards:
            event_name = event.get("aria-label", "No title").replace("View ", "").strip()
            event_link = event.get("href", "#")
            if event_name not in seen_titles:
                seen_titles.add(event_name)
                events.append({
                    "title": event_name,
                    "link": event_link
                })
        return events


class MeetupScraper(EventScraper):
    """
    Scraper for Meetup events based on location and date.
    """
    def __init__(self, location: str, date: str):
        """
        Initialize the Meetup scraper with the location and date.

        Args:
            location: The location for which to fetch events.
            date: The date for which to fetch events.
        """
        super().__init__(location, date)
        self.base_url = (
            f"https://www.meetup.com/find/gb--17--{location}/"
        )

    def get_events(self):
        """
        Scrape Meetup for events.

        Returns:
            events: A list of dictionaries containing event details.
        """
        soup = self.fetch_page()
        script_tags = soup.find_all("script", {"type": "application/ld+json"})
        events = []

        for tag in script_tags:
            try:
                data = json.loads(tag.string)
                if isinstance(data, list):
                    for event in data:
                        if event.get("@type") == "Event":
                            events.append(
                                {"title": event.get("name"), 
                                 "link": event.get("url")}
                            )
                elif data.get("@type") == "Event":
                    events.append(
                        {"title": data.get("name"), 
                         "link": data.get("url")}
                    )
            except json.JSONDecodeError:
                continue

        return events
