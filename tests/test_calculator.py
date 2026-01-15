# coding=utf-8
# flake8: noqa
# pylint: disable=line-too-long
"""Unit tests for the calculator module."""

from __future__ import absolute_import

import time
from collections import deque
from unittest import TestCase

from octoprint_temp_eta import calculator


class TestCalculateLinearETA(TestCase):
    """Test cases for calculate_linear_eta function."""

    def test_insufficient_data_empty_history(self):
        """Test with empty history returns None."""
        history = deque()
        result = calculator.calculate_linear_eta(history, 60.0)
        self.assertIsNone(result)

    def test_insufficient_data_single_sample(self):
        """Test with single sample returns None."""
        history = deque([(time.time(), 20.0, 60.0)])
        result = calculator.calculate_linear_eta(history, 60.0)
        self.assertIsNone(result)

    def test_invalid_target_nan(self):
        """Test with NaN target returns None."""
        now = time.time()
        history = deque([(now - 1, 20.0, 60.0), (now, 22.0, 60.0)])
        result = calculator.calculate_linear_eta(history, float("nan"))
        self.assertIsNone(result)

    def test_invalid_target_inf(self):
        """Test with infinite target returns None."""
        now = time.time()
        history = deque([(now - 1, 20.0, 60.0), (now, 22.0, 60.0)])
        result = calculator.calculate_linear_eta(history, float("inf"))
        self.assertIsNone(result)

    def test_invalid_window_seconds(self):
        """Test with invalid window_seconds returns None."""
        now = time.time()
        history = deque([(now - 1, 20.0, 60.0), (now, 22.0, 60.0)])
        result = calculator.calculate_linear_eta(history, 60.0, window_seconds=-1.0)
        self.assertIsNone(result)

    def test_invalid_data_in_history(self):
        """Test that invalid data points are skipped."""
        now = time.time()
        history = deque(
            [
                (now - 10, 0.0, 60.0),
                (now - 9, float("nan"), 60.0),  # Invalid temp
                (now - 8, 4.0, 60.0),
                (now - 7, 6.0, 60.0),
                (now - 6, 8.0, 60.0),
                (now - 5, 10.0, 60.0),
                (now - 4, 12.0, 60.0),
                (now - 3, 14.0, 60.0),
                (now - 2, 16.0, 60.0),
                (now - 1, 18.0, 60.0),
                (now, 20.0, 60.0),
            ]
        )
        result = calculator.calculate_linear_eta(history, 60.0)
        # Should still work by skipping invalid data
        self.assertIsNotNone(result)

    def test_heating_linear(self):
        """Test linear heating calculation."""
        now = time.time()
        # Heating from 20°C to 60°C at 2°C/s
        history = deque(
            [
                (now - 10, 0.0, 60.0),
                (now - 9, 2.0, 60.0),
                (now - 8, 4.0, 60.0),
                (now - 7, 6.0, 60.0),
                (now - 6, 8.0, 60.0),
                (now - 5, 10.0, 60.0),
                (now - 4, 12.0, 60.0),
                (now - 3, 14.0, 60.0),
                (now - 2, 16.0, 60.0),
                (now - 1, 18.0, 60.0),
                (now, 20.0, 60.0),
            ]
        )
        result = calculator.calculate_linear_eta(history, 60.0)
        # Should be around 20 seconds (40°C remaining / 2°C/s)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertGreater(result, 15.0)
        self.assertLess(result, 25.0)

    def test_already_at_target(self):
        """Test when already at target returns None."""
        now = time.time()
        history = deque(
            [
                (now - 2, 60.0, 60.0),
                (now - 1, 60.0, 60.0),
                (now, 60.0, 60.0),
            ]
        )
        result = calculator.calculate_linear_eta(history, 60.0)
        self.assertIsNone(result)

    def test_cooling_returns_none(self):
        """Test cooling (negative rate) returns None."""
        now = time.time()
        history = deque(
            [
                (now - 2, 62.0, 60.0),
                (now - 1, 61.0, 60.0),
                (now, 60.0, 60.0),
            ]
        )
        result = calculator.calculate_linear_eta(history, 65.0)
        self.assertIsNone(result)


class TestCalculateExponentialETA(TestCase):
    """Test cases for calculate_exponential_eta function."""

    def test_insufficient_data(self):
        """Test with insufficient data returns None."""
        history = deque()
        result = calculator.calculate_exponential_eta(history, 60.0)
        self.assertIsNone(result)

    def test_invalid_target_nan(self):
        """Test with NaN target returns None."""
        now = time.time()
        history = deque([(now - 1, 20.0, 60.0), (now, 22.0, 60.0)])
        result = calculator.calculate_exponential_eta(history, float("nan"))
        self.assertIsNone(result)

    def test_invalid_window_seconds(self):
        """Test with invalid window_seconds returns None."""
        now = time.time()
        history = deque([(now - 1, 20.0, 60.0), (now, 22.0, 60.0)])
        result = calculator.calculate_exponential_eta(history, 60.0, window_seconds=0.0)
        self.assertIsNone(result)

    def test_fallback_to_linear(self):
        """Test fallback to linear with minimal data."""
        now = time.time()
        # Only 4 samples - should fallback to linear
        history = deque(
            [
                (now - 3, 20.0, 60.0),
                (now - 2, 22.0, 60.0),
                (now - 1, 24.0, 60.0),
                (now, 26.0, 60.0),
            ]
        )
        result = calculator.calculate_exponential_eta(history, 60.0)
        # Should still get a result via fallback
        self.assertIsNotNone(result)
        assert result is not None

    def test_exponential_heating(self):
        """Test exponential heating calculation."""
        now = time.time()
        # Simulated exponential approach
        history = deque()
        for i in range(30):
            t = now - (30 - i)
            # Asymptotic approach: starts fast, slows down
            temp = 60.0 - 40.0 * (0.95**i)
            history.append((t, temp, 60.0))

        result = calculator.calculate_exponential_eta(history, 60.0)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertGreater(result, 0.0)


