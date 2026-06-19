"""Unit tests for the Temperature ETA plugin.

These tests follow the guidance in tests/README.md:
- pytest
- mock external dependencies (OctoPrint internals)
- test edge cases
- avoid sleeps (monkeypatch time)
"""

from __future__ import annotations

import json
import pathlib
from collections import deque
from pathlib import Path
from typing import Any, cast

import pytest

import octoprint_temp_eta
from octoprint_temp_eta import TempETAPlugin
from octoprint_temp_eta import calculator as calc_module


class DummyLogger:
    """Minimal logger stub for tests."""

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        del msg, args, kwargs

    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        del msg, args, kwargs

    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        del msg, args, kwargs

    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        del msg, args, kwargs


class InfoRecordingLogger(DummyLogger):
    """Record calls for test assertions."""

    def __init__(self) -> None:
        """Initialize test helper state."""
        self.info_calls: list[str] = []

    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        del args
        self.info_calls.append(str(msg))


class WarningRecordingLogger(DummyLogger):
    """Record calls for test assertions."""

    def __init__(self) -> None:
        """Initialize test helper state."""
        self.warning_calls: list[str] = []
        self.debug_calls: list[str] = []

    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        del args
        self.warning_calls.append(str(msg))

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        del args, kwargs
        self.debug_calls.append(str(msg))


class DebuggableLogger(DummyLogger):
    """Logger stub with level-check support for tests."""

    def __init__(self, enabled: bool = True) -> None:
        """Initialize test helper state."""
        self._enabled = bool(enabled)
        self.debug_payloads: list[Any] = []

    def isEnabledFor(self, level: int) -> bool:  # noqa: N802 (OctoPrint/stdlib style)
        """Return logger level support for tests."""
        del level
        return bool(self._enabled)

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a test logger stub method."""
        self.debug_payloads.append(((msg, *args), {}))


def _get_attr(obj: Any, name: str) -> Any:
    """Read an internal attribute without dotted protected-member access."""
    return getattr(obj, name)


def _set_attr(obj: Any, name: str, value: Any) -> None:
    """Write an internal attribute without dotted protected-member access."""
    setattr(obj, name, value)


def _call_attr(obj: Any, name: str, *args: Any, **kwargs: Any) -> Any:
    """Call an internal method without dotted protected-member access."""
    return getattr(obj, name)(*args, **kwargs)


def _member(name: str) -> str:
    """Build an internal member name without inline protected-member tokens."""
    return f"_{name}"


class DummyPluginManager:
    """Minimal PluginManager stub for tests."""

    def __init__(self) -> None:
        """Initialize test helper state."""
        self.messages: list[dict[str, Any]] = []

    def send_plugin_message(self, identifier: str, payload: dict[str, Any]) -> None:
        """Provide a test stub implementation."""
        self.messages.append({"identifier": identifier, "payload": payload})


class DummySettings:
    """Minimal Settings stub for tests."""

    def __init__(self, values: dict[str, Any]) -> None:
        """Initialize test helper state."""
        self._values = dict(values)

    def get_boolean(self, path: list[str]) -> bool:
        """Return dummy value for tests."""
        return bool(self._values.get(path[0]))

    def get_float(self, path: list[str]) -> float:
        """Return dummy value for tests."""
        value = self._values.get(path[0])
        if value is None:
            return 0.0
        return float(value)

    def get_int(self, path: list[str]) -> int:
        """Return dummy value for tests."""
        value = self._values.get(path[0])
        if value is None:
            return 0
        return int(value)

    def get(self, path: list[str]) -> Any:
        """Provide a test helper method."""
        return self._values.get(path[0])

    def set(self, path: list[str], value: Any) -> None:
        """Provide a test stub implementation."""
        self._values[path[0]] = value

    def save(self) -> None:
        """Provide a test stub implementation."""
        return


class DummyPrinterProfileManager:
    """Minimal PrinterProfileManager stub for tests."""

    def __init__(self, profile: dict[str, Any]) -> None:
        """Initialize test helper state."""
        self._profile = profile

    def get_current_or_default(self) -> dict[str, Any]:
        """Return dummy value for tests."""
        return dict(self._profile)


class DummyPrinter:
    """Minimal Printer stub for tests."""

    def __init__(
        self,
        printing: bool = False,
        paused: bool = False,
        state_id: str = "OPERATIONAL",
    ) -> None:
        """Initialize test helper state."""
        self._printing = printing
        self._paused = paused
        self._state_id = state_id

        self.registered_callbacks: list[Any] = []

    def register_callback(self, callback: Any) -> None:
        """Register callback in dummy printer."""
        self.registered_callbacks.append(callback)

    def is_printing(self) -> bool:
        """Return dummy state for tests."""
        return bool(self._printing)

    def is_paused(self) -> bool:
        """Return dummy state for tests."""
        return bool(self._paused)

    def get_state_id(self) -> str:
        """Return dummy value for tests."""
        return str(self._state_id)


@pytest.fixture(name="temp_eta_plugin")
def fixture_temp_eta_plugin() -> TempETAPlugin:
    """Create a plugin instance with mocked OctoPrint dependencies."""
    p = TempETAPlugin()
    _set_attr(p, _member("identifier"), "temp_eta")
    _set_attr(p, _member("plugin_version"), "0.0.0")
    _set_attr(p, _member("logger"), DummyLogger())
    _set_attr(p, _member("plugin_manager"), DummyPluginManager())
    _set_attr(p, _member("printer"), DummyPrinter(printing=False))
    _set_attr(
        p,
        _member("printer_profile_manager"),
        DummyPrinterProfileManager(
            {
                "id": "default",
                "name": "Default",
                "heatedBed": True,
                "heatedChamber": False,
                "extruder": {"count": 1},
            }
        ),
    )
    _set_attr(
        p,
        _member("settings"),
        DummySettings(
            {
                "enabled": True,
                "enable_heating_eta": True,
                "suppress_while_printing": False,
                "threshold_start": 5.0,
                "update_interval": 0.0,
                "algorithm": "linear",
                "history_size": 60,
                "debug_logging": False,
            }
        ),
    )

    # Avoid implicit profile switching side effects unless a test wants them.
    _set_attr(p, _member("active_profile_id"), "default")
    return p


def _set_plugin_data_folder(temp_eta_plugin: Any, folder: Path) -> None:
    """Provide a local test helper."""
    plugin_any = cast(Any, temp_eta_plugin)
    plugin_any.get_plugin_data_folder = lambda: str(folder)


def _set_time(monkeypatch: pytest.MonkeyPatch, now: float) -> None:
    """Provide a local test helper."""
    monkeypatch.setattr(octoprint_temp_eta.time, "time", lambda: float(now))


def test_settings_defaults_shape(temp_eta_plugin: Any) -> None:
    """Test settings defaults shape."""
    defaults = temp_eta_plugin.get_settings_defaults()

    assert defaults["enabled"] is True
    assert defaults["enable_heating_eta"] is True
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
    sound_volume = defaults["sound_volume"]
    assert sound_volume is not None
    assert 0.0 <= float(sound_volume) <= 1.0

    sound_min_interval_s = defaults["sound_min_interval_s"]
    assert sound_min_interval_s is not None
    assert float(sound_min_interval_s) >= 0.0

    assert defaults["notification_enabled"] is False
    assert defaults["notification_target_reached"] is False
    assert defaults["notification_cooldown_finished"] is False
    notification_timeout_s = defaults["notification_timeout_s"]
    assert notification_timeout_s is not None
    assert float(notification_timeout_s) >= 1.0

    notification_min_interval_s = defaults["notification_min_interval_s"]
    assert notification_min_interval_s is not None
    assert float(notification_min_interval_s) >= 0.0


def test_debug_log_settings_snapshot_skips_when_debug_disabled(
    temp_eta_plugin: Any,
) -> None:
    """Test debug log settings snapshot skips when debug disabled."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("debug_logging_enabled"), False)
    _set_attr(plugin_any, _member("last_settings_snapshot_log_time"), 0.0)

    called: list[Any] = []
    _set_attr(
        plugin_any,
        _member("debug_log"),
        lambda *args, **kwargs: called.append((args, kwargs)),
    )

    _call_attr(temp_eta_plugin, _member("debug_log_settings_snapshot"), 100.0)
    assert not called
    assert _get_attr(plugin_any, _member("last_settings_snapshot_log_time")) == 0.0


