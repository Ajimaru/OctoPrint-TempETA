"""Unit tests for the Temperature ETA plugin.

These tests follow the guidance in tests/README.md:
- pytest
- mock external dependencies (OctoPrint internals)
- test edge cases
- avoid sleeps (monkeypatch time)
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, cast

import pytest

import octoprint_temp_eta
from octoprint_temp_eta import TempETAPlugin


class DummyLogger:
    def debug(self, *args: Any, **kwargs: Any) -> None:
        return

    def info(self, *args: Any, **kwargs: Any) -> None:
        return


class DummyPluginManager:
    def __init__(self) -> None:
        self.messages: List[Dict[str, Any]] = []

    def send_plugin_message(self, identifier: str, payload: Dict[str, Any]) -> None:
        self.messages.append({"identifier": identifier, "payload": payload})


class DummySettings:
    def __init__(self, values: Dict[str, Any]) -> None:
        self._values = dict(values)

    def get_boolean(self, path: List[str]) -> bool:
        return bool(self._values.get(path[0]))

    def get_float(self, path: List[str]) -> float:
        value = self._values.get(path[0])
        if value is None:
            return 0.0
        return float(value)

    def get_int(self, path: List[str]) -> int:
        value = self._values.get(path[0])
        if value is None:
            return 0
        return int(value)

    def get(self, path: List[str]) -> Any:
        return self._values.get(path[0])

    def set(self, path: List[str], value: Any) -> None:
        self._values[path[0]] = value

    def save(self) -> None:
        return


class DummyPrinterProfileManager:
    def __init__(self, profile: Dict[str, Any]) -> None:
        self._profile = profile

    def get_current_or_default(self) -> Dict[str, Any]:
        return dict(self._profile)


class DummyPrinter:
    def __init__(self, printing: bool = False) -> None:
        self._printing = printing

    def is_printing(self) -> bool:
        return bool(self._printing)


@pytest.fixture()
def plugin() -> TempETAPlugin:
    """Create a plugin instance with mocked OctoPrint dependencies."""
    p = TempETAPlugin()
    p_any = cast(Any, p)
    p_any._identifier = "temp_eta"
    p_any._logger = DummyLogger()
    p_any._plugin_manager = DummyPluginManager()
    p_any._printer = DummyPrinter(printing=False)
    p_any._printer_profile_manager = DummyPrinterProfileManager(
        {
            "id": "default",
            "name": "Default",
            "heatedBed": True,
            "heatedChamber": False,
            "extruder": {"count": 1},
        }
    )
    p_any._settings = DummySettings(
        {
            "enabled": True,
            "suppress_while_printing": False,
            "threshold_start": 5.0,
            "update_interval": 0.0,
            "algorithm": "linear",
            "history_size": 60,
            "debug_logging": False,
        }
    )

    # Avoid implicit profile switching side effects unless a test wants them.
    p_any._active_profile_id = "default"
    return p


def _set_time(monkeypatch: pytest.MonkeyPatch, now: float) -> None:
    monkeypatch.setattr(octoprint_temp_eta.time, "time", lambda: float(now))


def test_settings_defaults_shape(plugin: TempETAPlugin) -> None:
    defaults = plugin.get_settings_defaults()

    assert defaults["enabled"] is True
    assert defaults["threshold_start"] == 5.0
    assert defaults["algorithm"] in ("linear", "exponential")
    assert defaults["update_interval"] == 1.0
    assert defaults["history_size"] == 60

    assert defaults["enable_cooldown_eta"] is True
    assert defaults["cooldown_mode"] in ("threshold", "ambient")
    cooldown_target_tool0 = defaults["cooldown_target_tool0"]
    assert cooldown_target_tool0 is not None
    assert float(cooldown_target_tool0) > 0

    cooldown_hysteresis_c = defaults["cooldown_hysteresis_c"]
    assert cooldown_hysteresis_c is not None
    assert float(cooldown_hysteresis_c) > 0

    cooldown_fit_window_seconds = defaults["cooldown_fit_window_seconds"]
    assert cooldown_fit_window_seconds is not None
    assert int(cooldown_fit_window_seconds) >= 10

    assert defaults["show_historical_graph"] is True

    assert defaults["color_mode"] in ("bands", "status")
    assert isinstance(defaults["color_heating"], str)
    assert isinstance(defaults["color_cooling"], str)
    assert isinstance(defaults["color_idle"], str)

    assert defaults["sound_enabled"] is False
    assert defaults["sound_target_reached"] is False
    assert defaults["sound_cooldown_finished"] is False
    assert 0.0 <= float(defaults["sound_volume"]) <= 1.0
    assert float(defaults["sound_min_interval_s"]) >= 0.0


def test_calculate_linear_eta_returns_none_with_insufficient_history(
    plugin: TempETAPlugin,
) -> None:
    plugin._temp_history["tool0"] = deque([(1.0, 20.0, 200.0)], maxlen=60)
    assert plugin._calculate_linear_eta("tool0", 200.0) is None


def test_calculate_linear_eta_simple(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Linear ETA uses last 10 seconds and returns remaining/rate."""
    # now=100, points at 95 (20C) -> 100 (30C)
    _set_time(monkeypatch, 100.0)
    plugin._temp_history["tool0"] = deque(
        [(95.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60
    )

    eta = plugin._calculate_linear_eta("tool0", 50.0)
    assert eta is not None
    assert abs(eta - 10.0) < 1e-6


def test_calculate_exponential_eta_falls_back_to_linear_when_not_enough_points(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    _set_time(monkeypatch, 30.0)
    plugin._temp_history["tool0"] = deque(
        [(15.0, 20.0, 100.0), (25.0, 30.0, 100.0), (30.0, 40.0, 100.0)], maxlen=60
    )
    # < 6 points in window => exponential falls back to linear, which needs 2 recent points.
    assert plugin._calculate_exponential_eta("tool0", 100.0) is not None


def test_calculate_exponential_eta_returns_number_for_reasonable_curve(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Exponential ETA should return a positive number for a smooth heating curve."""
    # Build a curve approaching target (remaining decays).
    target = 100.0
    points = [
        (0.0, 20.0, target),
        (5.0, 35.0, target),
        (10.0, 48.0, target),
        (15.0, 59.0, target),
        (20.0, 68.0, target),
        (25.0, 75.0, target),
        (30.0, 80.0, target),
        (35.0, 84.0, target),
    ]
    _set_time(monkeypatch, 35.0)
    plugin._temp_history["tool0"] = deque(points, maxlen=60)

    eta = plugin._calculate_exponential_eta("tool0", target)
    assert eta is not None
    assert eta > 0


def test_temperature_callback_records_only_when_target_set_and_far_enough(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    _set_time(monkeypatch, 100.0)
    plugin._temp_history = {}

    plugin.on_printer_add_temperature({"tool0": {"actual": 90.0, "target": 100.0}})
    assert "tool0" in plugin._temp_history
    assert len(plugin._temp_history["tool0"]) == 1

    # Remaining < threshold_start -> should not record.
    _set_time(monkeypatch, 101.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 98.0, "target": 100.0}})
    assert len(plugin._temp_history["tool0"]) == 1

    # target <= 0 -> should not record.
    _set_time(monkeypatch, 102.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 10.0, "target": 0.0}})
    assert len(plugin._temp_history["tool0"]) == 1


def test_temperature_callback_treats_string_target_off_as_cooldown(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["enable_cooldown_eta"], True)
    settings.set(["cooldown_mode"], "threshold")
    settings.set(["cooldown_target_tool0"], 50.0)
    settings.set(["cooldown_hysteresis_c"], 1.0)
    settings.set(["cooldown_fit_window_seconds"], 120)

    _set_time(monkeypatch, 200.0)
    plugin._cooldown_history["tool0"].clear()

    # Simulate a firmware/virtual-printer target format that sends a string like "off".
    plugin.on_printer_add_temperature({"tool0": {"actual": 200.0, "target": "off"}})
    assert len(plugin._cooldown_history["tool0"]) == 1


def test_calculate_cooldown_linear_eta_simple(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["enable_cooldown_eta"], True)
    settings.set(["cooldown_fit_window_seconds"], 120)

    # Cooling: 100C -> 90C over 10s => -1 C/s. Goal 80C => remaining 10C => 10s.
    _set_time(monkeypatch, 10.0)
    plugin._cooldown_history["tool0"] = deque([(0.0, 100.0), (10.0, 90.0)], maxlen=60)

    eta = plugin._calculate_cooldown_linear_eta("tool0", 80.0)
    assert eta is not None
    assert abs(eta - 10.0) < 1e-6


def test_calculate_cooldown_exponential_eta_returns_number_for_reasonable_curve(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["enable_cooldown_eta"], True)
    settings.set(["cooldown_fit_window_seconds"], 300)

    ambient = 20.0
    goal = 21.0

    # Build a smooth cooldown curve towards ambient.
    points = [
        (0.0, 90.0),
        (10.0, 75.0),
        (20.0, 64.0),
        (30.0, 56.0),
        (40.0, 50.0),
        (50.0, 45.0),
        (60.0, 41.0),
    ]
    _set_time(monkeypatch, 60.0)
    plugin._cooldown_history["tool0"] = deque(points, maxlen=60)

    eta = plugin._calculate_cooldown_exponential_eta(
        heater_name="tool0", ambient_c=ambient, goal_c=goal
    )
    assert eta is not None
    assert eta > 0


def test_broadcast_includes_cooldown_eta_when_target_is_zero(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["enable_cooldown_eta"], True)
    settings.set(["cooldown_mode"], "threshold")
    settings.set(["cooldown_target_tool0"], 50.0)
    settings.set(["cooldown_hysteresis_c"], 1.0)
    settings.set(["cooldown_fit_window_seconds"], 120)

    # Provide cooldown history for a falling temperature.
    _set_time(monkeypatch, 10.0)
    plugin._cooldown_history["tool0"] = deque([(0.0, 80.0), (10.0, 70.0)], maxlen=60)

    pm: DummyPluginManager = plugin._plugin_manager  # type: ignore[assignment]

    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 70.0, "target": 0.0}})

    msgs = [m["payload"] for m in pm.messages if m["payload"].get("heater") == "tool0"]
    assert msgs
    payload = msgs[-1]
    assert payload.get("type") == "eta_update"
    assert payload.get("eta_kind") in ("cooling", None)
    # When cooling ETA is available, cooldown_target should be provided.
    if payload.get("eta_kind") == "cooling":
        assert payload.get("cooldown_target") is not None
        assert payload.get("eta") is not None


def test_suppress_while_printing_clears_once_and_stops_updates(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    settings = cast(DummySettings, cast(Any, plugin)._settings)
    settings.set(["suppress_while_printing"], True)
    cast(Any, plugin)._printer = DummyPrinter(printing=True)

    # Ensure we don't trigger profile-switch clear noise.
    plugin._active_profile_id = "default"  # type: ignore[attr-defined]

    # Pre-populate known heater keys so clear messages are observable.
    plugin._temp_history = {
        "tool0": deque([(1.0, 20.0, 200.0), (2.0, 21.0, 200.0)], maxlen=60)
    }

    pm: DummyPluginManager = plugin._plugin_manager  # type: ignore[assignment]

    _set_time(monkeypatch, 100.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 25.0, "target": 200.0}})
    first_count = len(pm.messages)
    assert first_count >= 1
    # Suppression should prevent recording new data.
    assert len(plugin._temp_history["tool0"]) == 0

    _set_time(monkeypatch, 101.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 30.0, "target": 200.0}})
    # No additional clears while suppression remains active.
    assert len(pm.messages) == first_count


def test_broadcast_sends_only_supported_heaters(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Ensure unsupported heaters (e.g. tool1 when extruder count is 1) are ignored."""
    pm: DummyPluginManager = plugin._plugin_manager  # type: ignore[assignment]

    _set_time(monkeypatch, 100.0)
    plugin.on_printer_add_temperature(
        {
            "tool0": {"actual": 20.0, "target": 200.0},
            "tool1": {"actual": 20.0, "target": 200.0},
            "bed": {"actual": 30.0, "target": 60.0},
        }
    )

    heaters = [
        m["payload"]["heater"]
        for m in pm.messages
        if m["payload"].get("type") == "eta_update"
    ]
    assert "tool0" in heaters
    assert "bed" in heaters
    assert "tool1" not in heaters