class TestCalculateCooldownLinearETA(TestCase):
    """Test cases for calculate_cooldown_linear_eta function."""

    def test_insufficient_data(self):
        """Test with insufficient data returns None."""
        history = deque()
        result = calculator.calculate_cooldown_linear_eta(history, 30.0)
        self.assertIsNone(result)

    def test_invalid_goal_nan(self):
        """Test with NaN goal returns None."""
        now = time.time()
        history = deque([(now - 1, 60.0), (now, 58.0)])
        result = calculator.calculate_cooldown_linear_eta(history, float("nan"))
        self.assertIsNone(result)

    def test_invalid_window_seconds(self):
        """Test with invalid window_seconds returns None."""
        now = time.time()
        history = deque([(now - 1, 60.0), (now, 58.0)])
        result = calculator.calculate_cooldown_linear_eta(
            history, 30.0, window_seconds=-10.0
        )
        self.assertIsNone(result)

    def test_invalid_data_in_history(self):
        """Test that invalid data points are filtered out."""
        now = time.time()
        history = deque(
            [
                (now - 10, 80.0),
                (float("inf"), 75.0),  # Invalid timestamp
                (now - 8, float("nan")),  # Invalid temp
                (now - 6, 70.0),
                (now - 4, 65.0),
                (now - 2, 60.0),
                (now, 55.0),
            ]
        )
        result = calculator.calculate_cooldown_linear_eta(history, 30.0)
        # Should still work by filtering invalid data
        self.assertIsNotNone(result)
        assert result is not None

    def test_cooldown_linear(self):
        """Test linear cooldown calculation when already below goal."""
        now = time.time()
        # Cooling from 80°C, already cooled down below 30°C goal
        history = deque()
        for i in range(60):
            t = now - (60 - i)
            temp = 80.0 - i
            history.append((t, temp))

        result = calculator.calculate_cooldown_linear_eta(history, 30.0)
        # Final temp is 80-59=21°C (i goes 0-59, last is 59)
        # Already below goal of 30°C, so should return None
        self.assertIsNone(result)

    def test_cooldown_in_progress(self):
        """Test cooldown calculation when still above goal."""
        now = time.time()
        # Cooling from 60°C at -0.5°C/s, goal 30°C
        history = deque()
        for i in range(40):
            t = now - (40 - i)
            temp = 60.0 - (i * 0.5)
            history.append((t, temp))

        result = calculator.calculate_cooldown_linear_eta(history, 30.0)
        # Final temp is 60 - (39 * 0.5) = 40.5°C (i goes 0-39, last is 39)
        # Goal is 30°C, rate -0.5°C/s, remaining ~10.5°C = ~21s
        self.assertIsNotNone(result)
        assert result is not None
        self.assertGreater(result, 0.0)

    def test_not_cooling_returns_none(self):
        """Test that heating during cooldown returns None."""
        now = time.time()
        history = deque(
            [
                (now - 2, 40.0),
                (now - 1, 41.0),
                (now, 42.0),
            ]
        )
        result = calculator.calculate_cooldown_linear_eta(history, 30.0)
        self.assertIsNone(result)


class TestCalculateCooldownExponentialETA(TestCase):
    """Test cases for calculate_cooldown_exponential_eta function."""

    def test_insufficient_data(self):
        """Test with insufficient data returns None."""
        history = deque()
        result = calculator.calculate_cooldown_exponential_eta(history, 20.0, 30.0)
        self.assertIsNone(result)

    def test_invalid_ambient_nan(self):
        """Test with NaN ambient returns None."""
        now = time.time()
        history = deque([(now, 60.0)])
        result = calculator.calculate_cooldown_exponential_eta(
            history, float("nan"), 30.0
        )
        self.assertIsNone(result)

    def test_invalid_goal_nan(self):
        """Test with NaN goal returns None."""
        now = time.time()
        history = deque([(now, 60.0)])
        result = calculator.calculate_cooldown_exponential_eta(
            history, 20.0, float("nan")
        )
        self.assertIsNone(result)

    def test_invalid_window_seconds(self):
        """Test with invalid window_seconds returns None."""
        now = time.time()
        history = deque([(now - 1, 60.0), (now, 58.0)])
        result = calculator.calculate_cooldown_exponential_eta(
            history, 20.0, 30.0, window_seconds=float("inf")
        )
        self.assertIsNone(result)

    def test_invalid_ambient_goal(self):
        """Test with goal below ambient returns None."""
        now = time.time()
        history = deque([(now, 60.0)])
        result = calculator.calculate_cooldown_exponential_eta(history, 30.0, 25.0)
        self.assertIsNone(result)

    def test_exponential_cooldown(self):
        """Test exponential cooldown calculation."""
        now = time.time()
        ambient = 20.0
        goal = 30.0

        # Simulate Newton's law of cooling: T(t) = T_ambient + (T_0 - T_ambient) * e^(-t/tau)
        history = deque()
        t0_temp = 80.0

        for i in range(120):
            t = now - (120 - i)
            temp = ambient + (t0_temp - ambient) * (0.99**i)
            history.append((t, temp))

        result = calculator.calculate_cooldown_exponential_eta(
            history, ambient, goal, window_seconds=120.0
        )
        self.assertIsNotNone(result)
        assert result is not None
        self.assertGreater(result, 0.0)


if __name__ == "__main__":
    import unittest

    unittest.main()