def test_debug_log_settings_snapshot_logs_and_throttles(temp_eta_plugin: Any) -> None:
    """Test debug log settings snapshot logs and throttles."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("last_settings_snapshot_log_time"), 0.0)

    logged: list[str] = []

    def _capture(msg: str, *_args: Any) -> None:
        """Provide a local test helper callback."""
        logged.append(msg)

    _set_attr(plugin_any, _member("debug_log"), _capture)

    _call_attr(temp_eta_plugin, _member("debug_log_settings_snapshot"), 100.0)
    assert logged

    # Throttled: within 60s should not log again.
    logged.clear()
    _call_attr(temp_eta_plugin, _member("debug_log_settings_snapshot"), 120.0)
    assert not logged


def test_refresh_runtime_caches_applies_valid_settings_and_orders_backoff(
    temp_eta_plugin: Any,
) -> None:
    """Test refresh runtime caches applies valid settings and orders backoff."""
    plugin_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(plugin_any, _member("settings")))

    settings.set(["threshold_start"], 7.5)
    settings.set(["update_interval"], 0.5)
    settings.set(["persist_backoff_reset_s"], 5.0)
    settings.set(["persist_backoff_initial_s"], 20.0)
    # Intentionally inverted to exercise ordering correction (max must be >= 10 to be accepted).
    settings.set(["persist_backoff_max_s"], 10.0)
    settings.set(["persist_max_json_bytes"], 20000)

    _set_attr(plugin_any, _member("threshold_start_c"), 5.0)
    _set_attr(plugin_any, _member("update_interval_s"), 1.0)
    _set_attr(plugin_any, _member("persist_backoff_current_s"), 999.0)

    _call_attr(
        temp_eta_plugin,
        _member("refresh_runtime_caches"),
    )

    assert _get_attr(plugin_any, _member("threshold_start_c")) == 7.5
    assert _get_attr(plugin_any, _member("update_interval_s")) == 0.5
    assert _get_attr(plugin_any, _member("persist_backoff_reset_s")) == 5.0
    assert _get_attr(plugin_any, _member("persist_backoff_initial_s")) == 20.0
    assert _get_attr(plugin_any, _member("persist_backoff_max_s")) == 20.0
    assert (
        1.0
        <= float(_get_attr(plugin_any, _member("persist_backoff_current_s")))
        <= 20.0
    )
    assert _get_attr(plugin_any, _member("persist_max_json_bytes")) == 20000


def test_refresh_runtime_caches_handles_missing_or_broken_settings(
    temp_eta_plugin: Any,
) -> None:
    """Test refresh runtime caches handles missing or broken settings."""
    plugin_any = cast(Any, temp_eta_plugin)

    # Missing settings: should return early.
    _set_attr(plugin_any, _member("settings"), None)
    _call_attr(
        temp_eta_plugin,
        _member("refresh_runtime_caches"),
    )

    class _RaisingSettings:
        """Raise errors on access for failure-path tests."""

        def get_float(self, _path: list[str]) -> float:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

        def get_int(self, _path: list[str]) -> int:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("settings"), _RaisingSettings())

    # Exercise exception paths and the ordering no-op branch.
    _set_attr(plugin_any, _member("persist_backoff_initial_s"), 1.0)
    _set_attr(plugin_any, _member("persist_backoff_reset_s"), 10.0)
    _call_attr(
        temp_eta_plugin,
        _member("refresh_runtime_caches"),
    )


def test_maybe_persist_history_schedules_on_startup_and_backoff_floor(
    temp_eta_plugin: Any,
) -> None:
    """Test maybe persist history schedules on startup and backoff floor."""
    plugin_any = cast(Any, temp_eta_plugin)

    called: list[float] = []
    _set_attr(
        plugin_any,
        _member("persist_current_profile_history"),
        lambda: called.append(1.0),
    )

    _set_attr(plugin_any, _member("history_dirty"), True)
    _set_attr(plugin_any, _member("next_persist_time"), 0.0)
    _set_attr(plugin_any, _member("persist_backoff_current_s"), 5.0)
    _set_attr(plugin_any, _member("persist_backoff_initial_s"), 10.0)
    _set_attr(plugin_any, _member("persist_backoff_max_s"), 40.0)
    _set_attr(plugin_any, _member("persist_phase_active"), False)

    _call_attr(temp_eta_plugin, _member("maybe_persist_history"), 100.0)
    assert not called
    assert _get_attr(plugin_any, _member("next_persist_time")) == 105.0

    # Not due yet.
    _call_attr(temp_eta_plugin, _member("maybe_persist_history"), 104.9)
    assert not called

    # Due: should persist and lift current to at least initial.
    _call_attr(temp_eta_plugin, _member("maybe_persist_history"), 105.0)
    assert called
    assert _get_attr(plugin_any, _member("persist_backoff_current_s")) == 10.0
    assert _get_attr(plugin_any, _member("persist_phase_active")) is True


def test_persist_current_profile_history_emits_size_warning_and_trims(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test persist current profile history emits size warning and trims."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(plugin_any, _member("active_profile_id"), "default")

    # Force the size-cap path.
    _set_attr(plugin_any, _member("persist_max_json_bytes"), 1024)
    _set_attr(plugin_any, _member("last_persist_size_warning_time"), 0.0)
    _set_attr(plugin_any, _member("logger"), WarningRecordingLogger())

    # Lots of points -> large JSON.
    _set_attr(
        plugin_any,
        _member("temp_history"),
        {
            "tool0": deque(
                [(float(i), 20.0 + i * 0.01, 200.0) for i in range(500)], maxlen=2000
            )
        },
    )
    _set_attr(plugin_any, _member("history_dirty"), True)

    _set_time(monkeypatch, 1000.0)
    _call_attr(
        temp_eta_plugin,
        _member("persist_current_profile_history"),
    )

    assert _get_attr(plugin_any, _member("logger")).warning_calls
    # Ensure atomic tmp cleanup happens.
    assert not (tmp_path / "history_default.json.tmp").exists()
    assert (tmp_path / "history_default.json").exists()


def test_persist_current_profile_history_breaks_when_cannot_trim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test persist current profile history breaks when cannot trim."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(plugin_any, _member("active_profile_id"), "default")

    # Force trimming path even with minimal samples.
    _set_attr(plugin_any, _member("persist_max_json_bytes"), 50)
    _set_attr(plugin_any, _member("logger"), WarningRecordingLogger())

    # Exactly 2 points -> trimming cannot reduce below 2.
    _set_attr(
        plugin_any,
        _member("temp_history"),
        {"tool0": deque([(1.0, 20.0, 200.0), (2.0, 21.0, 200.0)], maxlen=60)},
    )
    _set_attr(plugin_any, _member("history_dirty"), True)

    _set_time(monkeypatch, 1000.0)
    _call_attr(
        temp_eta_plugin,
        _member("persist_current_profile_history"),
    )
    assert (tmp_path / "history_default.json").exists()


def test_persist_current_profile_history_cleans_tmp_when_replace_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test persist current profile history cleans tmp when replace fails."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(plugin_any, _member("active_profile_id"), "default")
    _set_attr(plugin_any, _member("logger"), WarningRecordingLogger())

    _set_attr(
        plugin_any,
        _member("temp_history"),
        {
            "tool0": deque(
                [(1.0, 20.0, 200.0), (2.0, 21.0, 200.0), (3.0, 22.0, 200.0)], maxlen=60
            )
        },
    )
    _set_attr(plugin_any, _member("history_dirty"), True)

    def _boom_replace(self: pathlib.Path, target: pathlib.Path):
        """Provide a local test helper callback."""
        raise RuntimeError("replace failed")

    monkeypatch.setattr(pathlib.Path, "replace", _boom_replace)

    _set_time(monkeypatch, 1000.0)
    _call_attr(
        temp_eta_plugin,
        _member("persist_current_profile_history"),
    )
    assert not (tmp_path / "history_default.json.tmp").exists()


def test_persist_current_profile_history_ignores_unlink_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test persist current profile history ignores unlink errors."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(plugin_any, _member("active_profile_id"), "default")
    _set_attr(plugin_any, _member("logger"), WarningRecordingLogger())

    _set_attr(
        plugin_any,
        _member("temp_history"),
        {
            "tool0": deque(
                [(1.0, 20.0, 200.0), (2.0, 21.0, 200.0), (3.0, 22.0, 200.0)], maxlen=60
            )
        },
    )
    _set_attr(plugin_any, _member("history_dirty"), True)

    def _boom_replace(self: pathlib.Path, target: pathlib.Path):
        """Provide a local test helper callback."""
        raise RuntimeError("replace failed")

    def _boom_unlink(self: pathlib.Path):
        """Provide a local test helper callback."""
        raise RuntimeError("unlink failed")

    monkeypatch.setattr(pathlib.Path, "replace", _boom_replace)
    monkeypatch.setattr(pathlib.Path, "unlink", _boom_unlink)

    _set_time(monkeypatch, 1000.0)
    _call_attr(
        temp_eta_plugin,
        _member("persist_current_profile_history"),
    )


def test_on_printer_add_temperature_logs_heater_names_when_debug_enabled(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature logs heater names when debug enabled."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("logger"), DebuggableLogger(enabled=True))
    _set_attr(plugin_any, _member("last_update_time"), 0.0)
    _set_attr(plugin_any, _member("calculate_and_broadcast_eta"), lambda _data: None)

    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_printer_add_temperature(
        {
            "tool0": {"actual": 20.0, "target": 200.0},
            "bed": {"actual": 30.0, "target": 60.0},
            "junk": "not-a-heater",
        }
    )

    dbg = cast(DebuggableLogger, _get_attr(plugin_any, _member("logger")))
    assert dbg.debug_payloads


def test_on_printer_add_temperature_target_change_enters_persist_phase(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature target change enters persist phase."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(plugin_any, _member("calculate_and_broadcast_eta"), lambda _data: None)

    entered: list[str] = []
    _set_attr(
        plugin_any,
        _member("enter_persist_phase"),
        lambda _now, reason: entered.append(str(reason)),
    )

    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 20.0, "target": 200.0}}
    )

    _set_time(monkeypatch, 101.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 21.0, "target": 201.0}}
    )

    assert "target_change" in entered


def test_on_printer_add_temperature_uses_idle_debug_interval_when_no_samples_recorded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature uses idle debug interval when no samples recorded."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(plugin_any, _member("calculate_and_broadcast_eta"), lambda _data: None)

    # Make threshold impossible to meet so recorded_count stays 0.
    _set_attr(plugin_any, _member("threshold_start_c"), 1000.0)
    # Prevent periodic cache refresh from resetting threshold from settings.
    cast(DummySettings, _get_attr(plugin_any, _member("settings"))).set(
        ["threshold_start"], 1000.0
    )
    _set_attr(plugin_any, _member("last_runtime_cache_refresh_time"), 100.0)

    intervals: list[float] = []

    def _capture(_now: float, interval: float, *_args: Any, **_kwargs: Any) -> None:
        """Provide a local test helper callback."""
        intervals.append(float(interval))

    _set_attr(plugin_any, _member("debug_log_throttled"), _capture)

    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 20.0, "target": 30.0}}
    )
    assert intervals
    assert 60.0 in intervals


def test_sanitize_settings_payload_clamps_and_handles_invalid_values(
    temp_eta_plugin: Any,
) -> None:
    """Test sanitize settings payload clamps and handles invalid values."""
    data: dict[str, Any] = {
        "threshold_start": "nope",
        "update_interval": "",
        "history_size": "nope",
        "historical_graph_window_seconds": "999999",
        "sound_volume": "2",
        "notification_timeout_s": None,
        "cooldown_hysteresis_c": 0,
        "cooldown_fit_window_seconds": "",
        "cooldown_ambient_temp": "nope",
    }

    _call_attr(temp_eta_plugin, _member("sanitize_settings_payload"), data)

    assert data["threshold_start"] == 1.0
    assert data["update_interval"] == 0.1
    assert data["history_size"] == 10
    assert data["historical_graph_window_seconds"] == 1800
    assert data["sound_volume"] == 1.0
    assert data["notification_timeout_s"] == 1.0
    assert data["cooldown_hysteresis_c"] == 0.1
    assert data["cooldown_fit_window_seconds"] == 10
    assert data["cooldown_ambient_temp"] is None

    data2: dict[str, Any] = {"cooldown_ambient_temp": "25"}
    _call_attr(temp_eta_plugin, _member("sanitize_settings_payload"), data2)
    assert data2["cooldown_ambient_temp"] == 25.0

    data3: dict[str, Any] = {"cooldown_ambient_temp": ""}
    _call_attr(temp_eta_plugin, _member("sanitize_settings_payload"), data3)
    assert data3["cooldown_ambient_temp"] is None


def test_send_history_reset_message_includes_optional_ids(
    temp_eta_plugin: Any,
) -> None:
    """Test send history reset message includes optional ids."""
    plugin_any = cast(Any, temp_eta_plugin)
    pm: DummyPluginManager = _get_attr(plugin_any, _member("plugin_manager"))

    _call_attr(
        temp_eta_plugin,
        _member("send_history_reset_message"),
        "profile_switch",
        old_profile_id="old",
        profile_id="new",
    )
    assert pm.messages
    payload = pm.messages[-1]["payload"]
    assert payload["type"] == "history_reset"
    assert payload["reason"] == "profile_switch"
    assert payload["old_profile_id"] == "old"
    assert payload["profile_id"] == "new"


def test_send_history_reset_message_returns_when_plugin_manager_missing(
    temp_eta_plugin: Any,
) -> None:
    """Test send history reset message returns when plugin manager missing."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("plugin_manager"), None)
    _call_attr(temp_eta_plugin, _member("send_history_reset_message"), "noop")


def test_clear_all_heaters_frontend_returns_when_plugin_manager_missing(
    temp_eta_plugin: Any,
) -> None:
    """Test clear all heaters frontend returns when plugin manager missing."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("plugin_manager"), None)
    _call_attr(
        temp_eta_plugin,
        _member("clear_all_heaters_frontend"),
    )


def test_debug_log_settings_snapshot_handles_settings_exception(
    temp_eta_plugin: Any,
) -> None:
    """Test debug log settings snapshot handles settings exception."""
    plugin_any = cast(Any, temp_eta_plugin)

    class _RaisingSettings:
        """Raise errors on access for failure-path tests."""

        def get_boolean(self, _path: list[str]) -> bool:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

        def get(self, _path: list[str]) -> Any:
            """Provide a test helper method."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("settings"), _RaisingSettings())

    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("last_settings_snapshot_log_time"), 0.0)

    logged: list[Any] = []
    _set_attr(
        plugin_any,
        _member("debug_log"),
        lambda *args, **kwargs: logged.append((args, kwargs)),
    )

    _call_attr(temp_eta_plugin, _member("debug_log_settings_snapshot"), 100.0)
    assert not logged
    # Timestamp is updated before reading settings, even if reading fails.
    assert _get_attr(plugin_any, _member("last_settings_snapshot_log_time")) == 100.0


def test_persist_current_profile_history_trims_to_size_cap_and_writes_atomically(
    temp_eta_plugin: Any,
    tmp_path: Path,
) -> None:
    """Test persist current profile history trims to size cap and writes atomically."""
    plugin_any = cast(Any, temp_eta_plugin)

    class _CapturingLogger(DummyLogger):
        """Capture log output for test assertions."""

        def __init__(self) -> None:
            """Initialize test helper state."""
            self.warning_calls: list[str] = []

        def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None:
            """Provide a test logger stub method."""
            del args, kwargs
            self.warning_calls.append(str(msg))

    _set_attr(plugin_any, _member("logger"), _CapturingLogger())

    _set_plugin_data_folder(temp_eta_plugin, tmp_path)

    # Force an aggressive cap to exercise trimming logic.
    _set_attr(plugin_any, _member("persist_max_json_bytes"), 1500)

    # Create lots of samples to exceed the cap.
    with _get_attr(plugin_any, _member("lock")):
        _get_attr(plugin_any, _member("temp_history"))["tool0"] = deque(maxlen=10_000)
        _get_attr(plugin_any, _member("temp_history"))["bed"] = deque(maxlen=10_000)

        for i in range(600):
            ts = float(i)
            _get_attr(plugin_any, _member("temp_history"))["tool0"].append(
                (ts, 20.0 + i * 0.1, 200.0)
            )
            _get_attr(plugin_any, _member("temp_history"))["bed"].append(
                (ts, 30.0 + i * 0.05, 60.0)
            )

    _set_attr(plugin_any, _member("history_dirty"), True)

    _call_attr(
        temp_eta_plugin,
        _member("persist_current_profile_history"),
    )

    history_path = tmp_path / "history_default.json"
    assert history_path.exists()
    assert not (tmp_path / "history_default.json.tmp").exists()

    raw = history_path.read_bytes()
    assert len(raw) <= int(_get_attr(plugin_any, _member("persist_max_json_bytes")))

    payload = json.loads(raw.decode("utf-8"))
    assert payload["profile_id"] == "default"
    samples = payload["samples"]
    assert "tool0" in samples
    assert "bed" in samples

    # Optional heaters may be present but empty.
    if "chamber" in samples:
        assert samples["chamber"] == []

    # Trim logic guarantees at least 2 points per heater.
    assert len(samples["tool0"]) >= 2
    assert len(samples["bed"]) >= 2

    # And trimming should have happened (we started with 600 points each).
    assert len(samples["tool0"]) < 600
    assert len(samples["bed"]) < 600


def test_persist_backoff_phase_transitions_and_maybe_persist(
    temp_eta_plugin: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test persist backoff phase transitions and maybe persist."""
    plugin_any = cast(Any, temp_eta_plugin)

    # Keep callback fast: we only want to exercise phase/backoff code paths.
    _set_attr(plugin_any, _member("calculate_and_broadcast_eta"), lambda _data: None)

    persisted: list[float] = []

    def _persist_stub() -> None:
        """Provide a local test helper."""
        persisted.append(float(octoprint_temp_eta.time.time()))
        _set_attr(plugin_any, _member("history_dirty"), False)

    _set_attr(plugin_any, _member("persist_current_profile_history"), _persist_stub)

    # Start at a deterministic time.
    _set_time(monkeypatch, 1000.0)

    # First callback with an active heating phase should enter persist phase and schedule.
    data = {"tool0": {"actual": 20.0, "target": 40.0}}
    temp_eta_plugin.on_printer_add_temperature(data)

    assert _get_attr(plugin_any, _member("persist_phase_active")) is True
    assert float(_get_attr(plugin_any, _member("persist_backoff_current_s"))) == float(
        _get_attr(plugin_any, _member("persist_backoff_initial_s"))
    )
    assert float(_get_attr(plugin_any, _member("next_persist_time"))) > 1000.0
    assert not persisted

    # Advance time to the scheduled persist time and call maybe_persist.
    _set_time(monkeypatch, float(_get_attr(plugin_any, _member("next_persist_time"))))
    _set_attr(plugin_any, _member("history_dirty"), True)
    _call_attr(
        temp_eta_plugin,
        _member("maybe_persist_history"),
        octoprint_temp_eta.time.time(),
    )
    assert persisted

    # Backoff doubles after persisting (up to max).
    assert float(_get_attr(plugin_any, _member("persist_backoff_current_s"))) >= float(
        _get_attr(plugin_any, _member("persist_backoff_initial_s"))
    )

    # Now simulate leaving the active phase (target off), which should reset backoff.
    _set_time(monkeypatch, 1100.0)
    data = {"tool0": {"actual": 25.0, "target": 0.0}}
    temp_eta_plugin.on_printer_add_temperature(data)
    assert float(_get_attr(plugin_any, _member("persist_backoff_current_s"))) == float(
        _get_attr(plugin_any, _member("persist_backoff_reset_s"))
    )


def test_is_print_job_active_returns_false_when_printer_missing(
    temp_eta_plugin: Any,
) -> None:
    """Test is print job active returns false when printer missing."""
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("printer"), None)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("is_print_job_active"),
        )
        is False
    )


def test_debug_log_throttled_respects_interval(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test debug log throttled respects interval."""
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("debug_logging_enabled"), True)
    _set_attr(p_any, _member("last_debug_log_time"), -1e9)

    calls: list[str] = []
    monkeypatch.setattr(
        temp_eta_plugin, "_debug_log", lambda msg, *args: calls.append(str(msg))
    )

    _call_attr(temp_eta_plugin, _member("debug_log_throttled"), 10.0, 30.0, "hello")
    _call_attr(temp_eta_plugin, _member("debug_log_throttled"), 20.0, 30.0, "hello")
    _call_attr(temp_eta_plugin, _member("debug_log_throttled"), 50.0, 30.0, "hello")
    assert calls == ["hello", "hello"]


