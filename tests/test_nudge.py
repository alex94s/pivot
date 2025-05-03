# -*- coding: utf-8 -*-
"""
Module Name: test_nudge.py

Description:
This module contains unit tests for the nudge.py module to ensure the correct
functionality of the nudge generation process.

Author: elreysausage

Date: 2025-01-25
"""

import unittest
from unittest.mock import patch, MagicMock

import src.nudge


class TestNudge(unittest.TestCase):
    """
    Test suite for the nudge module.
    """
    def test_get_random_prompt(self):
        """
        Test that get_random_prompt returns a valid prompt.
        """
        location = "London"
        prompt = src.nudge.get_random_prompt(
            location, 
            preferences=None
        )
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    @patch("openai.ChatCompletion.create")
    def test_generate_nudge(self, mock_openai: MagicMock) -> None:
        """
        Test generating a nudge using OpenAI API.

        Args:
            mock_openai: The mocked ChatCompletion.create function.
        """
        mock_openai.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Try watching a foreign film without subtitles."
                    }
                }
            ]
        }
        api_key = "fake_api_key"
        location = "New York"
        result = src.nudge.generate_nudge(api_key, location)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertEqual(result, "Try watching a foreign film without subtitles.")

        mock_openai.assert_called_once()
        _, kwargs = mock_openai.call_args
        self.assertIn("messages", kwargs)
        self.assertIn("model", kwargs)
        self.assertEqual(kwargs["model"], "gpt-4")

    @patch("openai.ChatCompletion.create", side_effect=Exception("API error"))
    def test_generate_nudge_failure(self, mock_openai: MagicMock) -> None:
        """
        Test handling of API failure.

        Args:
            mock_openai: The mocked ChatCompletion.create function.
        """
        api_key = "fake_api_key"
        location = "Paris"
        result = src.nudge.generate_nudge(api_key, location)

        self.assertIsNone(result)
        mock_openai.assert_called_once()


if __name__ == "__main__":
    unittest.main()
