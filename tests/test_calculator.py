# flake8: noqa
# pylint: disable=line-too-long
"""Unit tests for the calculator module."""

import math
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

    def test_constant_rate_heating(self):
        """A 1 C/s ramp preserves the selected exponential ETA."""
        history = deque((float(i), 20.0 + i, 60.0) for i in range(30))

        result = calculator.calculate_exponential_eta(history, 60.0)

        self.assertIsNotNone(result)
        # 11 C remain; the fitted slowdown predicts about 23.6 seconds,
        # rather than falling back to the smoothed linear estimate of 12 s.
        self.assertAlmostEqual(result, 23.59, delta=0.01)

    def test_noisy_exponential_heating(self):
        """Temperature residuals preserve the ETA of a known heating curve."""
        target, asymptote, tau = 50.0, 55.0, 30.0
        history = deque(
            (
                float(i),
                asymptote - 35.0 * math.exp(-i / tau) + (0.3 if i % 2 else -0.3),
                target,
            )
            for i in range(30)
        )
        expected = tau * math.log((asymptote - history[-1][1]) / (asymptote - target))

        for spike in (None, 65.0):
            with self.subTest(spike=spike):
                samples = history.copy()
                if spike is not None:
                    # An interior sample above all candidates must be skipped
                    # without shifting the remaining temperature/time pairs.
                    samples[8] = (8.0, spike, target)
                result = calculator.calculate_exponential_eta(samples, target)

                self.assertIsNotNone(result)
                self.assertAlmostEqual(result, expected, delta=1.0)


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


class TestRealPrinterSamples(TestCase):
    """Regression tests built from samples captured on real printers.

    These runs exposed three defects: an exponential fit anchored on the
    target instead of the heater's steady state, a sanity guard loose enough
    that bad estimates pinned just under it, and a two-point slope that made
    the countdown jump between updates.
    """

    # Heated bed, 27.6C -> 44.9C against a 50C target, ~2s sampling.
    # Measured rate over the final samples puts the true remaining time near
    # 19s; the target-anchored fit used to report 62-149s here.
    HEATED_BED_TARGET = 50.0
    HEATED_BED_SAMPLES = [
        (0.0, 27.56),
        (0.01, 27.56),
        (1.6, 27.49),
        (3.6, 28.66),
        (5.6, 30.03),
        (7.6, 31.37),
        (9.6, 32.53),
        (11.6, 34.03),
        (13.6, 34.9),
        (15.62, 35.86),
        (17.6, 36.54),
        (19.6, 37.2),
        (21.6, 38.04),
        (23.6, 38.66),
        (25.6, 39.34),
        (27.6, 40.2),
        (29.0, 40.2),
        (29.03, 40.78),
        (29.59, 41.09),
        (30.02, 41.09),
        (31.02, 41.37),
        (31.6, 41.53),
        (32.02, 41.63),
        (33.02, 42.08),
        (33.6, 42.13),
        (34.02, 42.38),
        (35.02, 42.78),
        (35.6, 42.84),
        (36.02, 43.0),
        (37.02, 43.16),
        (37.6, 43.3),
        (38.02, 43.59),
        (39.02, 43.89),
        (39.59, 43.94),
        (40.01, 44.27),
        (41.02, 44.2),
        (41.6, 44.6),
        (42.03, 44.59),
        (43.02, 44.84),
        (43.6, 44.88),
    ]

    def _history(self, upto=None):
        rows = self.HEATED_BED_SAMPLES[:upto]
        now = time.time()
        base = self.HEATED_BED_SAMPLES[0][0]
        return deque(
            (
                (
                    now - (self.HEATED_BED_SAMPLES[-1][0] - (t - base)),
                    temp,
                    self.HEATED_BED_TARGET,
                )
                for t, temp in rows
            ),
            maxlen=60,
        )

    def test_exponential_not_inflated_on_slow_bed(self):
        """Exponential ETA must stay near the measured remaining time."""
        history = self._history()
        result = calculator.calculate_exponential_eta(history, self.HEATED_BED_TARGET)
        self.assertIsNotNone(result)
        assert result is not None
        # True remaining ~19s. Anything past 40s is the old inflated fit.
        self.assertLess(result, 40.0)
        self.assertGreater(result, 5.0)

    def test_exponential_stays_close_to_linear(self):
        """The two estimates must agree within the sanity bounds."""
        for upto in range(8, len(self.HEATED_BED_SAMPLES) + 1):
            history = self._history(upto)
            exp = calculator.calculate_exponential_eta(history, self.HEATED_BED_TARGET)
            lin = calculator.calculate_linear_eta(history, self.HEATED_BED_TARGET)
            if exp is None or lin is None:
                continue
            if abs(exp - lin) <= calculator.EXP_SANITY_SLACK_S:
                continue
            self.assertLessEqual(
                exp,
                lin * calculator.EXP_SANITY_MAX_RATIO,
                msg=f"exponential {exp:.1f}s diverged from linear {lin:.1f}s at n={upto}",
            )

    def test_eta_decreases_as_bed_approaches_target(self):
        """ETA must trend downward, not swing between updates."""
        etas = []
        for upto in range(10, len(self.HEATED_BED_SAMPLES) + 1):
            result = calculator.calculate_exponential_eta(
                self._history(upto), self.HEATED_BED_TARGET
            )
            if result is not None:
                etas.append(result)
        self.assertGreater(len(etas), 10)
        self.assertLess(etas[-1], etas[0])
        # No single update may more than double the countdown.
        for prev, cur in zip(etas, etas[1:]):
            self.assertLess(cur, max(prev * 2.0, prev + 10.0))

    def test_linear_eta_is_stable_between_updates(self):
        """Consecutive linear estimates must not swing.

        Measured on this run, the previous two-point slope moved the countdown
        by 2.1s on average between updates; the least-squares fit holds it
        under 1.5s. This is the property users actually see, so it is asserted
        on the unmodified samples rather than against injected noise.
        """
        etas = []
        for upto in range(10, len(self.HEATED_BED_SAMPLES) + 1):
            result = calculator.calculate_linear_eta(
                self._history(upto), self.HEATED_BED_TARGET
            )
            if result is not None:
                etas.append(result)

        self.assertGreater(len(etas), 20)
        jumps = [abs(b - a) for a, b in zip(etas, etas[1:])]
        mean_jump = sum(jumps) / len(jumps)
        self.assertLess(mean_jump, 1.5, msg=f"mean jump {mean_jump:.2f}s too large")
        self.assertLess(max(jumps), 6.0)


if __name__ == "__main__":
    import unittest

    unittest.main()