def test_suppress_while_printing_enabled_defaults_true_without_settings(
    temp_eta_plugin: Any,
) -> None:
    """Test suppress while printing enabled defaults true without settings."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("settings"), None)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("suppress_while_printing_enabled"),
        )
        is True
    )


def test_suppress_while_printing_enabled_returns_true_on_settings_error(
    temp_eta_plugin: Any,
) -> None:
    """Test suppress while printing enabled returns true on settings error."""
    plugin_any = cast(Any, temp_eta_plugin)

    class _BadSettings:
        """Provide a broken/misconfigured stub for error-path tests."""

        def get_boolean(self, _path: list[str]) -> bool:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("settings"), _BadSettings())
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("suppress_while_printing_enabled"),
        )
        is True
    )


def test_is_print_job_active_returns_false_when_printer_methods_raise(
    temp_eta_plugin: Any,
) -> None:
    """Test is print job active returns false when printer methods raise."""
    plugin_any = cast(Any, temp_eta_plugin)

    class _BadPrinter:
        """Provide a broken/misconfigured stub for error-path tests."""

        def is_printing(self) -> bool:
            """Return dummy state for tests."""
            raise RuntimeError("boom")

        def is_paused(self) -> bool:
            """Return dummy state for tests."""
            raise RuntimeError("boom")

        def get_state_id(self) -> str:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("printer"), _BadPrinter())
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("is_print_job_active"),
        )
        is False
    )


def test_refresh_debug_logging_flag_handles_settings_error(
    temp_eta_plugin: Any,
) -> None:
    """Test refresh debug logging flag handles settings error."""
    plugin_any = cast(Any, temp_eta_plugin)

    class _BadSettings:
        """Provide a broken/misconfigured stub for error-path tests."""

        def get_boolean(self, _path: list[str]) -> bool:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("settings"), _BadSettings())
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _call_attr(
        temp_eta_plugin,
        _member("refresh_debug_logging_flag"),
    )
    assert _get_attr(plugin_any, _member("debug_logging_enabled")) is False


def test_debug_log_swallows_logger_exceptions(temp_eta_plugin: Any) -> None:
    """Test debug log swallows logger exceptions."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)

    class _BadLogger:
        """Provide a broken/misconfigured stub for error-path tests."""

        def info(self, *args: Any, **kwargs: Any) -> None:
            """Provide a test logger stub method."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("logger"), _BadLogger())
    _call_attr(temp_eta_plugin, _member("debug_log"), "hello")


def test_is_print_job_active_checks_paused_and_state_id(temp_eta_plugin: Any) -> None:
    """Test is print job active checks paused and state id."""
    plugin_any = cast(Any, temp_eta_plugin)

    _set_attr(plugin_any, _member("printer"), DummyPrinter(printing=False, paused=True))
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("is_print_job_active"),
        )
        is True
    )

    _set_attr(
        plugin_any,
        _member("printer"),
        DummyPrinter(printing=False, paused=False, state_id="PAUSING"),
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("is_print_job_active"),
        )
        is True
    )

    _set_attr(
        plugin_any,
        _member("printer"),
        DummyPrinter(printing=False, paused=False, state_id="OPERATIONAL"),
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("is_print_job_active"),
        )
        is False
    )


def test_get_current_profile_id_returns_default_on_exception(
    temp_eta_plugin: Any,
) -> None:
    """Test get current profile id returns default on exception."""
    plugin_any = cast(Any, temp_eta_plugin)

    class _BadProfileMgr:
        """Provide a broken/misconfigured stub for error-path tests."""

        def get_current_or_default(self) -> dict[str, Any]:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("printer_profile_manager"), _BadProfileMgr())
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("get_current_profile_id"),
        )
        == "default"
    )


def test_read_history_maxlen_setting_sanitizes(temp_eta_plugin: Any) -> None:
    """Test read history maxlen setting sanitizes."""
    plugin_any = cast(Any, temp_eta_plugin)

    _get_attr(plugin_any, _member("settings")).set(["history_size"], 1)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("read_history_maxlen_setting"),
        )
        == 10
    )

    _get_attr(plugin_any, _member("settings")).set(["history_size"], 999)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("read_history_maxlen_setting"),
        )
        == 300
    )

    _get_attr(plugin_any, _member("settings")).set(["history_size"], 42)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("read_history_maxlen_setting"),
        )
        == 42
    )


def test_read_history_maxlen_setting_uses_default_on_settings_error(
    temp_eta_plugin: Any,
) -> None:
    """Test read history maxlen setting uses default on settings error."""
    plugin_any = cast(Any, temp_eta_plugin)
    default_size = int(_get_attr(plugin_any, _member("default_history_size")))

    class _BadSettings:
        """Provide a broken/misconfigured stub for error-path tests."""

        def get_int(self, _path: list[str]) -> int:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("settings"), _BadSettings())
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("read_history_maxlen_setting"),
        )
        == default_size
    )


def test_set_history_maxlen_rebuilds_and_marks_dirty(temp_eta_plugin: Any) -> None:
    """Test set history maxlen rebuilds and marks dirty."""
    plugin_any = cast(Any, temp_eta_plugin)

    _get_attr(plugin_any, _member("temp_history"))["tool0"] = deque(
        [(1.0, 10.0, 50.0), (2.0, 11.0, 50.0), (3.0, 12.0, 50.0)], maxlen=60
    )
    _set_attr(plugin_any, _member("history_dirty"), False)
    _set_attr(plugin_any, _member("history_maxlen"), 60)

    _call_attr(temp_eta_plugin, _member("set_history_maxlen"), 2)
    assert _get_attr(plugin_any, _member("history_maxlen")) == 2
    assert list(_get_attr(plugin_any, _member("temp_history"))["tool0"]) == [
        (2.0, 11.0, 50.0),
        (3.0, 12.0, 50.0),
    ]
    assert _get_attr(plugin_any, _member("history_dirty")) is True


def test_read_history_maxlen_setting_returns_default_without_settings(
    temp_eta_plugin: Any,
) -> None:
    """Test read history maxlen setting returns default without settings."""
    plugin_any = cast(Any, temp_eta_plugin)
    default_size = int(_get_attr(plugin_any, _member("default_history_size")))
    _set_attr(plugin_any, _member("settings"), None)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("read_history_maxlen_setting"),
        )
        == default_size
    )


def test_set_history_maxlen_nonpositive_uses_default(temp_eta_plugin: Any) -> None:
    """Test set history maxlen nonpositive uses default."""
    plugin_any = cast(Any, temp_eta_plugin)
    default_size = int(_get_attr(plugin_any, _member("default_history_size")))
    _set_attr(plugin_any, _member("history_maxlen"), 60)
    _set_attr(
        plugin_any,
        _member("temp_history"),
        {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)},
    )

    _call_attr(temp_eta_plugin, _member("set_history_maxlen"), 0)
    assert _get_attr(plugin_any, _member("history_maxlen")) == default_size
    assert (
        _get_attr(plugin_any, _member("temp_history"))["tool0"].maxlen == default_size
    )


def test_is_heater_supported_branches_and_debug_cache(temp_eta_plugin: Any) -> None:
    """Test is heater supported branches and debug cache."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("last_heater_support_decision"), {})

    # Capture support-change logs (only emitted on transitions).
    logged: list[str] = []
    _set_attr(
        plugin_any, _member("debug_log"), lambda msg, *args: logged.append(str(msg))
    )

    assert _call_attr(temp_eta_plugin, _member("is_heater_supported"), "bed") is True
    assert (
        _call_attr(temp_eta_plugin, _member("is_heater_supported"), "chamber") is False
    )
    assert _call_attr(temp_eta_plugin, _member("is_heater_supported"), "tool0") is True
    assert _call_attr(temp_eta_plugin, _member("is_heater_supported"), "tool1") is False
    assert _call_attr(temp_eta_plugin, _member("is_heater_supported"), "toolX") is False
    assert (
        _call_attr(temp_eta_plugin, _member("is_heater_supported"), "mystery") is False
    )

    # Ensure cache is populated for at least one heater.
    assert "bed" in _get_attr(plugin_any, _member("last_heater_support_decision"))
    assert logged


def test_is_heater_supported_logs_when_no_profile(temp_eta_plugin: Any) -> None:
    """Test is heater supported logs when no profile."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("last_heater_support_decision"), {})

    class _EmptyProfileMgr:
        """Provide an empty stub for edge-case tests."""

        def get_current_or_default(self) -> dict[str, Any]:
            """Return dummy value for tests."""
            return {}

    _set_attr(plugin_any, _member("printer_profile_manager"), _EmptyProfileMgr())

    logs: list[str] = []
    _set_attr(
        plugin_any, _member("debug_log"), lambda msg, *args: logs.append(str(msg))
    )

    assert _call_attr(temp_eta_plugin, _member("is_heater_supported"), "bed") is False
    assert logs


def test_is_heater_supported_logs_on_exception(temp_eta_plugin: Any) -> None:
    """Test is heater supported logs on exception."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("last_heater_support_decision"), {})

    class _BoomProfileMgr:
        """Raise errors intentionally for failure-path tests."""

        def get_current_or_default(self) -> dict[str, Any]:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("printer_profile_manager"), _BoomProfileMgr())

    logs: list[str] = []
    _set_attr(
        plugin_any, _member("debug_log"), lambda msg, *args: logs.append(str(msg))
    )

    assert _call_attr(temp_eta_plugin, _member("is_heater_supported"), "bed") is False
    assert any("Heater support error" in m for m in logs)


def test_switch_active_profile_logs_profile_summary_when_debug_enabled(
    tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test switch active profile logs profile summary when debug enabled."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)

    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("active_profile_id"), "old")

    messages: list[str] = []
    _set_attr(
        plugin_any, _member("debug_log"), lambda msg, *args: messages.append(str(msg))
    )

    _call_attr(temp_eta_plugin, _member("switch_active_profile_if_needed"), force=True)
    assert any("Profile summary" in m for m in messages)


def test_switch_active_profile_logs_profile_summary_unavailable_on_exception(
    tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test switch active profile logs profile summary unavailable on exception."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)

    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("active_profile_id"), "old")

    class _BoomProfileMgr:
        """Raise errors intentionally for failure-path tests."""

        def get_current_or_default(self) -> dict[str, Any]:
            """Return dummy value for tests."""
            raise RuntimeError("boom")

    _set_attr(plugin_any, _member("printer_profile_manager"), _BoomProfileMgr())

    messages: list[str] = []
    _set_attr(
        plugin_any, _member("debug_log"), lambda msg, *args: messages.append(str(msg))
    )

    _call_attr(temp_eta_plugin, _member("switch_active_profile_if_needed"), force=True)
    assert any("Profile summary unavailable" in m for m in messages)


def test_switch_active_profile_non_forced_clears_live_history_and_sends_clear(
    tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test switch active profile non forced clears live history and sends clear."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)

    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("active_profile_id"), "old")
    _set_attr(plugin_any, _member("history_dirty"), False)

    # Seed old heaters so we can verify clear messages.
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {
            "tool0": deque([(1.0, 10.0, 50.0)], maxlen=60),
            "bed": deque([(1.0, 10.0, 50.0)], maxlen=60),
        },
    )

    logs: list[str] = []
    _set_attr(
        plugin_any, _member("debug_log"), lambda msg, *args: logs.append(str(msg))
    )

    pm = cast(DummyPluginManager, _get_attr(plugin_any, _member("plugin_manager")))
    pm.messages.clear()

    _call_attr(temp_eta_plugin, _member("switch_active_profile_if_needed"), force=False)

    assert _get_attr(plugin_any, _member("active_profile_id")) == "default"
    assert _get_attr(temp_eta_plugin, _member("temp_history")) == {}
    assert any("Cleared live (RAM) history" in m for m in logs)

    cleared = [
        m["payload"].get("heater")
        for m in pm.messages
        if m["payload"].get("eta") is None
    ]
    assert set(cleared) >= {"tool0", "bed"}


