# -*- coding: utf-8 -*-
"""
Module Name: test_schedule.py

Description:
These tests use the unittest module and the mock.patch function to simulate
the behavior of the subprocess.run function when adding an event to the macOS
Calendar app using AppleScript.

Author: elreysausage

Date: 2025-01-25
"""

import unittest
from unittest.mock import patch, MagicMock

import src.schedule


class TestSchedule(unittest.TestCase):
    """
    Test suite for the schedule module.
    """
    def test_sanitize_summary(self):
        """
        Test summary text sanitization for AppleScript.
        """
        self.assertEqual(src.schedule.sanitize_summary('Test "quote"'), 'Test \\"quote\\"')
        self.assertEqual(src.schedule.sanitize_summary("Multi\nline"), "Multi line")
        self.assertEqual(src.schedule.sanitize_summary('Clean Text'), 'Clean Text')

    @patch("src.schedule.subprocess.run")
    def test_add_event(self, mock_subprocess: MagicMock) -> None:
        """
        Test adding an event to macOS Calendar using AppleScript.

        Args:
            mock_subprocess: The mocked subprocess.run function.
        """
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Success"
        src.schedule.add_event(
            summary="Test Event",
            calendar_name="Home",
            year=2025,
            month=2,
            day=10,
            start_time=10,
            end_time=11
        )
        mock_subprocess.assert_called_once()
    
    @patch("src.schedule.add_event")
    def test_add_weekly_schedule(self, mock_add_event: MagicMock) -> None:
        """
        Test adding a weekly schedule to the macOS Calendar.

        Args:
            mock_add_event: The mocked add_event function.
        """
        test_schedule_weekday = [
            ("Test Event 1", 8, 9),
            ("Test Event 2", 9, 10),
        ]
        test_schedule_weekend = [
            ("Weekend Event", 10, 11),
        ]
        location = "London"
        src.schedule.add_weekly_schedule(
            test_schedule_weekday,
            test_schedule_weekend,
            location
        )
        self.assertGreater(mock_add_event.call_count, 0)


if __name__ == "__main__":
    unittest.main()