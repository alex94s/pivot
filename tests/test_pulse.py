# -*- coding: utf-8 -*-
"""
Module Name: test_pulse.py

Description:
This module contains unit tests for the pulse.py module to ensure the correct
functionality of the event scraping process.

Author: elreysausage

Date: 2025-01-25
"""

import unittest
from unittest.mock import patch, MagicMock

from src.pulse import (
    TimeOutScraper, 
    AtlasObscuraScraper, 
    TicketmasterScraper, 
    EventbriteScraper,
    MeetupScraper
)


class TestEventScrapers(unittest.TestCase):
    """
    Test suite for the event scraper classes.
    """
    def setUp(self):
        """
        Set up the test case with default location and date.
        """
        self.location = "london"
        self.date = "2025-02-10"

    @patch("src.pulse.requests.get")
    def test_timeout_scraper(self, mock_get: MagicMock) -> None:
        """
        Test the TimeOut event scraper.

        Args:
            mock_get: The mocked requests.get function.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body>"
            "<article>"
            "<h3>1. Sample Event</h3>"
            "<a href='/event-link'></a>"
            "<p>Event description.</p>"
            "</article>"
            "</body></html>"
        )
        mock_get.return_value = mock_response
        scraper = TimeOutScraper(self.location, self.date)
        events = scraper.get_events()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        self.assertEqual(events[0]["title"], "1. Sample Event")
        self.assertIn("description", events[0])
        self.assertIn("link", events[0])

    @patch("src.pulse.requests.get")
    def test_atlas_obscura_scraper(self, mock_get: MagicMock) -> None:
        """
        Test the Atlas Obscura event scraper.

        Args:
            mock_get: The mocked requests.get function.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body>"
            "<div class='Card__content-wrap'>"
            "<h3 class='Card__heading'><span>Hidden Spot</span></h3>"
            "<div class='Card__content js-subtitle-content'>Cool place</div>"
            "</div>"
            "</body></html>"
        )
        mock_get.return_value = mock_response
        scraper = AtlasObscuraScraper(self.location, self.date)
        events = scraper.get_events()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        self.assertEqual(events[0]["title"], "Hidden Spot")

    @patch("src.pulse.requests.get")
    def test_ticketmaster_scraper(self, mock_get: MagicMock) -> None:
        """
        Test the Ticketmaster event scraper.

        Args:
            mock_get: The mocked requests.get function.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body>"
            "<button class='sc-12yab8l-0 crscED'>"
            "<span class='VisuallyHidden-sc-8buqks-0 lmhoCy'>Concert Night</span>"
            "</button>"
            "</body></html>"
        )
        mock_get.return_value = mock_response
        scraper = TicketmasterScraper(self.location, self.date)
        events = scraper.get_events()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        self.assertEqual(events[0]["title"], "Concert Night")

    @patch("src.pulse.requests.get")
    def test_eventbrite_scraper(self, mock_get: MagicMock) -> None:
        """
        Test the Eventbrite event scraper.

        Args:
            mock_get: The mocked requests.get function.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body>"
            "<a class='event-card-link' "
            "aria-label='Tech Conference' "
            "href='/tech-event'></a>"
            "</body></html>"
        )
        mock_get.return_value = mock_response
        scraper = EventbriteScraper(self.location, self.date)
        events = scraper.get_events()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        self.assertEqual(events[0]["title"], "Tech Conference")
        self.assertIn("link", events[0])

    @patch("src.pulse.requests.get")
    def test_meetup_scraper(self, mock_get: MagicMock) -> None:
        """
        Test the Meetup event scraper.

        Args:
            mock_get: The mocked requests.get function.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body>"
            "<script type='application/ld+json'>"
            "["
            "{"
            "\"@type\": \"Event\", "
            "\"name\": \"Meetup Gathering\", "
            "\"url\": \"https://www.meetup.com/event\""
            "}"
            "]"
            "</script>"
            "</body></html>"
        )
        mock_get.return_value = mock_response
        scraper = MeetupScraper(self.location, self.date)
        events = scraper.get_events()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        self.assertEqual(events[0]["title"], "Meetup Gathering")
        self.assertIn("link", events[0])


if __name__ == "__main__":
    unittest.main()