def test_cooldown_mode_defaults_to_threshold_on_invalid(temp_eta_plugin: Any) -> None:
    """Test cooldown mode defaults to threshold on invalid."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "nope")
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_mode"),
        )
        == "threshold"
    )


def test_cooldown_hysteresis_and_fit_window_clamp(temp_eta_plugin: Any) -> None:
    """Test cooldown hysteresis and fit window clamp."""
    plugin_any = cast(Any, temp_eta_plugin)

    _get_attr(plugin_any, _member("settings")).set(["cooldown_hysteresis_c"], 0)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_hysteresis_c"),
        )
        == 1.0
    )

    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 5)
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_fit_window_seconds"),
        )
        == 10.0
    )

    _get_attr(plugin_any, _member("settings")).set(
        ["cooldown_fit_window_seconds"], 99999
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_fit_window_seconds"),
        )
        == 1800.0
    )


def test_get_cooldown_threshold_target_per_heater(temp_eta_plugin: Any) -> None:
    """Test get cooldown threshold target per heater."""
    plugin_any = cast(Any, temp_eta_plugin)

    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_tool0"], 55.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_bed"], 44.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_chamber"], 33.0)

    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_threshold_target_c"), "tool0")
        == 55.0
    )
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_threshold_target_c"), "bed")
        == 44.0
    )
    assert (
        _call_attr(
            temp_eta_plugin, _member("get_cooldown_threshold_target_c"), "chamber"
        )
        == 33.0
    )
    assert (
        _call_attr(
            temp_eta_plugin, _member("get_cooldown_threshold_target_c"), "unknown"
        )
        is None
    )


def test_get_cooldown_ambient_c_prefers_user_then_baseline_then_history(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test get cooldown ambient c prefers user then baseline then history."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], 21.0)
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_ambient_c"), "tool0") == 21.0
    )

    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], None)
    _get_attr(plugin_any, _member("cooldown_ambient_baseline"))["tool0"] = 19.5
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_ambient_c"), "tool0") == 19.5
    )

    # With no baseline, derive a conservative estimate from history
    # (requires a min notably below current).
    _get_attr(plugin_any, _member("cooldown_ambient_baseline")).pop("tool0", None)
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(90.0, 60.0), (95.0, 40.0), (100.0, 50.0)], maxlen=60
    )
    amb = _call_attr(temp_eta_plugin, _member("get_cooldown_ambient_c"), "tool0")
    assert amb is not None
    assert abs(amb - 39.5) < 1e-6


def test_get_cooldown_ambient_c_ignores_invalid_user_setting(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test get cooldown ambient c ignores invalid user setting."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    # Invalid ambient setting should be ignored (exception path).
    _get_attr(plugin_any, _member("settings")).set(
        ["cooldown_ambient_temp"], "not-a-number"
    )
    _get_attr(plugin_any, _member("cooldown_ambient_baseline")).pop("tool0", None)
    _get_attr(plugin_any, _member("cooldown_history")).pop("tool0", None)

    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_ambient_c"), "tool0") is None
    )


def test_get_cooldown_display_target_ambient_adds_band(temp_eta_plugin: Any) -> None:
    """Test get cooldown display target ambient adds band."""
    plugin_any = cast(Any, temp_eta_plugin)

    # Force a known ambient and ensure we add at least a 1°C band.
    _set_attr(plugin_any, _member("get_cooldown_ambient_c"), lambda heater: 20.0)

    goal = _call_attr(
        temp_eta_plugin,
        _member("get_cooldown_display_target_c"),
        heater_name="tool0",
        actual_c=50.0,
        mode="ambient",
        hysteresis_c=0.2,
    )
    assert goal == 21.0


def test_calculate_cooldown_linear_eta_paths(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate cooldown linear eta paths."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_time(monkeypatch, 100.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 120)

    # Happy path: negative slope.
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(90.0, 60.0), (100.0, 50.0)], maxlen=60
    )
    eta = _call_attr(
        temp_eta_plugin, _member("calculate_cooldown_linear_eta"), "tool0", goal_c=40.0
    )
    assert eta is not None
    assert abs(eta - 10.0) < 1e-6

    # Not enough recent samples -> debug log + None.
    logged: list[str] = []
    _set_attr(
        plugin_any, _member("debug_log"), lambda msg, *args: logged.append(str(msg))
    )
    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 10)
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(0.0, 60.0), (1.0, 59.0)], maxlen=60
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_linear_eta"),
            "tool0",
            goal_c=40.0,
        )
        is None
    )
    assert logged

    # Slope not negative -> debug log + None.
    logged.clear()
    _set_time(monkeypatch, 200.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 120)
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(90.0, 50.0), (100.0, 55.0)], maxlen=60
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_linear_eta"),
            "tool0",
            goal_c=40.0,
        )
        is None
    )
    assert logged


def test_calculate_cooldown_eta_seconds_ambient_mode_calls_exponential(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate cooldown eta seconds ambient mode calls exponential."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], 20.0)

    called: list[dict[str, Any]] = []

    def _fake_exp(**kwargs: Any) -> float:
        """Provide a local test helper callback."""
        called.append(dict(kwargs))
        return 123.0

    _set_attr(plugin_any, _member("calculate_cooldown_exponential_eta"), _fake_exp)
    eta = _call_attr(
        temp_eta_plugin,
        _member("calculate_cooldown_eta_seconds"),
        heater_name="tool0",
        actual_c=60.0,
        display_target_c=25.0,
        mode="ambient",
        hysteresis_c=1.0,
    )
    assert eta == 123.0
    assert called


def test_reset_user_settings_to_defaults_returns_when_no_settings(
    temp_eta_plugin: Any,
) -> None:
    """Test reset user settings to defaults returns when no settings."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(plugin_any, _member("settings"), None)
    _call_attr(
        temp_eta_plugin,
        _member("reset_user_settings_to_defaults"),
    )


def test_reset_user_settings_to_defaults_applies_runtime_state(
    temp_eta_plugin: Any,
) -> None:
    """Test reset user settings to defaults applies runtime state."""
    plugin_any = cast(Any, temp_eta_plugin)

    # Make settings differ from defaults.
    _get_attr(plugin_any, _member("settings")).set(["enabled"], False)
    _get_attr(plugin_any, _member("settings")).set(["history_size"], 10)
    _get_attr(plugin_any, _member("settings")).set(["debug_logging"], True)

    # Make runtime state differ too.
    _set_attr(plugin_any, _member("history_maxlen"), 10)
    _get_attr(plugin_any, _member("temp_history"))["tool0"] = deque(
        [(1.0, 10.0, 50.0)], maxlen=10
    )
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)

    def _raise_save() -> None:
        """Provide a local test helper."""
        raise RuntimeError("save failed")

    _get_attr(plugin_any, _member("settings")).save = _raise_save

    _call_attr(
        temp_eta_plugin,
        _member("reset_user_settings_to_defaults"),
    )

    defaults = temp_eta_plugin.get_settings_defaults()
    default_history_size = defaults["history_size"]
    assert default_history_size is not None

    assert _get_attr(plugin_any, _member("settings")).get_boolean(["enabled"]) == bool(
        defaults["enabled"]
    )
    assert _get_attr(plugin_any, _member("settings")).get_int(["history_size"]) == int(
        default_history_size
    )

    # History size reset should be applied.
    assert _get_attr(plugin_any, _member("history_maxlen")) == int(default_history_size)
    assert _get_attr(plugin_any, _member("temp_history"))["tool0"].maxlen == int(
        default_history_size
    )


def test_asset_and_api_hooks_shape(temp_eta_plugin: Any) -> None:
    """Test asset and api hooks shape."""
    assets = temp_eta_plugin.get_assets()
    # Styling ships as pre-compiled CSS (not LESS) so it survives pip installs
    # on hosts without a server-side LESS compiler.
    assert "js" in assets and "css" in assets

    assert temp_eta_plugin.is_api_protected() is True
    assert temp_eta_plugin.is_api_adminonly() is True

    commands = temp_eta_plugin.get_api_commands()
    assert "reset_profile_history" in commands
    assert "reset_settings_defaults" in commands


def test_template_configs_and_autoescape(temp_eta_plugin: Any) -> None:
    """Test template configs and autoescape."""
    assert temp_eta_plugin.is_template_autoescaped() is True
    cfgs = temp_eta_plugin.get_template_configs()
    assert isinstance(cfgs, list)
    assert {c.get("type") for c in cfgs if isinstance(c, dict)} >= {
        "navbar",
        "sidebar",
        "settings",
        "tab",
    }


def test_settings_helpers_default_and_exception_paths(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test settings helpers default and exception paths."""
    p_any = cast(Any, temp_eta_plugin)

    # No settings attached: return safe defaults.
    _set_attr(p_any, _member("settings"), None)
    _set_attr(p_any, _member("debug_logging_enabled"), True)
    _call_attr(
        temp_eta_plugin,
        _member("refresh_debug_logging_flag"),
    )
    assert _get_attr(p_any, _member("debug_logging_enabled")) is False

    assert (
        _call_attr(
            temp_eta_plugin,
            _member("suppress_while_printing_enabled"),
        )
        is True
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("heating_enabled"),
        )
        is True
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_enabled"),
        )
        is False
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_mode"),
        )
        == "threshold"
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_hysteresis_c"),
        )
        == 1.0
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_fit_window_seconds"),
        )
        == 120.0
    )

    # Settings present, but getters raise: helpers should fall back to defaults.
    settings = DummySettings({"debug_logging": True})

    def _boom(*_args: Any, **_kwargs: Any) -> Any:
        """Provide a local test helper callback."""
        raise RuntimeError("boom")

    monkeypatch.setattr(settings, "get_boolean", _boom)
    monkeypatch.setattr(settings, "get", _boom)
    monkeypatch.setattr(settings, "get_float", _boom)
    monkeypatch.setattr(settings, "get_int", _boom)

    _set_attr(p_any, _member("settings"), settings)

    _call_attr(
        temp_eta_plugin,
        _member("refresh_debug_logging_flag"),
    )
    assert _get_attr(p_any, _member("debug_logging_enabled")) is False

    assert (
        _call_attr(
            temp_eta_plugin,
            _member("suppress_while_printing_enabled"),
        )
        is True
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("heating_enabled"),
        )
        is True
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_enabled"),
        )
        is False
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_mode"),
        )
        == "threshold"
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_hysteresis_c"),
        )
        == 1.0
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("cooldown_fit_window_seconds"),
        )
        == 120.0
    )


def test_load_profile_history_invalid_json_and_shape(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test load profile history invalid json and shape."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(temp_eta_plugin, _member("persist_max_age_seconds"), 10.0)
    _set_time(monkeypatch, 100.0)

    # Invalid JSON should be handled.
    (tmp_path / "history_default.json").write_text("{not json", encoding="utf-8")
    assert _call_attr(temp_eta_plugin, _member("load_profile_history"), "default") == {}

    # Wrong top-level shape should be ignored.
    (tmp_path / "history_default.json").write_text(
        json.dumps([1, 2, 3]), encoding="utf-8"
    )
    assert _call_attr(temp_eta_plugin, _member("load_profile_history"), "default") == {}

    # samples not a dict -> ignored.
    (tmp_path / "history_default.json").write_text(
        json.dumps({"samples": [1, 2, 3]}), encoding="utf-8"
    )
    assert _call_attr(temp_eta_plugin, _member("load_profile_history"), "default") == {}


def test_load_profile_history_skips_invalid_heater_and_point_shapes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test load profile history skips invalid heater and point shapes."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(temp_eta_plugin, _member("persist_max_age_seconds"), 10.0)
    _set_time(monkeypatch, 100.0)

    # JSON keys are always strings, so to hit the defensive branch that rejects
    # non-string heater keys we monkeypatch json.loads to return such a dict.
    payload = {
        "version": 1,
        "saved_at": 100.0,
        "profile_id": "default",
        "history_size": 60,
        "samples": {
            123: [[95.0, 20.0, 50.0]],
            "tool0": "nope",
            "bed": [[95.0, 20.0]],
            "chamber": [["bad", "x", "y"]],
        },
    }
    (tmp_path / "history_default.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(octoprint_temp_eta.json, "loads", lambda _text: payload)
    assert _call_attr(temp_eta_plugin, _member("load_profile_history"), "default") == {}


def test_on_settings_save_toggles_debug_updates_history_and_handles_non_dict_saved(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on settings save toggles debug updates history and handles non dict saved."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))

    logger = InfoRecordingLogger()
    _set_attr(p_any, _member("logger"), logger)

    settings.set(["enabled"], True)
    settings.set(["debug_logging"], False)
    settings.set(["history_size"], 60)
    _set_attr(p_any, _member("debug_logging_enabled"), False)

    _set_attr(p_any, _member("history_maxlen"), 60)
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {
            "tool0": deque([(1.0, 10.0, 50.0)], maxlen=60),
            "bed": deque([(1.0, 10.0, 50.0)], maxlen=60),
        },
    )

    def _fake_save(_self: Any, _data: dict[str, Any]) -> str:
        """Provide a local test helper callback."""
        settings.set(["enabled"], False)
        settings.set(["debug_logging"], True)
        settings.set(["history_size"], 50)
        return "ok"

    monkeypatch.setattr(
        octoprint_temp_eta.octoprint.plugin.SettingsPlugin,
        "on_settings_save",
        _fake_save,
    )
    result = temp_eta_plugin.on_settings_save({"enabled": False})

    assert result == {}
    assert any("Debug logging" in msg for msg in logger.info_calls)
    assert _get_attr(p_any, _member("history_maxlen")) == 50
    assert _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"].maxlen == 50

    pm = cast(DummyPluginManager, _get_attr(p_any, _member("plugin_manager")))
    assert any(
        m["payload"].get("type") == "eta_update" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_on_settings_save_sanitizes_numeric_payload_before_delegating(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on settings save sanitizes numeric payload before delegating."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))

    captured: dict[str, Any] = {}

    def _fake_save(_self: Any, data: dict[str, Any]) -> dict[str, Any]:
        """Provide a local test helper callback."""
        captured.update(data)
        # Simulate persisted values.
        for k, v in data.items():
            settings.set([k], v)
        return data

    monkeypatch.setattr(
        octoprint_temp_eta.octoprint.plugin.SettingsPlugin,
        "on_settings_save",
        _fake_save,
    )

    temp_eta_plugin.on_settings_save(
        {
            "threshold_start": -1,
            "update_interval": 999,
            "history_size": -50,
            "historical_graph_window_seconds": 99999,
            "sound_volume": -5,
            "notification_timeout_s": 0,
            "cooldown_target_tool0": -10,
            "cooldown_ambient_temp": -20,
            "cooldown_fit_window_seconds": 0,
        }
    )

    assert captured["threshold_start"] == 1.0
    assert captured["update_interval"] == 5.0
    assert captured["history_size"] == 10
    assert captured["historical_graph_window_seconds"] == 1800
    assert captured["sound_volume"] == 0.0
    assert captured["notification_timeout_s"] == 1.0
    assert captured["cooldown_target_tool0"] == 0.0
    assert captured["cooldown_ambient_temp"] is None
    assert captured["cooldown_fit_window_seconds"] == 10


def test_on_settings_save_reconfigures_mqtt_client(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Saving settings should reconfigure the MQTT client when present."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))

    settings.set(["mqtt_enabled"], True)
    settings.set(["mqtt_broker_host"], "broker")
    settings.set(["mqtt_broker_port"], 1883)
    settings.set(["mqtt_username"], "u")
    settings.set(["mqtt_password"], "p")
    settings.set(["mqtt_use_tls"], False)
    settings.set(["mqtt_tls_insecure"], False)
    settings.set(["mqtt_base_topic"], "octoprint/temp_eta")
    settings.set(["mqtt_qos"], 1)
    settings.set(["mqtt_retain"], True)
    settings.set(["mqtt_publish_interval"], 2.0)

    class RecordingMQTT:
        """Record calls for test assertions."""

        def __init__(self) -> None:
            """Initialize test helper state."""
            self.configured: dict[str, Any] = {}

        def configure(self, cfg: dict[str, Any]) -> None:
            """Provide a test stub implementation."""
            self.configured = dict(cfg)

    mqtt_client = RecordingMQTT()
    _set_attr(p_any, _member("mqtt_client"), mqtt_client)

    monkeypatch.setattr(
        octoprint_temp_eta.octoprint.plugin.SettingsPlugin,
        "on_settings_save",
        lambda _self, _data: {},
    )
    temp_eta_plugin.on_settings_save({"mqtt_enabled": True})

    assert mqtt_client.configured.get("mqtt_enabled") is True
    assert mqtt_client.configured.get("mqtt_broker_host") == "broker"
    assert mqtt_client.configured.get("mqtt_broker_port") == 1883


def test_on_printer_add_temperature_records_sample_and_triggers_update(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature records sample and triggers update."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["threshold_start"], 5.0)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 0.0)
    _get_attr(plugin_any, _member("settings")).set(["enable_heating_eta"], True)

    calls: list[Any] = []
    _set_attr(
        plugin_any,
        _member("calculate_and_broadcast_eta"),
        calls.append,
    )
    _set_attr(plugin_any, _member("maybe_persist_history"), lambda now: None)

    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 20.0, "target": 40.0}}
    )

    assert calls
    assert "tool0" in _get_attr(plugin_any, _member("temp_history"))
    assert len(_get_attr(plugin_any, _member("temp_history"))["tool0"]) == 1
    assert _get_attr(plugin_any, _member("history_dirty")) is True


def test_on_printer_add_temperature_suppresses_while_printing_and_clears_once(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature suppresses while printing and clears once."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["suppress_while_printing"], True)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 0.0)

    _set_attr(plugin_any, _member("printer"), DummyPrinter(printing=True))
    _set_attr(plugin_any, _member("suppressing_due_to_print"), False)

    # Seed some state so clear messages are sent.
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)},
    )

    _set_attr(
        plugin_any,
        _member("calculate_and_broadcast_eta"),
        lambda _data: (_ for _ in ()).throw(
            AssertionError("should not compute while suppressed")
        ),
    )

    pm = cast(DummyPluginManager, _get_attr(plugin_any, _member("plugin_manager")))
    before = len(pm.messages)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 20.0, "target": 40.0}}
    )
    after_first = len(pm.messages)

    assert _get_attr(plugin_any, _member("suppressing_due_to_print")) is True
    assert after_first > before

    # Second call: still suppressed, should not clear again.
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 21.0, "target": 41.0}}
    )
    assert len(pm.messages) == after_first


def test_on_printer_add_temperature_unsuppresses_when_job_not_active(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature unsuppresses when job not active."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["suppress_while_printing"], True)
    _get_attr(plugin_any, _member("settings")).set(["threshold_start"], 5.0)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 0.0)
    _get_attr(plugin_any, _member("settings")).set(["enable_heating_eta"], True)

    # Not printing anymore.
    _set_attr(plugin_any, _member("printer"), DummyPrinter(printing=False))
    _set_attr(plugin_any, _member("suppressing_due_to_print"), True)

    called: list[Any] = []
    _set_attr(
        plugin_any,
        _member("calculate_and_broadcast_eta"),
        called.append,
    )
    _set_attr(plugin_any, _member("maybe_persist_history"), lambda now: None)

    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 20.0, "target": 40.0}}
    )
    assert _get_attr(plugin_any, _member("suppressing_due_to_print")) is False
    assert called


def test_on_printer_add_temperature_updates_ambient_baseline_when_lower(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature updates ambient baseline when lower."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 999.0)

    _get_attr(plugin_any, _member("cooldown_ambient_baseline"))["tool0"] = 100.0
    temp_eta_plugin.on_printer_add_temperature({"tool0": {"actual": 90.0, "target": 0}})
    assert (
        _get_attr(plugin_any, _member("cooldown_ambient_baseline")).get("tool0") == 90.0
    )


def test_on_printer_add_temperature_skips_when_holding_or_below_threshold(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature skips when holding or below threshold."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _set_attr(plugin_any, _member("temp_history"), {})
    _set_attr(plugin_any, _member("history_dirty"), False)

    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["threshold_start"], 5.0)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 0.0)
    _get_attr(plugin_any, _member("settings")).set(["enable_heating_eta"], True)

    calls: list[Any] = []
    _set_attr(
        plugin_any,
        _member("calculate_and_broadcast_eta"),
        calls.append,
    )
    _set_attr(plugin_any, _member("maybe_persist_history"), lambda now: None)

    # remaining <= epsilon_hold (0.2) => no history record.
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 39.9, "target": 40.0}}
    )
    assert calls
    assert (
        "tool0" not in _get_attr(plugin_any, _member("temp_history"))
        or len(_get_attr(plugin_any, _member("temp_history"))["tool0"]) == 0
    )
    assert _get_attr(plugin_any, _member("history_dirty")) is False

    calls.clear()
    # remaining < threshold => no history record.
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 37.0, "target": 40.0}}
    )
    assert calls
    assert (
        "tool0" not in _get_attr(plugin_any, _member("temp_history"))
        or len(_get_attr(plugin_any, _member("temp_history"))["tool0"]) == 0
    )
    assert _get_attr(plugin_any, _member("history_dirty")) is False


def test_on_printer_add_temperature_non_numeric_target_tracks_cooldown_and_baseline(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature non numeric target tracks cooldown and baseline."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 0.0)

    # Pretend we were heating before, so we take the "cooldown start" path.
    _get_attr(plugin_any, _member("last_target_by_heater"))["tool0"] = 200.0

    debug_calls: list[Any] = []
    _set_attr(
        plugin_any,
        _member("debug_log_throttled"),
        lambda *args, **kwargs: debug_calls.append((args, kwargs)),
    )

    _set_attr(plugin_any, _member("calculate_and_broadcast_eta"), lambda data: None)
    _set_attr(plugin_any, _member("maybe_persist_history"), lambda now: None)

    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 100.0, "target": "off"}}
    )

    assert debug_calls  # should log non-numeric target / cooldown start
    assert "tool0" in _get_attr(plugin_any, _member("cooldown_history"))
    assert len(_get_attr(plugin_any, _member("cooldown_history"))["tool0"]) == 1
    assert (
        _get_attr(plugin_any, _member("cooldown_ambient_baseline")).get("tool0")
        == 100.0
    )


def test_on_printer_add_temperature_skips_invalid_actual_values_and_creates_cooldown_history(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature skips invalid actual values and creates cooldown history."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_time(monkeypatch, 100.0)

    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 999.0)

    # Ensure debug path is active so coverage records the non-numeric target handler.
    _set_attr(plugin_any, _member("debug_logging_enabled"), True)
    _set_attr(plugin_any, _member("last_debug_log_time"), 0.0)

    _set_attr(plugin_any, _member("calculate_and_broadcast_eta"), lambda data: None)
    _set_attr(plugin_any, _member("maybe_persist_history"), lambda now: None)

    temp_eta_plugin.on_printer_add_temperature(
        {
            "tool0": {"actual": None, "target": 0},
            "tool1": {"actual": "abc", "target": 0},
            "tool2": {"actual": 100.0, "target": "off"},
        }
    )

    assert "tool2" in _get_attr(plugin_any, _member("cooldown_history"))
    assert len(_get_attr(plugin_any, _member("cooldown_history"))["tool2"]) == 1
    # Baseline should be learned when previously unset.
    assert (
        _get_attr(plugin_any, _member("cooldown_ambient_baseline")).get("tool2")
        == 100.0
    )


def test_printer_callback_stubs_do_not_crash(temp_eta_plugin: Any) -> None:
    """Test printer callback stubs do not crash."""
    temp_eta_plugin.on_printer_send_current_data({"state": "ok"})
    temp_eta_plugin.on_printer_add_log({"line": "hello"})


def test_on_printer_add_temperature_respects_update_interval(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on printer add temperature respects update interval."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _get_attr(plugin_any, _member("settings")).set(["threshold_start"], 5.0)
    _get_attr(plugin_any, _member("settings")).set(["update_interval"], 10.0)
    _get_attr(plugin_any, _member("settings")).set(["enable_heating_eta"], True)

    called: list[Any] = []
    _set_attr(
        plugin_any,
        _member("calculate_and_broadcast_eta"),
        called.append,
    )
    _set_attr(plugin_any, _member("maybe_persist_history"), lambda now: None)

    # First call triggers (last_update_time starts at 0).
    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 20.0, "target": 40.0}}
    )
    assert called

    called.clear()
    # Second call within interval should NOT trigger.
    _set_time(monkeypatch, 105.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 21.0, "target": 40.0}}
    )
    assert not called


def test_calculate_and_broadcast_eta_skips_non_dict_and_unsupported(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta skips non dict and unsupported."""
    plugin_any = cast(Any, temp_eta_plugin)

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()

    def _supported(heater: str) -> bool:
        """Provide a local test helper."""
        return heater == "bed"

    _set_attr(plugin_any, _member("is_heater_supported"), _supported)

    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {
            "time": 123,
            "tool0": {"actual": 20.0, "target": 40.0},
            "bed": {"actual": 20.0, "target": 40.0},
        },
    )

    pm = cast(DummyPluginManager, _get_attr(plugin_any, _member("plugin_manager")))
    assert pm.messages
    last = pm.messages[-1]["payload"]
    assert last["heater"] == "bed"


def test_calculate_and_broadcast_eta_auto_creates_history_for_new_heater(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta auto creates history for new heater."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()

    # Force support for tool1 and ensure it's not already tracked.
    _set_attr(
        plugin_any, _member("is_heater_supported"), lambda heater: heater == "tool1"
    )
    _get_attr(temp_eta_plugin, _member("temp_history")).pop("tool1", None)

    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool1": {"actual": 20.0, "target": 40.0}},
    )
    assert "tool1" in _get_attr(temp_eta_plugin, _member("temp_history"))


def test_calculate_and_broadcast_eta_cooldown_threshold_skips_when_below_hysteresis(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta cooldown threshold skips when below hysteresis."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "threshold")
    _get_attr(plugin_any, _member("settings")).set(["cooldown_hysteresis_c"], 1.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_tool0"], 50.0)

    # If called, the test should fail.
    _set_attr(
        plugin_any,
        _member("calculate_cooldown_eta_seconds"),
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("should not compute cooldown eta")
        ),
    )

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {
            "tool0": {"actual": 50.5, "target": 0},
        },
    )

    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["cooldown_mode"] == "threshold"
    assert msg["cooldown_target"] == 50.0


def test_calculate_and_broadcast_eta_cooldown_ambient_computes_and_sends_kind(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta cooldown ambient computes and sends kind."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "ambient")
    _get_attr(plugin_any, _member("settings")).set(["cooldown_hysteresis_c"], 2.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], 20.0)

    _set_attr(
        plugin_any,
        _member("calculate_cooldown_eta_seconds"),
        lambda *args, **kwargs: 5.0,
    )

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {
            "tool0": {"actual": 30.0, "target": 0},
        },
    )

    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] == 5.0
    assert msg["eta_kind"] == "cooling"
    assert msg["cooldown_mode"] == "ambient"
    assert msg["cooldown_target"] == 22.0


def test_calculate_and_broadcast_eta_cooldown_threshold_under_one_second_logs_insufficient_fit(
    temp_eta_plugin: Any,
) -> None:
    """Cooldown-threshold ETA under one second should log insufficient-fit warning."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "threshold")
    _get_attr(plugin_any, _member("settings")).set(["cooldown_hysteresis_c"], 1.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_tool0"], 40.0)

    debug_calls: list[Any] = []
    _set_attr(
        plugin_any,
        _member("debug_log_throttled"),
        lambda *args, **kwargs: debug_calls.append((args, kwargs)),
    )

    _set_attr(
        plugin_any,
        _member("calculate_cooldown_eta_seconds"),
        lambda *args, **kwargs: 0.5,
    )
    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()

    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 45.5, "target": 0}},
    )

    assert any("insufficient fit" in str(args[2]) for (args, _kwargs) in debug_calls)
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None


def test_calculate_and_broadcast_eta_cooldown_target_none_triggers_debug_log(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta cooldown target none triggers debug log."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "ambient")
    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], None)

    calls: list[Any] = []
    _set_attr(
        plugin_any,
        _member("debug_log_throttled"),
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {
            "tool0": {"actual": 30.0, "target": 0},
        },
    )

    assert calls
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["cooldown_target"] is None


def test_calculate_and_broadcast_eta_cooldown_eta_under_one_second_logs_insufficient_fit(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta cooldown eta under one second logs insufficient fit."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "ambient")
    _get_attr(plugin_any, _member("settings")).set(["cooldown_hysteresis_c"], 1.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], 20.0)

    debug_calls: list[Any] = []
    _set_attr(
        plugin_any,
        _member("debug_log_throttled"),
        lambda *args, **kwargs: debug_calls.append((args, kwargs)),
    )

    # Force compute, but return <1s so it is hidden.
    _set_attr(
        plugin_any,
        _member("calculate_cooldown_eta_seconds"),
        lambda *args, **kwargs: 0.5,
    )
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(90.0, 60.0)], maxlen=60
    )

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 30.0, "target": 0}},
    )

    assert any("insufficient fit" in str(args[2]) for (args, _kwargs) in debug_calls)
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None


def test_calculate_and_broadcast_eta_cooldown_forced_target_under_one_second_hits_branches(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate and broadcast eta cooldown forced target under one second hits branches."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "ambient")
    _get_attr(plugin_any, _member("settings")).set(["cooldown_hysteresis_c"], 1.0)

    debug_calls: list[Any] = []
    _set_attr(
        plugin_any,
        _member("debug_log_throttled"),
        lambda *args, **kwargs: debug_calls.append((args, kwargs)),
    )

    monkeypatch.setattr(
        temp_eta_plugin, "_get_cooldown_display_target_c", lambda **_kw: 40.0
    )
    monkeypatch.setattr(
        temp_eta_plugin, "_calculate_cooldown_eta_seconds", lambda **_kw: 0.5
    )

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 60.0, "target": 0}},
    )

    assert any("insufficient fit" in str(args[2]) for (args, _kwargs) in debug_calls)
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["cooldown_target"] == 40.0


def test_calculate_and_broadcast_eta_heating_exponential_and_hide_under_one_second(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta heating exponential and hide under one second."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_heating_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["threshold_start"], 5.0)
    _get_attr(plugin_any, _member("settings")).set(["algorithm"], "exponential")

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _set_attr(
        plugin_any, _member("calculate_exponential_eta"), lambda heater, target: 0.5
    )
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 20.0, "target": 40.0}},
    )

    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["eta_kind"] is None

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _set_attr(
        plugin_any, _member("calculate_exponential_eta"), lambda heater, target: 10.0
    )
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 20.0, "target": 40.0}},
    )
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["eta"] == 10.0
    assert msg["eta_kind"] == "heating"


def test_calculate_and_broadcast_eta_handles_non_numeric_values_and_close_to_target(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta handles non numeric values and close to target."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_heating_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["threshold_start"], 5.0)
    _get_attr(plugin_any, _member("settings")).set(["algorithm"], "linear")

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": "bad", "target": "bad"}},
    )
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None

    # Very close to target (below threshold) -> eta cleared.
    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 39.0, "target": 40.0}},
    )
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["eta"] is None
    assert msg["eta_kind"] is None


def test_calculate_and_broadcast_eta_cooldown_insufficient_fit_logs_history_len(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate and broadcast eta cooldown insufficient fit logs history len."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enable_cooldown_eta"], True)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_mode"], "threshold")
    _get_attr(plugin_any, _member("settings")).set(["cooldown_hysteresis_c"], 1.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_tool0"], 50.0)

    # Ensure there is some history so hist_len path is meaningful.
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(0.0, 70.0)], maxlen=60
    )

    debug: list[str] = []
    _set_attr(
        plugin_any,
        _member("debug_log_throttled"),
        lambda now, interval, message, *args: debug.append(str(message)),
    )

    _set_attr(
        plugin_any,
        _member("calculate_cooldown_eta_seconds"),
        lambda *args, **kwargs: None,
    )

    _get_attr(plugin_any, _member("plugin_manager")).messages.clear()
    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 70.0, "target": 0}},
    )

    assert any("insufficient fit" in m for m in debug)
    msg = _get_attr(plugin_any, _member("plugin_manager")).messages[-1]["payload"]
    assert msg["eta"] is None
    assert msg["cooldown_target"] == 50.0


def test_calculate_exponential_eta_happy_path_returns_number(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate exponential eta happy path returns number."""
    target = 200.0
    _set_time(monkeypatch, 100.0)

    # Smooth heating curve approaching target (remaining decreases).
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [
            (80.0, 150.0, target),
            (85.0, 170.0, target),
            (90.0, 182.0, target),
            (92.0, 188.0, target),
            (95.0, 193.0, target),
            (98.0, 196.0, target),
            (100.0, 197.0, target),
        ],
        maxlen=60,
    )

    eta = _call_attr(
        temp_eta_plugin, _member("calculate_exponential_eta"), "tool0", target
    )
    assert eta is not None
    assert float(eta) >= 0.0


def test_calculate_cooldown_exponential_eta_happy_path(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate cooldown exponential eta happy path."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 120)
    _set_time(monkeypatch, 200.0)

    # Construct an exponential-ish cooldown curve with 6 points.
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [
            (150.0, 80.0),
            (160.0, 65.0),
            (170.0, 54.0),
            (180.0, 46.0),
            (190.0, 40.0),
            (200.0, 35.0),
        ],
        maxlen=60,
    )

    eta = _call_attr(
        temp_eta_plugin,
        _member("calculate_cooldown_exponential_eta"),
        heater_name="tool0",
        ambient_c=20.0,
        goal_c=25.0,
    )
    assert eta is not None
    assert float(eta) > 0.0


def test_cooldown_helpers_early_return_paths(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test cooldown helpers early return paths."""
    plugin_any = cast(Any, temp_eta_plugin)

    # Threshold target validation.
    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_tool0"], "")
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_threshold_target_c"), "tool0")
        is None
    )

    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_tool0"], -5)
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_threshold_target_c"), "tool0")
        is None
    )

    _get_attr(plugin_any, _member("settings")).set(["cooldown_target_tool0"], "nan")
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_threshold_target_c"), "tool0")
        is None
    )

    # Ambient helper: invalid user ambient -> fall back; no baseline/history -> None.
    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], -100)
    _get_attr(plugin_any, _member("cooldown_ambient_baseline")).pop("tool0", None)
    _get_attr(plugin_any, _member("cooldown_history")).pop("tool0", None)
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_ambient_c"), "tool0") is None
    )

    # Ambient helper: history too short (<3 recent points).
    _set_time(monkeypatch, 100.0)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_ambient_temp"], None)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 120)
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(90.0, 30.0), (95.0, 29.0)], maxlen=60
    )
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_ambient_c"), "tool0") is None
    )

    # Ambient helper: minimum is too close to current -> None.
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(90.0, 50.0), (95.0, 49.5), (100.0, 49.0)], maxlen=60
    )
    assert (
        _call_attr(temp_eta_plugin, _member("get_cooldown_ambient_c"), "tool0") is None
    )

    # Cooldown ETA guard clauses.
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_eta_seconds"),
            heater_name="tool0",
            actual_c=float("nan"),
            display_target_c=10.0,
            mode="threshold",
            hysteresis_c=1.0,
        )
        is None
    )

    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_eta_seconds"),
            heater_name="tool0",
            actual_c=10.0,
            display_target_c=10.0,
            mode="threshold",
            hysteresis_c=1.0,
        )
        is None
    )

    # Exponential cooldown: goal <= ambient.
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_exponential_eta"),
            heater_name="tool0",
            ambient_c=25.0,
            goal_c=20.0,
        )
        is None
    )


def test_calculate_cooldown_linear_eta_dt_nonpositive_and_remaining_nonpositive(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate cooldown linear eta dt nonpositive and remaining nonpositive."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 120)
    _set_time(monkeypatch, 100.0)

    # dt <= 0
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(100.0, 60.0), (100.0, 50.0)], maxlen=60
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_linear_eta"),
            "tool0",
            goal_c=40.0,
        )
        is None
    )

    # remaining <= 0
    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [(90.0, 60.0), (100.0, 50.0)], maxlen=60
    )
    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_linear_eta"),
            "tool0",
            goal_c=60.0,
        )
        is None
    )


def test_calculate_cooldown_exponential_eta_invalid_inputs_return_none(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate cooldown exponential eta invalid inputs return none."""
    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["cooldown_fit_window_seconds"], 120)
    _set_time(monkeypatch, 200.0)

    _get_attr(plugin_any, _member("cooldown_history"))["tool0"] = deque(
        [
            (150.0, 80.0),
            (160.0, 65.0),
            (170.0, 54.0),
            (180.0, 46.0),
            (190.0, 40.0),
            (200.0, 35.0),
        ],
        maxlen=60,
    )

    assert (
        _call_attr(
            temp_eta_plugin,
            _member("calculate_cooldown_exponential_eta"),
            heater_name="tool0",
            ambient_c=float("nan"),
            goal_c=25.0,
        )
        is None
    )


def test_on_api_command_reset_profile_history(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    # Avoid requiring Flask in unit tests.
    """Test on api command reset profile history."""
    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)

    plugin_any = cast(Any, temp_eta_plugin)
    _get_attr(plugin_any, _member("settings")).set(["enabled"], True)
    _set_attr(plugin_any, _member("active_profile_id"), "default")

    # Make the command deterministic.
    _set_attr(plugin_any, _member("reset_all_profile_histories"), lambda: 3)
    _set_attr(plugin_any, _member("get_current_profile_id"), lambda: "default")

    resp = temp_eta_plugin.on_api_command("reset_profile_history", {})
    assert resp["success"] is True
    assert resp["deleted_files"] == 3
    assert resp["profile_id"] == "default"


def test_reset_all_profile_histories_handles_enumeration_exception(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test reset all profile histories handles enumeration exception."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)

    # Force folder.mkdir to raise -> outer exception handler.
    def _boom_mkdir(self: Any, *args: Any, **kwargs: Any) -> None:
        """Provide a local test helper callback."""
        raise RuntimeError("boom")

    monkeypatch.setattr(octoprint_temp_eta.Path, "mkdir", _boom_mkdir)

    # Should not raise, should clear UI/history.
    _set_attr(
        plugin_any,
        _member("temp_history"),
        {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)},
    )
    deleted = _call_attr(
        temp_eta_plugin,
        _member("reset_all_profile_histories"),
    )
    assert deleted == 0
    assert not _get_attr(plugin_any, _member("temp_history"))["tool0"]


def test_reset_profile_history_handles_path_resolution_exception(
    temp_eta_plugin: Any,
) -> None:
    """Test reset profile history handles path resolution exception."""
    plugin_any = cast(Any, temp_eta_plugin)
    _set_attr(
        plugin_any,
        _member("temp_history"),
        {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)},
    )

    def _boom(_profile_id: str) -> Any:
        """Provide a local test helper callback."""
        raise RuntimeError("boom")

    _set_attr(plugin_any, _member("get_profile_history_path"), _boom)
    deleted = _call_attr(temp_eta_plugin, _member("reset_profile_history"), "default")
    assert deleted is False
    assert not _get_attr(plugin_any, _member("temp_history"))["tool0"]


def test_calculate_linear_eta_returns_none_with_insufficient_history(
    temp_eta_plugin: Any,
) -> None:
    """Test calculate linear eta returns none with insufficient history."""
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(1.0, 20.0, 200.0)], maxlen=60
    )
    assert (
        _call_attr(temp_eta_plugin, _member("calculate_linear_eta"), "tool0", 200.0)
        is None
    )


def test_calculate_linear_eta_simple(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Linear ETA uses last 10 seconds and returns remaining/rate."""
    # now=100, points at 95 (20C) -> 100 (30C)
    _set_time(monkeypatch, 100.0)
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(95.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60
    )

    eta = _call_attr(temp_eta_plugin, _member("calculate_linear_eta"), "tool0", 50.0)
    assert eta is not None
    assert abs(eta - 10.0) < 1e-6


def test_calculate_linear_eta_edge_cases(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate linear eta edge cases."""
    _set_time(monkeypatch, 100.0)

    # time_diff <= 0
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(100.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60
    )
    assert (
        _call_attr(temp_eta_plugin, _member("calculate_linear_eta"), "tool0", 50.0)
        is None
    )

    # temp_diff <= 0
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(95.0, 30.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )
    assert (
        _call_attr(temp_eta_plugin, _member("calculate_linear_eta"), "tool0", 50.0)
        is None
    )

    # remaining <= 0
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(95.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60
    )
    assert (
        _call_attr(temp_eta_plugin, _member("calculate_linear_eta"), "tool0", 25.0)
        is None
    )


def test_calculate_exponential_eta_falls_back_to_linear_when_not_enough_points(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate exponential eta falls back to linear when not enough points."""
    _set_time(monkeypatch, 30.0)
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(15.0, 20.0, 100.0), (25.0, 30.0, 100.0), (30.0, 40.0, 100.0)], maxlen=60
    )
    # < 6 points in window => exponential falls back to linear, which needs 2 recent points.
    assert (
        _call_attr(
            temp_eta_plugin, _member("calculate_exponential_eta"), "tool0", 100.0
        )
        is not None
    )


def test_calculate_exponential_eta_returns_number_for_reasonable_curve(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
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
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        points, maxlen=60
    )

    eta = _call_attr(
        temp_eta_plugin, _member("calculate_exponential_eta"), "tool0", target
    )
    assert eta is not None
    assert eta > 0


def test_calculate_exponential_eta_returns_zero_when_within_epsilon(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate exponential eta returns zero when within epsilon."""
    target = 100.0
    _set_time(monkeypatch, 100.0)
    # 6+ points, last is within 0.5C of target.
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [
            (70.0, 80.0, target),
            (75.0, 85.0, target),
            (80.0, 90.0, target),
            (85.0, 93.0, target),
            (90.0, 95.0, target),
            (95.0, 99.7, target),
            (100.0, 99.7, target),
        ],
        maxlen=60,
    )
    eta = _call_attr(
        temp_eta_plugin, _member("calculate_exponential_eta"), "tool0", target
    )
    assert eta == 0.0


def test_calculate_exponential_eta_returns_none_when_not_heating(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate exponential eta returns none when not heating."""
    target = 100.0
    _set_time(monkeypatch, 100.0)
    # Temperatures essentially flat -> not heating in window.
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [
            (70.0, 50.0, target),
            (75.0, 50.0, target),
            (80.0, 50.0, target),
            (85.0, 50.0, target),
            (90.0, 50.0, target),
            (95.0, 50.1, target),
            (100.0, 50.1, target),
        ],
        maxlen=60,
    )
    assert (
        _call_attr(
            temp_eta_plugin, _member("calculate_exponential_eta"), "tool0", target
        )
        is None
    )


def test_calculate_exponential_eta_valueerror_falls_back_to_linear(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate exponential eta valueerror falls back to linear."""
    target = 100.0
    _set_time(monkeypatch, 100.0)

    # Data that reaches the final log() call.
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [
            (70.0, 60.0, target),
            (75.0, 65.0, target),
            (80.0, 70.0, target),
            (85.0, 74.0, target),
            (90.0, 78.0, target),
            (95.0, 82.0, target),
            # Use a non-integer remaining/epsilon ratio so it doesn't match any
            # delta values used in the regression logs above.
            (100.0, 85.3, target),
        ],
        maxlen=60,
    )

    # Force ValueError only for the ETA log() call.
    remaining_now = target - 85.3
    ratio_to_fail = remaining_now / 0.5

    # Import calculator module to mock it
    orig_log = calc_module.math.log

    def _fake_log(x: float) -> float:
        """Provide a local test helper callback."""
        if abs(float(x) - float(ratio_to_fail)) < 1e-6:
            raise ValueError("boom")
        return orig_log(x)

    monkeypatch.setattr(calc_module.math, "log", _fake_log)
    monkeypatch.setattr(
        calc_module,
        "calculate_linear_eta",
        lambda history, target, window_seconds=10.0: 123.0,
    )

    assert (
        _call_attr(
            temp_eta_plugin, _member("calculate_exponential_eta"), "tool0", target
        )
        == 123.0
    )


def test_calculate_exponential_eta_spike_protection_returns_linear_eta(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate exponential eta spike protection returns linear eta."""
    target = 100.0
    _set_time(monkeypatch, 100.0)

    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [
            (70.0, 40.0, target),
            (75.0, 50.0, target),
            (80.0, 58.0, target),
            (85.0, 64.0, target),
            (90.0, 69.0, target),
            (95.0, 73.0, target),
            (100.0, 76.0, target),
        ],
        maxlen=60,
    )

    # Force the final comparison to trigger.
    monkeypatch.setattr(
        calc_module,
        "calculate_linear_eta",
        lambda history, target, window_seconds=10.0: 0.1,
    )
    assert (
        _call_attr(
            temp_eta_plugin, _member("calculate_exponential_eta"), "tool0", target
        )
        == 0.1
    )


def test_temperature_callback_records_only_when_target_set_and_far_enough(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test temperature callback records only when target set and far enough."""
    _set_time(monkeypatch, 100.0)
    _set_attr(temp_eta_plugin, _member("temp_history"), {})

    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 90.0, "target": 100.0}}
    )
    assert "tool0" in _get_attr(temp_eta_plugin, _member("temp_history"))
    assert len(_get_attr(temp_eta_plugin, _member("temp_history"))["tool0"]) == 1

    # Remaining < threshold_start -> should not record.
    _set_time(monkeypatch, 101.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 98.0, "target": 100.0}}
    )
    assert len(_get_attr(temp_eta_plugin, _member("temp_history"))["tool0"]) == 1

    # target <= 0 -> should not record.
    _set_time(monkeypatch, 102.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 10.0, "target": 0.0}}
    )
    assert len(_get_attr(temp_eta_plugin, _member("temp_history"))["tool0"]) == 1


def test_temperature_callback_treats_string_target_off_as_cooldown(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test temperature callback treats string target off as cooldown."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["enable_cooldown_eta"], True)
    settings.set(["cooldown_mode"], "threshold")
    settings.set(["cooldown_target_tool0"], 50.0)
    settings.set(["cooldown_hysteresis_c"], 1.0)
    settings.set(["cooldown_fit_window_seconds"], 120)

    _set_time(monkeypatch, 200.0)
    _get_attr(temp_eta_plugin, _member("cooldown_history"))["tool0"].clear()

    # Simulate a firmware/virtual-printer target format that sends a string like "off".
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 200.0, "target": "off"}}
    )
    assert len(_get_attr(temp_eta_plugin, _member("cooldown_history"))["tool0"]) == 1


def test_on_after_startup_registers_callback(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Startup should register the temperature callback on the printer."""
    p_any = cast(Any, temp_eta_plugin)
    printer = cast(DummyPrinter, _get_attr(p_any, _member("printer")))

    # Avoid profile/history IO in this unit test.
    monkeypatch.setattr(
        temp_eta_plugin, "_switch_active_profile_if_needed", lambda *a, **k: None
    )

    temp_eta_plugin.on_after_startup()
    assert temp_eta_plugin in printer.registered_callbacks


def test_broadcast_publishes_to_mqtt_when_configured(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """ETA updates should be published to MQTT when a client is configured."""
    _set_time(monkeypatch, 100.0)

    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )
    _get_attr(temp_eta_plugin, _member("temp_history"))["bed"] = deque(
        [(90.0, 20.0, 60.0), (100.0, 30.0, 60.0)], maxlen=60
    )

    data = {
        "tool0": {"actual": 20.0, "target": 50.0},
        "bed": {"actual": 30.0, "target": 60.0},
        "chamber": {"actual": 30.0, "target": 60.0},
    }

    class RecordingMQTT:
        """Record calls for test assertions."""

        def __init__(self) -> None:
            """Initialize test helper state."""
            self.calls: list[dict[str, Any]] = []

        def publish_eta_update(self, **kwargs: Any) -> None:
            """Provide a test stub implementation."""
            self.calls.append(dict(kwargs))

    mqtt_client = RecordingMQTT()
    _set_attr(temp_eta_plugin, _member("mqtt_client"), mqtt_client)

    _call_attr(temp_eta_plugin, _member("calculate_and_broadcast_eta"), data)

    heaters = {c.get("heater") for c in mqtt_client.calls}
    assert "tool0" in heaters
    assert "bed" in heaters
    assert "chamber" not in heaters


def test_broadcast_mqtt_publish_connection_errors_are_logged(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Connection errors in MQTT publishing should be logged at error level."""
    _set_time(monkeypatch, 100.0)

    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )

    data = {"tool0": {"actual": 20.0, "target": 50.0}}

    class PublishErrorLogger(DummyLogger):
        """Record calls for test assertions."""

        def __init__(self) -> None:
            """Initialize test helper state."""
            self.error_calls: list[str] = []
            self.debug_calls: list[str] = []

        def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
            """Provide a test logger stub method."""
            del kwargs
            self.error_calls.append(msg % args if args else msg)

        def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
            """Provide a test logger stub method."""
            del kwargs
            self.debug_calls.append(msg % args if args else msg)

    class FailingMQTT:
        """Raise errors intentionally for failure-path tests."""

        def publish_eta_update(self, **_kwargs: Any) -> None:
            """Provide a test stub implementation."""
            raise ConnectionError("offline")

    logger = PublishErrorLogger()
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("logger"), logger)
    _set_attr(p_any, _member("mqtt_client"), FailingMQTT())

    _call_attr(temp_eta_plugin, _member("calculate_and_broadcast_eta"), data)

    assert any("MQTT publish failed (connection)" in m for m in logger.error_calls)
    assert not logger.debug_calls


def test_broadcast_mqtt_publish_other_errors_are_logged_debug(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Non-connection errors in MQTT publishing should be logged at debug level."""
    _set_time(monkeypatch, 100.0)

    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )

    data = {"tool0": {"actual": 20.0, "target": 50.0}}

    class BroadcastRecordingLogger(DummyLogger):
        """Record calls for test assertions."""

        def __init__(self) -> None:
            """Initialize test helper state."""
            self.error_calls: list[str] = []
            self.debug_calls: list[str] = []

        def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
            """Provide a test logger stub method."""
            del kwargs
            self.error_calls.append(msg % args if args else msg)

        def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
            """Provide a test logger stub method."""
            del kwargs
            self.debug_calls.append(msg % args if args else msg)

    class FailingMQTT:
        """Raise errors intentionally for failure-path tests."""

        def publish_eta_update(self, **_kwargs: Any) -> None:
            """Provide a test stub implementation."""
            raise RuntimeError("boom")

    logger = BroadcastRecordingLogger()
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("logger"), logger)
    _set_attr(p_any, _member("mqtt_client"), FailingMQTT())

    _call_attr(temp_eta_plugin, _member("calculate_and_broadcast_eta"), data)

    assert not logger.error_calls
    assert any("MQTT publish failed" in m for m in logger.debug_calls)


def test_broadcast_filters_unsupported_heaters(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """ETA updates should only be sent for heaters supported by the active profile."""
    _set_time(monkeypatch, 100.0)
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )
    _get_attr(temp_eta_plugin, _member("temp_history"))["bed"] = deque(
        [(90.0, 20.0, 60.0), (100.0, 30.0, 60.0)], maxlen=60
    )

    data = {
        "tool0": {"actual": 20.0, "target": 50.0},
        "bed": {"actual": 30.0, "target": 60.0},
        "chamber": {"actual": 30.0, "target": 60.0},
    }

    _call_attr(temp_eta_plugin, _member("calculate_and_broadcast_eta"), data)

    pm = cast(DummyPluginManager, _get_attr(temp_eta_plugin, _member("plugin_manager")))
    heaters = [
        m["payload"].get("heater")
        for m in pm.messages
        if m["payload"].get("type") == "eta_update"
    ]
    assert "tool0" in heaters
    assert "bed" in heaters
    assert "chamber" not in heaters


def test_suppress_while_printing_clears_once(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """When suppression is enabled, the plugin clears UI once and stops sending ETAs."""
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("printer"), DummyPrinter(printing=True))
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["suppress_while_printing"], True)

    _set_time(monkeypatch, 100.0)
    _get_attr(temp_eta_plugin, _member("temp_history"))["tool0"] = deque(maxlen=60)
    _get_attr(temp_eta_plugin, _member("temp_history"))["bed"] = deque(maxlen=60)

    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 10.0, "target": 50.0}}
    )

    pm = cast(DummyPluginManager, _get_attr(p_any, _member("plugin_manager")))
    # Should have emitted clear messages for known heaters.
    clears = [m for m in pm.messages if m["payload"].get("eta") is None]
    assert clears

    before = len(pm.messages)
    # Second callback while still printing should not spam additional clears.
    _set_time(monkeypatch, 101.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 12.0, "target": 50.0}}
    )
    assert len(pm.messages) == before


def test_persist_and_restore_profile_history(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Persisted history should be restored on startup (force profile switch)."""
    p1 = TempETAPlugin()
    p1_any = cast(Any, p1)
    _set_attr(p1_any, _member("identifier"), "temp_eta")
    _set_attr(p1_any, _member("plugin_version"), "0.0.0")
    _set_attr(p1_any, _member("logger"), DummyLogger())
    _set_attr(p1_any, _member("plugin_manager"), DummyPluginManager())
    _set_attr(p1_any, _member("printer"), DummyPrinter(printing=False))
    _set_attr(
        p1_any,
        _member("printer_profile_manager"),
        DummyPrinterProfileManager(
            {
                "id": "default",
                "name": "Default",
                "heatedBed": True,
                "heatedChamber": False,
                "extruder": {"count": 1},
            }
        ),
    )
    _set_attr(
        p1_any,
        _member("settings"),
        DummySettings(
            {
                "enabled": True,
                "enable_heating_eta": True,
                "suppress_while_printing": False,
                "threshold_start": 5.0,
                "update_interval": 0.0,
                "algorithm": "linear",
                "history_size": 60,
                "debug_logging": False,
            }
        ),
    )

    _set_plugin_data_folder(p1, tmp_path)
    _set_attr(p1_any, _member("active_profile_id"), "default")

    _set_time(monkeypatch, 100.0)
    _set_attr(
        p1_any,
        _member("temp_history"),
        {"tool0": deque([(95.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60)},
    )
    _set_attr(p1_any, _member("history_dirty"), True)
    _call_attr(p1, _member("persist_current_profile_history"))
    assert (tmp_path / "history_default.json").exists()

    # Restore in a new instance.
    p2 = TempETAPlugin()
    p2_any = cast(Any, p2)
    _set_attr(p2_any, _member("identifier"), "temp_eta")
    _set_attr(p2_any, _member("plugin_version"), "0.0.0")
    _set_attr(p2_any, _member("logger"), DummyLogger())
    _set_attr(p2_any, _member("plugin_manager"), DummyPluginManager())
    _set_attr(p2_any, _member("printer"), DummyPrinter(printing=False))
    _set_attr(
        p2_any,
        _member("printer_profile_manager"),
        _get_attr(p1_any, _member("printer_profile_manager")),
    )
    _set_attr(p2_any, _member("settings"), _get_attr(p1_any, _member("settings")))
    _set_plugin_data_folder(p2, tmp_path)

    _set_time(monkeypatch, 100.0)
    _call_attr(p2, _member("switch_active_profile_if_needed"), force=True)
    p2_history = _get_attr(p2_any, _member("temp_history"))
    assert "tool0" in p2_history
    assert len(p2_history["tool0"]) == 2


def test_reset_all_profile_histories_deletes_files_and_clears_ui(
    temp_eta_plugin: Any, tmp_path: Path
) -> None:
    """Reset should delete all history_*.json and clear frontend state."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    (tmp_path / "history_default.json").write_text("{}", encoding="utf-8")
    (tmp_path / "history_other.json").write_text("{}", encoding="utf-8")

    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque(maxlen=60), "bed": deque(maxlen=60)},
    )
    deleted = _call_attr(
        temp_eta_plugin,
        _member("reset_all_profile_histories"),
    )
    assert deleted == 2

    pm = cast(DummyPluginManager, _get_attr(temp_eta_plugin, _member("plugin_manager")))
    heaters = [
        m["payload"].get("heater")
        for m in pm.messages
        if m["payload"].get("type") == "eta_update"
    ]
    assert set(heaters) == {"tool0", "bed"}


def test_reset_all_profile_histories_handles_delete_failure(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any, tmp_path: Path
) -> None:
    """Test reset all profile histories handles delete failure."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    (tmp_path / "history_default.json").write_text("{}", encoding="utf-8")

    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)},
    )

    def _boom_unlink(self: Path) -> None:
        """Provide a local test helper callback."""
        raise RuntimeError("boom")

    monkeypatch.setattr(Path, "unlink", _boom_unlink)
    deleted = _call_attr(
        temp_eta_plugin,
        _member("reset_all_profile_histories"),
    )
    assert deleted == 0

    pm = cast(DummyPluginManager, _get_attr(temp_eta_plugin, _member("plugin_manager")))
    assert any(
        m["payload"].get("heater") == "tool0" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_on_api_command_reset_settings_defaults(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """API reset should restore defaults and emit a settings_reset message."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["threshold_start"], 42.0)
    settings.set(["debug_logging"], True)

    # Avoid depending on Flask in unit tests.
    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)

    resp = temp_eta_plugin.on_api_command("reset_settings_defaults", {})
    assert resp.get("success") is True
    assert settings.get_float(["threshold_start"]) == 5.0
    assert settings.get_boolean(["debug_logging"]) is False

    pm = cast(DummyPluginManager, _get_attr(p_any, _member("plugin_manager")))
    assert any(m["payload"].get("type") == "settings_reset" for m in pm.messages)


def test_on_api_command_reset_settings_defaults_swallows_send_errors(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test on api command reset settings defaults swallows send errors."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["threshold_start"], 42.0)

    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)

    class _BoomPluginManager(DummyPluginManager):
        """Raise errors intentionally for failure-path tests."""

        def send_plugin_message(self, identifier: str, payload: dict[str, Any]) -> None:
            """Provide a test stub implementation."""
            raise RuntimeError("boom")

    _set_attr(p_any, _member("plugin_manager"), _BoomPluginManager())
    resp = temp_eta_plugin.on_api_command("reset_settings_defaults", {})
    assert resp.get("success") is True


def test_on_settings_save_disabling_plugin_clears_frontend(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Disabling the plugin via settings save should clear all displayed heaters."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["enabled"], True)
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)},
    )

    # Simulate OctoPrint saving settings and setting enabled=False.
    def _fake_save(_self: Any, _data: dict[str, Any]) -> dict[str, Any]:
        """Provide a local test helper callback."""
        settings.set(["enabled"], False)
        return _data

    monkeypatch.setattr(
        octoprint_temp_eta.octoprint.plugin.SettingsPlugin,
        "on_settings_save",
        _fake_save,
    )
    temp_eta_plugin.on_settings_save({"enabled": False})

    pm = cast(DummyPluginManager, _get_attr(p_any, _member("plugin_manager")))
    assert any(
        m["payload"].get("heater") == "tool0" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_debug_log_settings_snapshot_throttles(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Settings snapshot logging should be throttled and safe."""
    _set_attr(temp_eta_plugin, _member("debug_logging_enabled"), True)
    calls: list[str] = []

    def _dbg(msg: str, *_args: Any) -> None:
        """Provide a local test helper."""
        calls.append(msg)

    monkeypatch.setattr(temp_eta_plugin, "_debug_log", _dbg)

    _call_attr(temp_eta_plugin, _member("debug_log_settings_snapshot"), 100.0)
    _call_attr(temp_eta_plugin, _member("debug_log_settings_snapshot"), 120.0)
    assert len(calls) == 1

    # Past the throttle window.
    _call_attr(temp_eta_plugin, _member("debug_log_settings_snapshot"), 200.0)
    assert len(calls) == 2


def test_get_profile_history_path_sanitizes(
    tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Profile ids should be sanitized to a safe filename."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    p = _call_attr(
        temp_eta_plugin, _member("get_profile_history_path"), "weird/..\\profile id"
    )
    assert p.parent == tmp_path
    assert "history_" in p.name
    assert "/" not in p.name
    assert "\\" not in p.name


def test_load_profile_history_filters_old_and_future(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Loader should ignore samples outside the allowed time window."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    _set_attr(temp_eta_plugin, _member("persist_max_age_seconds"), 10.0)

    now = 100.0
    _set_time(monkeypatch, now)

    payload = {
        "version": 1,
        "saved_at": now,
        "profile_id": "default",
        "history_size": 60,
        "samples": {
            "tool0": [
                [50.0, 10.0, 50.0],  # too old
                [95.0, 20.0, 50.0],  # ok
                [106.0, 30.0, 50.0],  # too far in future (> now+5)
                ["bad", 1, 2],  # invalid
            ]
        },
    }
    (tmp_path / "history_default.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )

    loaded = _call_attr(temp_eta_plugin, _member("load_profile_history"), "default")
    assert "tool0" in loaded
    assert list(loaded["tool0"]) == [(95.0, 20.0, 50.0)]


def test_reset_profile_history_deletes_file_and_clears(
    tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Reset profile history should delete file and clear UI."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    (tmp_path / "history_default.json").write_text("{}", encoding="utf-8")
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)},
    )

    deleted = _call_attr(temp_eta_plugin, _member("reset_profile_history"), "default")
    assert deleted is True
    assert not (tmp_path / "history_default.json").exists()

    pm = cast(DummyPluginManager, _get_attr(temp_eta_plugin, _member("plugin_manager")))
    assert any(
        m["payload"].get("heater") == "tool0" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_persist_current_profile_history_early_returns(
    tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test persist current profile history early returns."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    plugin_any = cast(Any, temp_eta_plugin)

    # Missing profile id.
    _set_attr(plugin_any, _member("active_profile_id"), "")
    _set_attr(plugin_any, _member("history_dirty"), True)
    _call_attr(
        temp_eta_plugin,
        _member("persist_current_profile_history"),
    )
    assert not (tmp_path / "history_default.json").exists()

    # Dirty but no samples.
    _set_attr(plugin_any, _member("active_profile_id"), "default")
    _set_attr(plugin_any, _member("history_dirty"), True)
    _set_attr(temp_eta_plugin, _member("temp_history"), {"tool0": deque([], maxlen=60)})
    _call_attr(
        temp_eta_plugin,
        _member("persist_current_profile_history"),
    )
    assert not (tmp_path / "history_default.json").exists()


def test_on_event_disconnect_persists_then_clears(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Disconnect should persist history (best effort) and clear all heaters."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("active_profile_id"), "default")
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque([(95.0, 20.0, 50.0)], maxlen=60)},
    )
    _set_attr(
        temp_eta_plugin,
        _member("cooldown_history"),
        {"tool0": deque([(95.0, 20.0)], maxlen=60)},
    )
    _set_attr(temp_eta_plugin, _member("history_dirty"), True)

    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_event("Disconnected", {})

    assert (tmp_path / "history_default.json").exists()
    assert len(_get_attr(temp_eta_plugin, _member("temp_history"))["tool0"]) == 0
    assert len(_get_attr(temp_eta_plugin, _member("cooldown_history"))["tool0"]) == 0


def test_on_event_error_persists_then_clears(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, temp_eta_plugin: Any
) -> None:
    """Test on event error persists then clears."""
    _set_plugin_data_folder(temp_eta_plugin, tmp_path)
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("active_profile_id"), "default")
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque([(95.0, 20.0, 50.0)], maxlen=60)},
    )
    _set_attr(
        temp_eta_plugin,
        _member("cooldown_history"),
        {"tool0": deque([(95.0, 20.0)], maxlen=60)},
    )
    _set_attr(temp_eta_plugin, _member("history_dirty"), True)

    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_event("Error", {})

    assert (tmp_path / "history_default.json").exists()
    assert len(_get_attr(temp_eta_plugin, _member("temp_history"))["tool0"]) == 0
    assert len(_get_attr(temp_eta_plugin, _member("cooldown_history"))["tool0"]) == 0


def test_on_event_print_started_resets_suppression_flag(temp_eta_plugin: Any) -> None:
    """Test on event print started resets suppression flag."""
    p_any = cast(Any, temp_eta_plugin)
    _set_attr(p_any, _member("suppressing_due_to_print"), True)
    temp_eta_plugin.on_event("PrintStarted", {})
    assert _get_attr(p_any, _member("suppressing_due_to_print")) is False


def test_on_event_shutdown_disconnects_mqtt(temp_eta_plugin: Any) -> None:
    """Shutdown should disconnect the MQTT client when present."""
    p_any = cast(Any, temp_eta_plugin)

    class RecordingMQTT:
        """Record calls for test assertions."""

        def __init__(self) -> None:
            """Initialize test helper state."""
            self.disconnected = False

        def disconnect(self) -> None:
            """Provide a test stub implementation."""
            self.disconnected = True

    mqtt_client = RecordingMQTT()
    _set_attr(p_any, _member("mqtt_client"), mqtt_client)

    temp_eta_plugin.on_event("Shutdown", {})
    assert mqtt_client.disconnected is True


def test_get_update_information_contains_current_version(temp_eta_plugin: Any) -> None:
    """Software update hook should include the current plugin version."""
    _set_attr(temp_eta_plugin, _member("plugin_version"), "0.5.0rc1")
    info = temp_eta_plugin.get_update_information()
    assert "temp_eta" in info
    assert info["temp_eta"]["current"] == "0.5.0rc1"
    assert info["temp_eta"]["repo"] == "OctoPrint-TempETA"


def test_on_api_command_unknown_returns_error(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Unknown API commands should return a structured error."""
    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)
    resp = temp_eta_plugin.on_api_command("nope", {})
    assert resp.get("success") is False


def test_calculate_cooldown_linear_eta_simple(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate cooldown linear eta simple."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["enable_cooldown_eta"], True)
    settings.set(["cooldown_fit_window_seconds"], 120)

    # Cooling: 100C -> 90C over 10s => -1 C/s. Goal 80C => remaining 10C => 10s.
    _set_time(monkeypatch, 10.0)
    _get_attr(temp_eta_plugin, _member("cooldown_history"))["tool0"] = deque(
        [(0.0, 100.0), (10.0, 90.0)], maxlen=60
    )

    eta = _call_attr(
        temp_eta_plugin, _member("calculate_cooldown_linear_eta"), "tool0", 80.0
    )
    assert eta is not None
    assert abs(eta - 10.0) < 1e-6


def test_calculate_cooldown_exponential_eta_returns_number_for_reasonable_curve(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test calculate cooldown exponential eta returns number for reasonable curve."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
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
    _get_attr(temp_eta_plugin, _member("cooldown_history"))["tool0"] = deque(
        points, maxlen=60
    )

    eta = _call_attr(
        temp_eta_plugin,
        _member("calculate_cooldown_exponential_eta"),
        heater_name="tool0",
        ambient_c=ambient,
        goal_c=goal,
    )
    assert eta is not None
    assert eta > 0


def test_broadcast_includes_cooldown_eta_when_target_is_zero(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test broadcast includes cooldown eta when target is zero."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["enable_cooldown_eta"], True)
    settings.set(["cooldown_mode"], "threshold")
    settings.set(["cooldown_target_tool0"], 50.0)
    settings.set(["cooldown_hysteresis_c"], 1.0)
    settings.set(["cooldown_fit_window_seconds"], 120)

    # Provide cooldown history for a falling temperature.
    _set_time(monkeypatch, 10.0)
    _get_attr(temp_eta_plugin, _member("cooldown_history"))["tool0"] = deque(
        [(0.0, 80.0), (10.0, 70.0)], maxlen=60
    )

    pm = cast(DummyPluginManager, _get_attr(temp_eta_plugin, _member("plugin_manager")))

    _call_attr(
        temp_eta_plugin,
        _member("calculate_and_broadcast_eta"),
        {"tool0": {"actual": 70.0, "target": 0.0}},
    )

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
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Test suppress while printing clears once and stops updates."""
    settings = cast(DummySettings, _get_attr(temp_eta_plugin, _member("settings")))
    settings.set(["suppress_while_printing"], True)
    _set_attr(temp_eta_plugin, _member("printer"), DummyPrinter(printing=True))

    # Ensure we don't trigger profile-switch clear noise.
    _set_attr(temp_eta_plugin, _member("active_profile_id"), "default")

    # Pre-populate known heater keys so clear messages are observable.
    _set_attr(
        temp_eta_plugin,
        _member("temp_history"),
        {"tool0": deque([(1.0, 20.0, 200.0), (2.0, 21.0, 200.0)], maxlen=60)},
    )

    pm = cast(DummyPluginManager, _get_attr(temp_eta_plugin, _member("plugin_manager")))

    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 25.0, "target": 200.0}}
    )
    first_count = len(pm.messages)
    assert first_count >= 1
    # Suppression should prevent recording new data.
    assert len(_get_attr(temp_eta_plugin, _member("temp_history"))["tool0"]) == 0

    _set_time(monkeypatch, 101.0)
    temp_eta_plugin.on_printer_add_temperature(
        {"tool0": {"actual": 30.0, "target": 200.0}}
    )
    # No additional clears while suppression remains active.
    assert len(pm.messages) == first_count


def test_broadcast_sends_only_supported_heaters(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """Ensure unsupported heaters (e.g. tool1 when extruder count is 1) are ignored."""
    pm = cast(DummyPluginManager, _get_attr(temp_eta_plugin, _member("plugin_manager")))

    _set_time(monkeypatch, 100.0)
    temp_eta_plugin.on_printer_add_temperature(
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


class _DummyMQTTClient:
    """Minimal MQTT client stub exposing only is_connected() for API tests."""

    def __init__(self, connected: bool) -> None:
        """Initialize test helper state."""
        self._connected = connected

    def is_connected(self) -> bool:
        """Return the canned connection state."""
        return self._connected


@pytest.mark.parametrize(
    ("wrapper_present", "mqtt_enabled", "connected", "expected"),
    [
        # paho-mqtt available, MQTT on and connected to a broker.
        (True, True, True, {"available": True, "enabled": True, "connected": True}),
        # available and enabled, but the broker connection is down.
        (True, True, False, {"available": True, "enabled": True, "connected": False}),
        # available but MQTT disabled in settings: never reports connected.
        (True, False, True, {"available": True, "enabled": False, "connected": False}),
        # paho-mqtt not installed: wrapper absent, client is None.
        (False, True, True, {"available": False, "enabled": True, "connected": False}),
    ],
)
def test_on_api_get_reports_mqtt_status(
    monkeypatch: pytest.MonkeyPatch,
    temp_eta_plugin: Any,
    wrapper_present: bool,
    mqtt_enabled: bool,
    connected: bool,
    expected: dict[str, bool],
) -> None:
    """on_api_get should report MQTT availability/enabled/connected accurately.

    Locks in the response contract the settings UI polls: mqtt_connected is
    only ever True when the wrapper exists, MQTT is enabled, AND the client
    reports a live broker connection.
    """
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["mqtt_enabled"], mqtt_enabled)

    # Avoid depending on Flask in unit tests.
    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)

    if wrapper_present:
        # Sentinel object: on_api_get only checks `MQTTClientWrapper is not None`.
        monkeypatch.setattr(octoprint_temp_eta, "MQTTClientWrapper", object())
        _set_attr(p_any, _member("mqtt_client"), _DummyMQTTClient(connected))
    else:
        # Simulate paho-mqtt being unavailable: wrapper is None, client absent.
        monkeypatch.setattr(octoprint_temp_eta, "MQTTClientWrapper", None)
        _set_attr(p_any, _member("mqtt_client"), None)

    resp = temp_eta_plugin.on_api_get(None)

    assert resp["mqtt_available"] is expected["available"]
    assert resp["mqtt_enabled"] is expected["enabled"]
    assert resp["mqtt_connected"] is expected["connected"]


def test_on_api_get_connected_false_when_client_missing_but_enabled(
    monkeypatch: pytest.MonkeyPatch, temp_eta_plugin: Any
) -> None:
    """A None client (e.g. before startup) must not report a connection."""
    p_any = cast(Any, temp_eta_plugin)
    settings = cast(DummySettings, _get_attr(p_any, _member("settings")))
    settings.set(["mqtt_enabled"], True)

    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)
    monkeypatch.setattr(octoprint_temp_eta, "MQTTClientWrapper", object())
    _set_attr(p_any, _member("mqtt_client"), None)

    resp = temp_eta_plugin.on_api_get(None)

    assert resp["mqtt_available"] is True
    assert resp["mqtt_enabled"] is True
    assert resp["mqtt_connected"] is False
