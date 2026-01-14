"""Unit tests for the Temperature ETA plugin.

These tests follow the guidance in tests/README.md:
- pytest
- mock external dependencies (OctoPrint internals)
- test edge cases
- avoid sleeps (monkeypatch time)
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, cast

import pytest

import octoprint_temp_eta
from octoprint_temp_eta import TempETAPlugin


class DummyLogger:
    def debug(self, *args: Any, **kwargs: Any) -> None:
        return

    def info(self, *args: Any, **kwargs: Any) -> None:
        return

    def warning(self, *args: Any, **kwargs: Any) -> None:
        return


class RecordingLogger(DummyLogger):
    def __init__(self) -> None:
        self.info_calls: List[str] = []

    def info(self, *args: Any, **kwargs: Any) -> None:
        if args:
            self.info_calls.append(str(args[0]))
        return


class WarningRecordingLogger(DummyLogger):
    def __init__(self) -> None:
        self.warning_calls: List[str] = []
        self.debug_calls: List[str] = []

    def warning(self, *args: Any, **kwargs: Any) -> None:
        if args:
            self.warning_calls.append(str(args[0]))
        return

    def debug(self, *args: Any, **kwargs: Any) -> None:
        if args:
            self.debug_calls.append(str(args[0]))
        return


class DebuggableLogger(DummyLogger):
    def __init__(self, enabled: bool = True) -> None:
        self._enabled = bool(enabled)
        self.debug_payloads: List[Any] = []

    def isEnabledFor(self, level: int) -> bool:  # noqa: N802 (OctoPrint/stdlib style)
        return bool(self._enabled)

    def debug(self, *args: Any, **kwargs: Any) -> None:
        self.debug_payloads.append((args, kwargs))
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
    def __init__(
        self,
        printing: bool = False,
        paused: bool = False,
        state_id: str = "OPERATIONAL",
    ) -> None:
        self._printing = printing
        self._paused = paused
        self._state_id = state_id

        self.registered_callbacks: List[Any] = []

    def register_callback(self, callback: Any) -> None:
        self.registered_callbacks.append(callback)

    def is_printing(self) -> bool:
        return bool(self._printing)

    def is_paused(self) -> bool:
        return bool(self._paused)

    def get_state_id(self) -> str:
        return str(self._state_id)


@pytest.fixture()
def plugin() -> TempETAPlugin:
    """Create a plugin instance with mocked OctoPrint dependencies."""
    p = TempETAPlugin()
    p_any = cast(Any, p)
    p_any._identifier = "temp_eta"
    p_any._plugin_version = "0.0.0"
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
            "enable_heating_eta": True,
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


def _set_plugin_data_folder(plugin: TempETAPlugin, folder: Path) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any.get_plugin_data_folder = lambda: str(folder)


def _set_time(monkeypatch: pytest.MonkeyPatch, now: float) -> None:
    monkeypatch.setattr(octoprint_temp_eta.time, "time", lambda: float(now))


def test_settings_defaults_shape(plugin: TempETAPlugin) -> None:
    defaults = plugin.get_settings_defaults()

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
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._debug_logging_enabled = False
    plugin_any._last_settings_snapshot_log_time = 0.0

    called: List[Any] = []
    plugin_any._debug_log = lambda *args, **kwargs: called.append((args, kwargs))

    plugin._debug_log_settings_snapshot(100.0)
    assert called == []
    assert plugin_any._last_settings_snapshot_log_time == 0.0


def test_debug_log_settings_snapshot_logs_and_throttles(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._debug_logging_enabled = True
    plugin_any._last_settings_snapshot_log_time = 0.0

    logged: List[str] = []

    def _capture(msg: str, *args: Any) -> None:
        logged.append(msg)

    plugin_any._debug_log = _capture

    plugin._debug_log_settings_snapshot(100.0)
    assert logged

    # Throttled: within 60s should not log again.
    logged.clear()
    plugin._debug_log_settings_snapshot(120.0)
    assert logged == []


def test_refresh_runtime_caches_applies_valid_settings_and_orders_backoff(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    settings = cast(DummySettings, plugin_any._settings)

    settings.set(["threshold_start"], 7.5)
    settings.set(["update_interval"], 0.5)
    settings.set(["persist_backoff_reset_s"], 5.0)
    settings.set(["persist_backoff_initial_s"], 20.0)
    # Intentionally inverted to exercise ordering correction (max must be >= 10 to be accepted).
    settings.set(["persist_backoff_max_s"], 10.0)
    settings.set(["persist_max_json_bytes"], 20000)

    plugin_any._threshold_start_c = 5.0
    plugin_any._update_interval_s = 1.0
    plugin_any._persist_backoff_current_s = 999.0

    plugin._refresh_runtime_caches()

    assert plugin_any._threshold_start_c == 7.5
    assert plugin_any._update_interval_s == 0.5
    assert plugin_any._persist_backoff_reset_s == 5.0
    assert plugin_any._persist_backoff_initial_s == 20.0
    assert plugin_any._persist_backoff_max_s == 20.0
    assert 1.0 <= float(plugin_any._persist_backoff_current_s) <= 20.0
    assert plugin_any._persist_max_json_bytes == 20000


def test_refresh_runtime_caches_handles_missing_or_broken_settings(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    # Missing settings: should return early.
    plugin_any._settings = None
    plugin._refresh_runtime_caches()

    class _RaisingSettings:
        def get_float(self, _path: List[str]) -> float:
            raise RuntimeError("boom")

        def get_int(self, _path: List[str]) -> int:
            raise RuntimeError("boom")

    plugin_any._settings = _RaisingSettings()

    # Exercise exception paths and the ordering no-op branch.
    plugin_any._persist_backoff_initial_s = 1.0
    plugin_any._persist_backoff_reset_s = 10.0
    plugin._refresh_runtime_caches()


def test_maybe_persist_history_schedules_on_startup_and_backoff_floor(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    called: List[float] = []
    plugin_any._persist_current_profile_history = lambda: called.append(1.0)

    plugin_any._history_dirty = True
    plugin_any._next_persist_time = 0.0
    plugin_any._persist_backoff_current_s = 5.0
    plugin_any._persist_backoff_initial_s = 10.0
    plugin_any._persist_backoff_max_s = 40.0
    plugin_any._persist_phase_active = False

    plugin._maybe_persist_history(100.0)
    assert called == []
    assert plugin_any._next_persist_time == 105.0

    # Not due yet.
    plugin._maybe_persist_history(104.9)
    assert called == []

    # Due: should persist and lift current to at least initial.
    plugin._maybe_persist_history(105.0)
    assert called
    assert plugin_any._persist_backoff_current_s == 10.0
    assert plugin_any._persist_phase_active is True


def test_persist_current_profile_history_emits_size_warning_and_trims(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)
    plugin_any._active_profile_id = "default"

    # Force the size-cap path.
    plugin_any._persist_max_json_bytes = 1024
    plugin_any._last_persist_size_warning_time = 0.0
    plugin_any._logger = WarningRecordingLogger()

    # Lots of points -> large JSON.
    plugin_any._temp_history = {
        "tool0": deque(
            [(float(i), 20.0 + i * 0.01, 200.0) for i in range(500)], maxlen=2000
        )
    }
    plugin_any._history_dirty = True

    _set_time(monkeypatch, 1000.0)
    plugin._persist_current_profile_history()

    assert plugin_any._logger.warning_calls
    # Ensure atomic tmp cleanup happens.
    assert not (tmp_path / "history_default.json.tmp").exists()
    assert (tmp_path / "history_default.json").exists()


def test_persist_current_profile_history_breaks_when_cannot_trim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)
    plugin_any._active_profile_id = "default"

    # Force trimming path even with minimal samples.
    plugin_any._persist_max_json_bytes = 50
    plugin_any._logger = WarningRecordingLogger()

    # Exactly 2 points -> trimming cannot reduce below 2.
    plugin_any._temp_history = {
        "tool0": deque([(1.0, 20.0, 200.0), (2.0, 21.0, 200.0)], maxlen=60)
    }
    plugin_any._history_dirty = True

    _set_time(monkeypatch, 1000.0)
    plugin._persist_current_profile_history()
    assert (tmp_path / "history_default.json").exists()


def test_persist_current_profile_history_cleans_tmp_when_replace_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)
    plugin_any._active_profile_id = "default"
    plugin_any._logger = WarningRecordingLogger()

    plugin_any._temp_history = {
        "tool0": deque(
            [(1.0, 20.0, 200.0), (2.0, 21.0, 200.0), (3.0, 22.0, 200.0)], maxlen=60
        )
    }
    plugin_any._history_dirty = True

    import pathlib

    def _boom_replace(self: pathlib.Path, target: pathlib.Path):
        raise RuntimeError("replace failed")

    monkeypatch.setattr(pathlib.Path, "replace", _boom_replace)

    _set_time(monkeypatch, 1000.0)
    plugin._persist_current_profile_history()
    assert not (tmp_path / "history_default.json.tmp").exists()


def test_persist_current_profile_history_ignores_unlink_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)
    plugin_any._active_profile_id = "default"
    plugin_any._logger = WarningRecordingLogger()

    plugin_any._temp_history = {
        "tool0": deque(
            [(1.0, 20.0, 200.0), (2.0, 21.0, 200.0), (3.0, 22.0, 200.0)], maxlen=60
        )
    }
    plugin_any._history_dirty = True

    import pathlib

    def _boom_replace(self: pathlib.Path, target: pathlib.Path):
        raise RuntimeError("replace failed")

    def _boom_unlink(self: pathlib.Path):
        raise RuntimeError("unlink failed")

    monkeypatch.setattr(pathlib.Path, "replace", _boom_replace)
    monkeypatch.setattr(pathlib.Path, "unlink", _boom_unlink)

    _set_time(monkeypatch, 1000.0)
    plugin._persist_current_profile_history()


def test_on_printer_add_temperature_logs_heater_names_when_debug_enabled(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._logger = DebuggableLogger(enabled=True)
    plugin_any._last_update_time = 0.0
    plugin_any._calculate_and_broadcast_eta = lambda _data: None

    _set_time(monkeypatch, 100.0)
    plugin.on_printer_add_temperature(
        {
            "tool0": {"actual": 20.0, "target": 200.0},
            "bed": {"actual": 30.0, "target": 60.0},
            "junk": "not-a-heater",
        }
    )

    dbg = cast(DebuggableLogger, plugin_any._logger)
    assert dbg.debug_payloads


def test_on_printer_add_temperature_target_change_enters_persist_phase(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)
    plugin_any._calculate_and_broadcast_eta = lambda _data: None

    entered: List[str] = []
    plugin_any._enter_persist_phase = lambda _now, reason: entered.append(str(reason))

    _set_time(monkeypatch, 100.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 20.0, "target": 200.0}})

    _set_time(monkeypatch, 101.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 21.0, "target": 201.0}})

    assert "target_change" in entered


def test_on_printer_add_temperature_uses_idle_debug_interval_when_no_samples_recorded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)
    plugin_any._calculate_and_broadcast_eta = lambda _data: None

    # Make threshold impossible to meet so recorded_count stays 0.
    plugin_any._threshold_start_c = 1000.0
    # Prevent periodic cache refresh from resetting threshold from settings.
    cast(DummySettings, plugin_any._settings).set(["threshold_start"], 1000.0)
    plugin_any._last_runtime_cache_refresh_time = 100.0

    intervals: List[float] = []

    def _capture(now: float, interval: float, *_args: Any, **_kwargs: Any) -> None:
        intervals.append(float(interval))

    plugin_any._debug_log_throttled = _capture

    _set_time(monkeypatch, 100.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 20.0, "target": 30.0}})
    assert intervals
    assert 60.0 in intervals


def test_sanitize_settings_payload_clamps_and_handles_invalid_values(
    plugin: TempETAPlugin,
) -> None:
    data: Dict[str, Any] = {
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

    plugin._sanitize_settings_payload(data)

    assert data["threshold_start"] == 1.0
    assert data["update_interval"] == 0.1
    assert data["history_size"] == 10
    assert data["historical_graph_window_seconds"] == 1800
    assert data["sound_volume"] == 1.0
    assert data["notification_timeout_s"] == 1.0
    assert data["cooldown_hysteresis_c"] == 0.1
    assert data["cooldown_fit_window_seconds"] == 10
    assert data["cooldown_ambient_temp"] is None

    data2: Dict[str, Any] = {"cooldown_ambient_temp": "25"}
    plugin._sanitize_settings_payload(data2)
    assert data2["cooldown_ambient_temp"] == 25.0

    data3: Dict[str, Any] = {"cooldown_ambient_temp": ""}
    plugin._sanitize_settings_payload(data3)
    assert data3["cooldown_ambient_temp"] is None


def test_send_history_reset_message_includes_optional_ids(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    pm: DummyPluginManager = plugin_any._plugin_manager

    plugin._send_history_reset_message(
        "profile_switch", old_profile_id="old", profile_id="new"
    )
    assert pm.messages
    payload = pm.messages[-1]["payload"]
    assert payload["type"] == "history_reset"
    assert payload["reason"] == "profile_switch"
    assert payload["old_profile_id"] == "old"
    assert payload["profile_id"] == "new"


def test_send_history_reset_message_returns_when_plugin_manager_missing(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._plugin_manager = None
    plugin._send_history_reset_message("noop")


def test_clear_all_heaters_frontend_returns_when_plugin_manager_missing(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._plugin_manager = None
    plugin._clear_all_heaters_frontend()


def test_debug_log_settings_snapshot_handles_settings_exception(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    class _RaisingSettings:
        def get_boolean(self, _path: List[str]) -> bool:
            raise RuntimeError("boom")

        def get(self, _path: List[str]) -> Any:
            raise RuntimeError("boom")

    plugin_any._settings = _RaisingSettings()

    plugin_any._debug_logging_enabled = True
    plugin_any._last_settings_snapshot_log_time = 0.0

    logged: List[Any] = []
    plugin_any._debug_log = lambda *args, **kwargs: logged.append((args, kwargs))

    plugin._debug_log_settings_snapshot(100.0)
    assert logged == []
    # Timestamp is updated before reading settings, even if reading fails.
    assert plugin_any._last_settings_snapshot_log_time == 100.0


def test_persist_current_profile_history_trims_to_size_cap_and_writes_atomically(
    plugin: TempETAPlugin,
    tmp_path: Path,
) -> None:
    plugin_any = cast(Any, plugin)

    class _CapturingLogger(DummyLogger):
        def __init__(self) -> None:
            self.warning_calls: List[str] = []

        def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
            self.warning_calls.append(str(msg))

    plugin_any._logger = _CapturingLogger()

    _set_plugin_data_folder(plugin, tmp_path)

    # Force an aggressive cap to exercise trimming logic.
    plugin_any._persist_max_json_bytes = 1500

    # Create lots of samples to exceed the cap.
    with plugin_any._lock:
        plugin_any._temp_history["tool0"] = deque(maxlen=10_000)
        plugin_any._temp_history["bed"] = deque(maxlen=10_000)

        for i in range(600):
            ts = float(i)
            plugin_any._temp_history["tool0"].append((ts, 20.0 + i * 0.1, 200.0))
            plugin_any._temp_history["bed"].append((ts, 30.0 + i * 0.05, 60.0))

    plugin_any._history_dirty = True

    plugin._persist_current_profile_history()

    history_path = tmp_path / "history_default.json"
    assert history_path.exists()
    assert not (tmp_path / "history_default.json.tmp").exists()

    raw = history_path.read_bytes()
    assert len(raw) <= int(plugin_any._persist_max_json_bytes)

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
    plugin: TempETAPlugin,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plugin_any = cast(Any, plugin)

    # Keep callback fast: we only want to exercise phase/backoff code paths.
    plugin_any._calculate_and_broadcast_eta = lambda _data: None

    persisted: List[float] = []

    def _persist_stub() -> None:
        persisted.append(float(octoprint_temp_eta.time.time()))
        plugin_any._history_dirty = False

    plugin_any._persist_current_profile_history = _persist_stub

    # Start at a deterministic time.
    _set_time(monkeypatch, 1000.0)

    # First callback with an active heating phase should enter persist phase and schedule.
    data = {"tool0": {"actual": 20.0, "target": 40.0}}
    plugin.on_printer_add_temperature(data)

    assert plugin_any._persist_phase_active is True
    assert float(plugin_any._persist_backoff_current_s) == float(
        plugin_any._persist_backoff_initial_s
    )
    assert float(plugin_any._next_persist_time) > 1000.0
    assert persisted == []

    # Advance time to the scheduled persist time and call maybe_persist.
    _set_time(monkeypatch, float(plugin_any._next_persist_time))
    plugin_any._history_dirty = True
    plugin._maybe_persist_history(octoprint_temp_eta.time.time())
    assert persisted

    # Backoff doubles after persisting (up to max).
    assert float(plugin_any._persist_backoff_current_s) >= float(
        plugin_any._persist_backoff_initial_s
    )

    # Now simulate leaving the active phase (target off), which should reset backoff.
    _set_time(monkeypatch, 1100.0)
    data = {"tool0": {"actual": 25.0, "target": 0.0}}
    plugin.on_printer_add_temperature(data)
    assert float(plugin_any._persist_backoff_current_s) == float(
        plugin_any._persist_backoff_reset_s
    )


def test_is_print_job_active_returns_false_when_printer_missing(
    plugin: TempETAPlugin,
) -> None:
    p_any = cast(Any, plugin)
    p_any._printer = None
    assert plugin._is_print_job_active() is False


def test_debug_log_throttled_respects_interval(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    p_any._debug_logging_enabled = True
    p_any._last_debug_log_time = -1e9

    calls: List[str] = []
    monkeypatch.setattr(plugin, "_debug_log", lambda msg, *args: calls.append(str(msg)))

    plugin._debug_log_throttled(10.0, 30.0, "hello")
    plugin._debug_log_throttled(20.0, 30.0, "hello")
    plugin._debug_log_throttled(50.0, 30.0, "hello")
    assert calls == ["hello", "hello"]


def test_suppress_while_printing_enabled_defaults_true_without_settings(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings = None
    assert plugin._suppress_while_printing_enabled() is True


def test_suppress_while_printing_enabled_returns_true_on_settings_error(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    class _BadSettings:
        def get_boolean(self, _path: List[str]) -> bool:
            raise RuntimeError("boom")

    plugin_any._settings = _BadSettings()
    assert plugin._suppress_while_printing_enabled() is True


def test_is_print_job_active_returns_false_when_printer_methods_raise(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    class _BadPrinter:
        def is_printing(self) -> bool:
            raise RuntimeError("boom")

        def is_paused(self) -> bool:
            raise RuntimeError("boom")

        def get_state_id(self) -> str:
            raise RuntimeError("boom")

    plugin_any._printer = _BadPrinter()
    assert plugin._is_print_job_active() is False


def test_refresh_debug_logging_flag_handles_settings_error(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    class _BadSettings:
        def get_boolean(self, _path: List[str]) -> bool:
            raise RuntimeError("boom")

    plugin_any._settings = _BadSettings()
    plugin_any._debug_logging_enabled = True
    plugin._refresh_debug_logging_flag()
    assert plugin_any._debug_logging_enabled is False


def test_debug_log_swallows_logger_exceptions(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._debug_logging_enabled = True

    class _BadLogger:
        def info(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("boom")

    plugin_any._logger = _BadLogger()
    plugin._debug_log("hello")


def test_is_print_job_active_checks_paused_and_state_id(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)

    plugin_any._printer = DummyPrinter(printing=False, paused=True)
    assert plugin._is_print_job_active() is True

    plugin_any._printer = DummyPrinter(printing=False, paused=False, state_id="PAUSING")
    assert plugin._is_print_job_active() is True

    plugin_any._printer = DummyPrinter(
        printing=False, paused=False, state_id="OPERATIONAL"
    )
    assert plugin._is_print_job_active() is False


def test_get_current_profile_id_returns_default_on_exception(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    class _BadProfileMgr:
        def get_current_or_default(self) -> Dict[str, Any]:
            raise RuntimeError("boom")

    plugin_any._printer_profile_manager = _BadProfileMgr()
    assert plugin._get_current_profile_id() == "default"


def test_read_history_maxlen_setting_sanitizes(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)

    plugin_any._settings.set(["history_size"], 1)
    assert plugin._read_history_maxlen_setting() == 10

    plugin_any._settings.set(["history_size"], 999)
    assert plugin._read_history_maxlen_setting() == 300

    plugin_any._settings.set(["history_size"], 42)
    assert plugin._read_history_maxlen_setting() == 42


def test_read_history_maxlen_setting_uses_default_on_settings_error(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    default_size = int(plugin_any._default_history_size)

    class _BadSettings:
        def get_int(self, _path: List[str]) -> int:
            raise RuntimeError("boom")

    plugin_any._settings = _BadSettings()
    assert plugin._read_history_maxlen_setting() == default_size


def test_set_history_maxlen_rebuilds_and_marks_dirty(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)

    plugin_any._temp_history["tool0"] = deque(
        [(1.0, 10.0, 50.0), (2.0, 11.0, 50.0), (3.0, 12.0, 50.0)], maxlen=60
    )
    plugin_any._history_dirty = False
    plugin_any._history_maxlen = 60

    plugin._set_history_maxlen(2)
    assert plugin_any._history_maxlen == 2
    assert list(plugin_any._temp_history["tool0"]) == [
        (2.0, 11.0, 50.0),
        (3.0, 12.0, 50.0),
    ]
    assert plugin_any._history_dirty is True


def test_read_history_maxlen_setting_returns_default_without_settings(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    default_size = int(plugin_any._default_history_size)
    plugin_any._settings = None
    assert plugin._read_history_maxlen_setting() == default_size


def test_set_history_maxlen_nonpositive_uses_default(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)
    default_size = int(plugin_any._default_history_size)
    plugin_any._history_maxlen = 60
    plugin_any._temp_history = {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)}

    plugin._set_history_maxlen(0)
    assert plugin_any._history_maxlen == default_size
    assert plugin_any._temp_history["tool0"].maxlen == default_size


def test_is_heater_supported_branches_and_debug_cache(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._debug_logging_enabled = True
    plugin_any._last_heater_support_decision = {}

    # Capture support-change logs (only emitted on transitions).
    logged: List[str] = []
    plugin_any._debug_log = lambda msg, *args: logged.append(str(msg))

    assert plugin._is_heater_supported("bed") is True
    assert plugin._is_heater_supported("chamber") is False
    assert plugin._is_heater_supported("tool0") is True
    assert plugin._is_heater_supported("tool1") is False
    assert plugin._is_heater_supported("toolX") is False
    assert plugin._is_heater_supported("mystery") is False

    # Ensure cache is populated for at least one heater.
    assert "bed" in plugin_any._last_heater_support_decision
    assert logged


def test_is_heater_supported_logs_when_no_profile(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._debug_logging_enabled = True
    plugin_any._last_heater_support_decision = {}

    class _EmptyProfileMgr:
        def get_current_or_default(self) -> Dict[str, Any]:
            return {}

    plugin_any._printer_profile_manager = _EmptyProfileMgr()

    logs: List[str] = []
    plugin_any._debug_log = lambda msg, *args: logs.append(str(msg))

    assert plugin._is_heater_supported("bed") is False
    assert logs


def test_is_heater_supported_logs_on_exception(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._debug_logging_enabled = True
    plugin_any._last_heater_support_decision = {}

    class _BoomProfileMgr:
        def get_current_or_default(self) -> Dict[str, Any]:
            raise RuntimeError("boom")

    plugin_any._printer_profile_manager = _BoomProfileMgr()

    logs: List[str] = []
    plugin_any._debug_log = lambda msg, *args: logs.append(str(msg))

    assert plugin._is_heater_supported("bed") is False
    assert any("Heater support error" in m for m in logs)


def test_switch_active_profile_logs_profile_summary_when_debug_enabled(
    tmp_path: Path, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)

    plugin_any._debug_logging_enabled = True
    plugin_any._active_profile_id = "old"

    messages: List[str] = []
    plugin_any._debug_log = lambda msg, *args: messages.append(str(msg))

    plugin._switch_active_profile_if_needed(force=True)
    assert any("Profile summary" in m for m in messages)


def test_switch_active_profile_logs_profile_summary_unavailable_on_exception(
    tmp_path: Path, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)

    plugin_any._debug_logging_enabled = True
    plugin_any._active_profile_id = "old"

    class _BoomProfileMgr:
        def get_current_or_default(self) -> Dict[str, Any]:
            raise RuntimeError("boom")

    plugin_any._printer_profile_manager = _BoomProfileMgr()

    messages: List[str] = []
    plugin_any._debug_log = lambda msg, *args: messages.append(str(msg))

    plugin._switch_active_profile_if_needed(force=True)
    assert any("Profile summary unavailable" in m for m in messages)


def test_switch_active_profile_non_forced_clears_live_history_and_sends_clear(
    tmp_path: Path, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)

    plugin_any._debug_logging_enabled = True
    plugin_any._active_profile_id = "old"
    plugin_any._history_dirty = False

    # Seed old heaters so we can verify clear messages.
    plugin._temp_history = {
        "tool0": deque([(1.0, 10.0, 50.0)], maxlen=60),
        "bed": deque([(1.0, 10.0, 50.0)], maxlen=60),
    }

    logs: List[str] = []
    plugin_any._debug_log = lambda msg, *args: logs.append(str(msg))

    pm = cast(DummyPluginManager, plugin_any._plugin_manager)
    pm.messages.clear()

    plugin._switch_active_profile_if_needed(force=False)

    assert plugin_any._active_profile_id == "default"
    assert plugin._temp_history == {}
    assert any("Cleared live (RAM) history" in m for m in logs)

    cleared = [
        m["payload"].get("heater")
        for m in pm.messages
        if m["payload"].get("eta") is None
    ]
    assert set(cleared) >= {"tool0", "bed"}


def test_cooldown_mode_defaults_to_threshold_on_invalid(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["cooldown_mode"], "nope")
    assert plugin._cooldown_mode() == "threshold"


def test_cooldown_hysteresis_and_fit_window_clamp(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)

    plugin_any._settings.set(["cooldown_hysteresis_c"], 0)
    assert plugin._cooldown_hysteresis_c() == 1.0

    plugin_any._settings.set(["cooldown_fit_window_seconds"], 5)
    assert plugin._cooldown_fit_window_seconds() == 10.0

    plugin_any._settings.set(["cooldown_fit_window_seconds"], 99999)
    assert plugin._cooldown_fit_window_seconds() == 1800.0


def test_get_cooldown_threshold_target_per_heater(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)

    plugin_any._settings.set(["cooldown_target_tool0"], 55.0)
    plugin_any._settings.set(["cooldown_target_bed"], 44.0)
    plugin_any._settings.set(["cooldown_target_chamber"], 33.0)

    assert plugin._get_cooldown_threshold_target_c("tool0") == 55.0
    assert plugin._get_cooldown_threshold_target_c("bed") == 44.0
    assert plugin._get_cooldown_threshold_target_c("chamber") == 33.0
    assert plugin._get_cooldown_threshold_target_c("unknown") is None


def test_get_cooldown_ambient_c_prefers_user_then_baseline_then_history(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._settings.set(["cooldown_ambient_temp"], 21.0)
    assert plugin._get_cooldown_ambient_c("tool0") == 21.0

    plugin_any._settings.set(["cooldown_ambient_temp"], None)
    plugin_any._cooldown_ambient_baseline["tool0"] = 19.5
    assert plugin._get_cooldown_ambient_c("tool0") == 19.5

    # With no baseline, derive a conservative estimate from history (requires a min notably below current).
    plugin_any._cooldown_ambient_baseline.pop("tool0", None)
    plugin_any._cooldown_history["tool0"] = deque(
        [(90.0, 60.0), (95.0, 40.0), (100.0, 50.0)], maxlen=60
    )
    amb = plugin._get_cooldown_ambient_c("tool0")
    assert amb is not None
    assert abs(amb - 39.5) < 1e-6


def test_get_cooldown_ambient_c_ignores_invalid_user_setting(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    # Invalid ambient setting should be ignored (exception path).
    plugin_any._settings.set(["cooldown_ambient_temp"], "not-a-number")
    plugin_any._cooldown_ambient_baseline.pop("tool0", None)
    plugin_any._cooldown_history.pop("tool0", None)

    assert plugin._get_cooldown_ambient_c("tool0") is None


def test_get_cooldown_display_target_ambient_adds_band(plugin: TempETAPlugin) -> None:
    plugin_any = cast(Any, plugin)

    # Force a known ambient and ensure we add at least a 1°C band.
    plugin_any._get_cooldown_ambient_c = lambda heater: 20.0

    goal = plugin._get_cooldown_display_target_c(
        heater_name="tool0",
        actual_c=50.0,
        mode="ambient",
        hysteresis_c=0.2,
    )
    assert goal == 21.0


def test_calculate_cooldown_linear_eta_paths(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._debug_logging_enabled = True
    _set_time(monkeypatch, 100.0)
    plugin_any._settings.set(["cooldown_fit_window_seconds"], 120)

    # Happy path: negative slope.
    plugin_any._cooldown_history["tool0"] = deque(
        [(90.0, 60.0), (100.0, 50.0)], maxlen=60
    )
    eta = plugin._calculate_cooldown_linear_eta("tool0", goal_c=40.0)
    assert eta is not None
    assert abs(eta - 10.0) < 1e-6

    # Not enough recent samples -> debug log + None.
    logged: List[str] = []
    plugin_any._debug_log = lambda msg, *args: logged.append(str(msg))
    plugin_any._settings.set(["cooldown_fit_window_seconds"], 10)
    plugin_any._cooldown_history["tool0"] = deque([(0.0, 60.0), (1.0, 59.0)], maxlen=60)
    assert plugin._calculate_cooldown_linear_eta("tool0", goal_c=40.0) is None
    assert logged

    # Slope not negative -> debug log + None.
    logged.clear()
    _set_time(monkeypatch, 200.0)
    plugin_any._settings.set(["cooldown_fit_window_seconds"], 120)
    plugin_any._cooldown_history["tool0"] = deque(
        [(90.0, 50.0), (100.0, 55.0)], maxlen=60
    )
    assert plugin._calculate_cooldown_linear_eta("tool0", goal_c=40.0) is None
    assert logged


def test_calculate_cooldown_eta_seconds_ambient_mode_calls_exponential(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["cooldown_ambient_temp"], 20.0)

    called: List[Dict[str, Any]] = []

    def _fake_exp(**kwargs: Any) -> float:
        called.append(dict(kwargs))
        return 123.0

    plugin_any._calculate_cooldown_exponential_eta = _fake_exp
    eta = plugin._calculate_cooldown_eta_seconds(
        heater_name="tool0",
        actual_c=60.0,
        display_target_c=25.0,
        mode="ambient",
        hysteresis_c=1.0,
    )
    assert eta == 123.0
    assert called


def test_reset_user_settings_to_defaults_returns_when_no_settings(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings = None
    plugin._reset_user_settings_to_defaults()


def test_reset_user_settings_to_defaults_applies_runtime_state(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)

    # Make settings differ from defaults.
    plugin_any._settings.set(["enabled"], False)
    plugin_any._settings.set(["history_size"], 10)
    plugin_any._settings.set(["debug_logging"], True)

    # Make runtime state differ too.
    plugin_any._history_maxlen = 10
    plugin_any._temp_history["tool0"] = deque([(1.0, 10.0, 50.0)], maxlen=10)
    plugin_any._debug_logging_enabled = True

    def _raise_save() -> None:
        raise RuntimeError("save failed")

    plugin_any._settings.save = _raise_save

    plugin._reset_user_settings_to_defaults()

    defaults = plugin.get_settings_defaults()
    default_history_size = defaults["history_size"]
    assert default_history_size is not None

    assert plugin_any._settings.get_boolean(["enabled"]) == bool(defaults["enabled"])
    assert plugin_any._settings.get_int(["history_size"]) == int(default_history_size)

    # History size reset should be applied.
    assert plugin_any._history_maxlen == int(default_history_size)
    assert plugin_any._temp_history["tool0"].maxlen == int(default_history_size)


def test_asset_and_api_hooks_shape(plugin: TempETAPlugin) -> None:
    assets = plugin.get_assets()
    assert "js" in assets and "less" in assets

    assert plugin.is_api_protected() is True
    assert plugin.is_api_adminonly() is True

    commands = plugin.get_api_commands()
    assert "reset_profile_history" in commands
    assert "reset_settings_defaults" in commands


def test_template_configs_and_autoescape(plugin: TempETAPlugin) -> None:
    assert plugin.is_template_autoescaped() is True
    cfgs = plugin.get_template_configs()
    assert isinstance(cfgs, list)
    assert {c.get("type") for c in cfgs if isinstance(c, dict)} >= {
        "navbar",
        "sidebar",
        "settings",
        "tab",
    }


def test_settings_helpers_default_and_exception_paths(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)

    # No settings attached: return safe defaults.
    p_any._settings = None
    p_any._debug_logging_enabled = True
    plugin._refresh_debug_logging_flag()
    assert p_any._debug_logging_enabled is False

    assert plugin._suppress_while_printing_enabled() is True
    assert plugin._heating_enabled() is True
    assert plugin._cooldown_enabled() is False
    assert plugin._cooldown_mode() == "threshold"
    assert plugin._cooldown_hysteresis_c() == 1.0
    assert plugin._cooldown_fit_window_seconds() == 120.0

    # Settings present, but getters raise: helpers should fall back to defaults.
    settings = DummySettings({"debug_logging": True})

    def _boom(*_args: Any, **_kwargs: Any) -> Any:
        raise RuntimeError("boom")

    monkeypatch.setattr(settings, "get_boolean", _boom)
    monkeypatch.setattr(settings, "get", _boom)
    monkeypatch.setattr(settings, "get_float", _boom)
    monkeypatch.setattr(settings, "get_int", _boom)

    p_any._settings = settings

    plugin._refresh_debug_logging_flag()
    assert p_any._debug_logging_enabled is False

    assert plugin._suppress_while_printing_enabled() is True
    assert plugin._heating_enabled() is True
    assert plugin._cooldown_enabled() is False
    assert plugin._cooldown_mode() == "threshold"
    assert plugin._cooldown_hysteresis_c() == 1.0
    assert plugin._cooldown_fit_window_seconds() == 120.0


def test_load_profile_history_invalid_json_and_shape(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: TempETAPlugin
) -> None:
    _set_plugin_data_folder(plugin, tmp_path)
    plugin._persist_max_age_seconds = 10.0
    _set_time(monkeypatch, 100.0)

    # Invalid JSON should be handled.
    (tmp_path / "history_default.json").write_text("{not json", encoding="utf-8")
    assert plugin._load_profile_history("default") == {}

    # Wrong top-level shape should be ignored.
    (tmp_path / "history_default.json").write_text(
        json.dumps([1, 2, 3]), encoding="utf-8"
    )
    assert plugin._load_profile_history("default") == {}

    # samples not a dict -> ignored.
    (tmp_path / "history_default.json").write_text(
        json.dumps({"samples": [1, 2, 3]}), encoding="utf-8"
    )
    assert plugin._load_profile_history("default") == {}


def test_load_profile_history_skips_invalid_heater_and_point_shapes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: TempETAPlugin
) -> None:
    _set_plugin_data_folder(plugin, tmp_path)
    plugin._persist_max_age_seconds = 10.0
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
    assert plugin._load_profile_history("default") == {}


def test_on_settings_save_toggles_debug_updates_history_and_handles_non_dict_saved(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)

    logger = RecordingLogger()
    p_any._logger = logger

    settings.set(["enabled"], True)
    settings.set(["debug_logging"], False)
    settings.set(["history_size"], 60)
    p_any._debug_logging_enabled = False

    p_any._history_maxlen = 60
    plugin._temp_history = {
        "tool0": deque([(1.0, 10.0, 50.0)], maxlen=60),
        "bed": deque([(1.0, 10.0, 50.0)], maxlen=60),
    }

    def _fake_save(_self: Any, _data: Dict[str, Any]) -> str:
        settings.set(["enabled"], False)
        settings.set(["debug_logging"], True)
        settings.set(["history_size"], 50)
        return "ok"

    monkeypatch.setattr(
        octoprint_temp_eta.octoprint.plugin.SettingsPlugin,
        "on_settings_save",
        _fake_save,
    )
    result = plugin.on_settings_save({"enabled": False})

    assert result == {}
    assert any("Debug logging" in msg for msg in logger.info_calls)
    assert p_any._history_maxlen == 50
    assert plugin._temp_history["tool0"].maxlen == 50

    pm = cast(DummyPluginManager, p_any._plugin_manager)
    assert any(
        m["payload"].get("type") == "eta_update" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_on_settings_save_sanitizes_numeric_payload_before_delegating(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)

    captured: Dict[str, Any] = {}

    def _fake_save(_self: Any, data: Dict[str, Any]) -> Dict[str, Any]:
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

    plugin.on_settings_save(
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
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Saving settings should reconfigure the MQTT client when present."""
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)

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
        def __init__(self) -> None:
            self.configured: Dict[str, Any] = {}

        def configure(self, cfg: Dict[str, Any]) -> None:
            self.configured = dict(cfg)

    mqtt_client = RecordingMQTT()
    p_any._mqtt_client = mqtt_client

    monkeypatch.setattr(
        octoprint_temp_eta.octoprint.plugin.SettingsPlugin,
        "on_settings_save",
        lambda _self, _data: {},
    )
    plugin.on_settings_save({"mqtt_enabled": True})

    assert mqtt_client.configured.get("mqtt_enabled") is True
    assert mqtt_client.configured.get("mqtt_broker_host") == "broker"
    assert mqtt_client.configured.get("mqtt_broker_port") == 1883


def test_on_printer_add_temperature_records_sample_and_triggers_update(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["threshold_start"], 5.0)
    plugin_any._settings.set(["update_interval"], 0.0)
    plugin_any._settings.set(["enable_heating_eta"], True)

    calls: List[Any] = []
    plugin_any._calculate_and_broadcast_eta = lambda data: calls.append(data)
    plugin_any._maybe_persist_history = lambda now: None

    plugin.on_printer_add_temperature({"tool0": {"actual": 20.0, "target": 40.0}})

    assert calls
    assert "tool0" in plugin_any._temp_history
    assert len(plugin_any._temp_history["tool0"]) == 1
    assert plugin_any._history_dirty is True


def test_on_printer_add_temperature_suppresses_while_printing_and_clears_once(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["suppress_while_printing"], True)
    plugin_any._settings.set(["update_interval"], 0.0)

    plugin_any._printer = DummyPrinter(printing=True)
    plugin_any._suppressing_due_to_print = False

    # Seed some state so clear messages are sent.
    plugin._temp_history = {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)}

    plugin_any._calculate_and_broadcast_eta = lambda _data: (_ for _ in ()).throw(
        AssertionError("should not compute while suppressed")
    )

    pm = cast(DummyPluginManager, plugin_any._plugin_manager)
    before = len(pm.messages)
    plugin.on_printer_add_temperature({"tool0": {"actual": 20.0, "target": 40.0}})
    after_first = len(pm.messages)

    assert plugin_any._suppressing_due_to_print is True
    assert after_first > before

    # Second call: still suppressed, should not clear again.
    plugin.on_printer_add_temperature({"tool0": {"actual": 21.0, "target": 41.0}})
    assert len(pm.messages) == after_first


def test_on_printer_add_temperature_unsuppresses_when_job_not_active(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["suppress_while_printing"], True)
    plugin_any._settings.set(["threshold_start"], 5.0)
    plugin_any._settings.set(["update_interval"], 0.0)
    plugin_any._settings.set(["enable_heating_eta"], True)

    # Not printing anymore.
    plugin_any._printer = DummyPrinter(printing=False)
    plugin_any._suppressing_due_to_print = True

    called: List[Any] = []
    plugin_any._calculate_and_broadcast_eta = lambda data: called.append(data)
    plugin_any._maybe_persist_history = lambda now: None

    plugin.on_printer_add_temperature({"tool0": {"actual": 20.0, "target": 40.0}})
    assert plugin_any._suppressing_due_to_print is False
    assert called


def test_on_printer_add_temperature_updates_ambient_baseline_when_lower(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["update_interval"], 999.0)

    plugin_any._cooldown_ambient_baseline["tool0"] = 100.0
    plugin.on_printer_add_temperature({"tool0": {"actual": 90.0, "target": 0}})
    assert plugin_any._cooldown_ambient_baseline.get("tool0") == 90.0


def test_on_printer_add_temperature_skips_when_holding_or_below_threshold(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._temp_history = {}
    plugin_any._history_dirty = False

    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["threshold_start"], 5.0)
    plugin_any._settings.set(["update_interval"], 0.0)
    plugin_any._settings.set(["enable_heating_eta"], True)

    calls: List[Any] = []
    plugin_any._calculate_and_broadcast_eta = lambda data: calls.append(data)
    plugin_any._maybe_persist_history = lambda now: None

    # remaining <= epsilon_hold (0.2) => no history record.
    plugin.on_printer_add_temperature({"tool0": {"actual": 39.9, "target": 40.0}})
    assert calls
    assert (
        "tool0" not in plugin_any._temp_history
        or len(plugin_any._temp_history["tool0"]) == 0
    )
    assert plugin_any._history_dirty is False

    calls.clear()
    # remaining < threshold => no history record.
    plugin.on_printer_add_temperature({"tool0": {"actual": 37.0, "target": 40.0}})
    assert calls
    assert (
        "tool0" not in plugin_any._temp_history
        or len(plugin_any._temp_history["tool0"]) == 0
    )
    assert plugin_any._history_dirty is False


def test_on_printer_add_temperature_non_numeric_target_tracks_cooldown_and_baseline(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["update_interval"], 0.0)

    # Pretend we were heating before, so we take the "cooldown start" path.
    plugin_any._last_target_by_heater["tool0"] = 200.0

    debug_calls: List[Any] = []
    plugin_any._debug_log_throttled = lambda *args, **kwargs: debug_calls.append(
        (args, kwargs)
    )

    plugin_any._calculate_and_broadcast_eta = lambda data: None
    plugin_any._maybe_persist_history = lambda now: None

    plugin.on_printer_add_temperature({"tool0": {"actual": 100.0, "target": "off"}})

    assert debug_calls  # should log non-numeric target / cooldown start
    assert "tool0" in plugin_any._cooldown_history
    assert len(plugin_any._cooldown_history["tool0"]) == 1
    assert plugin_any._cooldown_ambient_baseline.get("tool0") == 100.0


def test_on_printer_add_temperature_skips_invalid_actual_values_and_creates_cooldown_history(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_time(monkeypatch, 100.0)

    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["update_interval"], 999.0)

    # Ensure debug path is active so coverage records the non-numeric target handler.
    plugin_any._debug_logging_enabled = True
    plugin_any._last_debug_log_time = 0.0

    plugin_any._calculate_and_broadcast_eta = lambda data: None
    plugin_any._maybe_persist_history = lambda now: None

    plugin.on_printer_add_temperature(
        {
            "tool0": {"actual": None, "target": 0},
            "tool1": {"actual": "abc", "target": 0},
            "tool2": {"actual": 100.0, "target": "off"},
        }
    )

    assert "tool2" in plugin_any._cooldown_history
    assert len(plugin_any._cooldown_history["tool2"]) == 1
    # Baseline should be learned when previously unset.
    assert plugin_any._cooldown_ambient_baseline.get("tool2") == 100.0


def test_printer_callback_stubs_do_not_crash(plugin: TempETAPlugin) -> None:
    plugin.on_printer_send_current_data({"state": "ok"})
    plugin.on_printer_add_log({"line": "hello"})


def test_on_printer_add_temperature_respects_update_interval(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enabled"], True)
    plugin_any._settings.set(["threshold_start"], 5.0)
    plugin_any._settings.set(["update_interval"], 10.0)
    plugin_any._settings.set(["enable_heating_eta"], True)

    called: List[Any] = []
    plugin_any._calculate_and_broadcast_eta = lambda data: called.append(data)
    plugin_any._maybe_persist_history = lambda now: None

    # First call triggers (last_update_time starts at 0).
    _set_time(monkeypatch, 100.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 20.0, "target": 40.0}})
    assert called

    called.clear()
    # Second call within interval should NOT trigger.
    _set_time(monkeypatch, 105.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 21.0, "target": 40.0}})
    assert called == []


def test_calculate_and_broadcast_eta_skips_non_dict_and_unsupported(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)

    plugin_any._plugin_manager.messages.clear()

    def _supported(heater: str) -> bool:
        return heater == "bed"

    plugin_any._is_heater_supported = _supported

    plugin._calculate_and_broadcast_eta(
        {
            "time": 123,
            "tool0": {"actual": 20.0, "target": 40.0},
            "bed": {"actual": 20.0, "target": 40.0},
        }
    )

    pm = cast(DummyPluginManager, plugin_any._plugin_manager)
    assert pm.messages
    last = pm.messages[-1]["payload"]
    assert last["heater"] == "bed"


def test_calculate_and_broadcast_eta_auto_creates_history_for_new_heater(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._plugin_manager.messages.clear()

    # Force support for tool1 and ensure it's not already tracked.
    plugin_any._is_heater_supported = lambda heater: heater == "tool1"
    plugin._temp_history.pop("tool1", None)

    plugin._calculate_and_broadcast_eta({"tool1": {"actual": 20.0, "target": 40.0}})
    assert "tool1" in plugin._temp_history


def test_calculate_and_broadcast_eta_cooldown_threshold_skips_when_below_hysteresis(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["cooldown_mode"], "threshold")
    plugin_any._settings.set(["cooldown_hysteresis_c"], 1.0)
    plugin_any._settings.set(["cooldown_target_tool0"], 50.0)

    # If called, the test should fail.
    plugin_any._calculate_cooldown_eta_seconds = lambda *args, **kwargs: (
        _ for _ in ()
    ).throw(AssertionError("should not compute cooldown eta"))

    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta(
        {
            "tool0": {"actual": 50.5, "target": 0},
        }
    )

    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["cooldown_mode"] == "threshold"
    assert msg["cooldown_target"] == 50.0


def test_calculate_and_broadcast_eta_cooldown_ambient_computes_and_sends_kind(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["cooldown_mode"], "ambient")
    plugin_any._settings.set(["cooldown_hysteresis_c"], 2.0)
    plugin_any._settings.set(["cooldown_ambient_temp"], 20.0)

    plugin_any._calculate_cooldown_eta_seconds = lambda *args, **kwargs: 5.0

    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta(
        {
            "tool0": {"actual": 30.0, "target": 0},
        }
    )

    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] == 5.0
    assert msg["eta_kind"] == "cooling"
    assert msg["cooldown_mode"] == "ambient"
    assert msg["cooldown_target"] == 22.0


def test_calculate_and_broadcast_eta_cooldown_threshold_under_one_second_logs_insufficient_fit(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["cooldown_mode"], "threshold")
    plugin_any._settings.set(["cooldown_hysteresis_c"], 1.0)
    plugin_any._settings.set(["cooldown_target_tool0"], 40.0)

    debug_calls: List[Any] = []
    plugin_any._debug_log_throttled = lambda *args, **kwargs: debug_calls.append(
        (args, kwargs)
    )

    plugin_any._calculate_cooldown_eta_seconds = lambda *args, **kwargs: 0.5
    plugin_any._plugin_manager.messages.clear()

    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 45.5, "target": 0}})

    assert any("insufficient fit" in str(args[2]) for (args, _kwargs) in debug_calls)
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None


def test_calculate_and_broadcast_eta_cooldown_target_none_triggers_debug_log(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["cooldown_mode"], "ambient")
    plugin_any._settings.set(["cooldown_ambient_temp"], None)

    calls: List[Any] = []
    plugin_any._debug_log_throttled = lambda *args, **kwargs: calls.append(
        (args, kwargs)
    )

    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta(
        {
            "tool0": {"actual": 30.0, "target": 0},
        }
    )

    assert calls
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["cooldown_target"] is None


def test_calculate_and_broadcast_eta_cooldown_eta_under_one_second_logs_insufficient_fit(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["cooldown_mode"], "ambient")
    plugin_any._settings.set(["cooldown_hysteresis_c"], 1.0)
    plugin_any._settings.set(["cooldown_ambient_temp"], 20.0)

    debug_calls: List[Any] = []
    plugin_any._debug_log_throttled = lambda *args, **kwargs: debug_calls.append(
        (args, kwargs)
    )

    # Force compute, but return <1s so it is hidden.
    plugin_any._calculate_cooldown_eta_seconds = lambda *args, **kwargs: 0.5
    plugin_any._cooldown_history["tool0"] = deque([(90.0, 60.0)], maxlen=60)

    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 30.0, "target": 0}})

    assert any("insufficient fit" in str(args[2]) for (args, _kwargs) in debug_calls)
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None


def test_calculate_and_broadcast_eta_cooldown_forced_target_under_one_second_hits_branches(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["cooldown_mode"], "ambient")
    plugin_any._settings.set(["cooldown_hysteresis_c"], 1.0)

    debug_calls: List[Any] = []
    plugin_any._debug_log_throttled = lambda *args, **kwargs: debug_calls.append(
        (args, kwargs)
    )

    monkeypatch.setattr(plugin, "_get_cooldown_display_target_c", lambda **_kw: 40.0)
    monkeypatch.setattr(plugin, "_calculate_cooldown_eta_seconds", lambda **_kw: 0.5)

    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 60.0, "target": 0}})

    assert any("insufficient fit" in str(args[2]) for (args, _kwargs) in debug_calls)
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["cooldown_target"] == 40.0


def test_calculate_and_broadcast_eta_heating_exponential_and_hide_under_one_second(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_heating_eta"], True)
    plugin_any._settings.set(["threshold_start"], 5.0)
    plugin_any._settings.set(["algorithm"], "exponential")

    plugin_any._plugin_manager.messages.clear()
    plugin_any._calculate_exponential_eta = lambda heater, target: 0.5
    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 20.0, "target": 40.0}})

    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None
    assert msg["eta_kind"] is None

    plugin_any._plugin_manager.messages.clear()
    plugin_any._calculate_exponential_eta = lambda heater, target: 10.0
    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 20.0, "target": 40.0}})
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["eta"] == 10.0
    assert msg["eta_kind"] == "heating"


def test_calculate_and_broadcast_eta_handles_non_numeric_values_and_close_to_target(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_heating_eta"], True)
    plugin_any._settings.set(["threshold_start"], 5.0)
    plugin_any._settings.set(["algorithm"], "linear")

    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta({"tool0": {"actual": "bad", "target": "bad"}})
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["heater"] == "tool0"
    assert msg["eta"] is None

    # Very close to target (below threshold) -> eta cleared.
    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 39.0, "target": 40.0}})
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["eta"] is None
    assert msg["eta_kind"] is None


def test_calculate_and_broadcast_eta_cooldown_insufficient_fit_logs_history_len(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enable_cooldown_eta"], True)
    plugin_any._settings.set(["cooldown_mode"], "threshold")
    plugin_any._settings.set(["cooldown_hysteresis_c"], 1.0)
    plugin_any._settings.set(["cooldown_target_tool0"], 50.0)

    # Ensure there is some history so hist_len path is meaningful.
    plugin_any._cooldown_history["tool0"] = deque([(0.0, 70.0)], maxlen=60)

    debug: List[str] = []
    plugin_any._debug_log_throttled = (
        lambda now, interval, message, *args: debug.append(str(message))
    )

    plugin_any._calculate_cooldown_eta_seconds = lambda *args, **kwargs: None

    plugin_any._plugin_manager.messages.clear()
    plugin._calculate_and_broadcast_eta({"tool0": {"actual": 70.0, "target": 0}})

    assert any("insufficient fit" in m for m in debug)
    msg = plugin_any._plugin_manager.messages[-1]["payload"]
    assert msg["eta"] is None
    assert msg["cooldown_target"] == 50.0


def test_calculate_exponential_eta_happy_path_returns_number(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    target = 200.0
    _set_time(monkeypatch, 100.0)

    # Smooth heating curve approaching target (remaining decreases).
    plugin._temp_history["tool0"] = deque(
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

    eta = plugin._calculate_exponential_eta("tool0", target)
    assert eta is not None
    assert float(eta) >= 0.0


def test_calculate_cooldown_exponential_eta_happy_path(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["cooldown_fit_window_seconds"], 120)
    _set_time(monkeypatch, 200.0)

    # Construct an exponential-ish cooldown curve with 6 points.
    plugin_any._cooldown_history["tool0"] = deque(
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

    eta = plugin._calculate_cooldown_exponential_eta(
        heater_name="tool0", ambient_c=20.0, goal_c=25.0
    )
    assert eta is not None
    assert float(eta) > 0.0


def test_cooldown_helpers_early_return_paths(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)

    # Threshold target validation.
    plugin_any._settings.set(["cooldown_target_tool0"], "")
    assert plugin._get_cooldown_threshold_target_c("tool0") is None

    plugin_any._settings.set(["cooldown_target_tool0"], -5)
    assert plugin._get_cooldown_threshold_target_c("tool0") is None

    plugin_any._settings.set(["cooldown_target_tool0"], "nan")
    assert plugin._get_cooldown_threshold_target_c("tool0") is None

    # Ambient helper: invalid user ambient -> fall back; no baseline/history -> None.
    plugin_any._settings.set(["cooldown_ambient_temp"], -100)
    plugin_any._cooldown_ambient_baseline.pop("tool0", None)
    plugin_any._cooldown_history.pop("tool0", None)
    assert plugin._get_cooldown_ambient_c("tool0") is None

    # Ambient helper: history too short (<3 recent points).
    _set_time(monkeypatch, 100.0)
    plugin_any._settings.set(["cooldown_ambient_temp"], None)
    plugin_any._settings.set(["cooldown_fit_window_seconds"], 120)
    plugin_any._cooldown_history["tool0"] = deque(
        [(90.0, 30.0), (95.0, 29.0)], maxlen=60
    )
    assert plugin._get_cooldown_ambient_c("tool0") is None

    # Ambient helper: minimum is too close to current -> None.
    plugin_any._cooldown_history["tool0"] = deque(
        [(90.0, 50.0), (95.0, 49.5), (100.0, 49.0)], maxlen=60
    )
    assert plugin._get_cooldown_ambient_c("tool0") is None

    # Cooldown ETA guard clauses.
    assert (
        plugin._calculate_cooldown_eta_seconds(
            heater_name="tool0",
            actual_c=float("nan"),
            display_target_c=10.0,
            mode="threshold",
            hysteresis_c=1.0,
        )
        is None
    )

    assert (
        plugin._calculate_cooldown_eta_seconds(
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
        plugin._calculate_cooldown_exponential_eta(
            heater_name="tool0", ambient_c=25.0, goal_c=20.0
        )
        is None
    )


def test_calculate_cooldown_linear_eta_dt_nonpositive_and_remaining_nonpositive(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["cooldown_fit_window_seconds"], 120)
    _set_time(monkeypatch, 100.0)

    # dt <= 0
    plugin_any._cooldown_history["tool0"] = deque(
        [(100.0, 60.0), (100.0, 50.0)], maxlen=60
    )
    assert plugin._calculate_cooldown_linear_eta("tool0", goal_c=40.0) is None

    # remaining <= 0
    plugin_any._cooldown_history["tool0"] = deque(
        [(90.0, 60.0), (100.0, 50.0)], maxlen=60
    )
    assert plugin._calculate_cooldown_linear_eta("tool0", goal_c=60.0) is None


def test_calculate_cooldown_exponential_eta_invalid_inputs_return_none(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["cooldown_fit_window_seconds"], 120)
    _set_time(monkeypatch, 200.0)

    plugin_any._cooldown_history["tool0"] = deque(
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
        plugin._calculate_cooldown_exponential_eta(
            heater_name="tool0", ambient_c=float("nan"), goal_c=25.0
        )
        is None
    )


def test_on_api_command_reset_profile_history(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    # Avoid requiring Flask in unit tests.
    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)

    plugin_any = cast(Any, plugin)
    plugin_any._settings.set(["enabled"], True)
    plugin_any._active_profile_id = "default"

    # Make the command deterministic.
    plugin_any._reset_all_profile_histories = lambda: 3
    plugin_any._get_current_profile_id = lambda: "default"

    resp = plugin.on_api_command("reset_profile_history", {})
    assert resp["success"] is True
    assert resp["deleted_files"] == 3
    assert resp["profile_id"] == "default"


def test_reset_all_profile_histories_handles_enumeration_exception(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    _set_plugin_data_folder(plugin, tmp_path)

    # Force folder.mkdir to raise -> outer exception handler.
    def _boom_mkdir(self: Any, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(octoprint_temp_eta.Path, "mkdir", _boom_mkdir)

    # Should not raise, should clear UI/history.
    plugin_any._temp_history = {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)}
    deleted = plugin._reset_all_profile_histories()
    assert deleted == 0
    assert list(plugin_any._temp_history["tool0"]) == []


def test_reset_profile_history_handles_path_resolution_exception(
    plugin: TempETAPlugin,
) -> None:
    plugin_any = cast(Any, plugin)
    plugin_any._temp_history = {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)}

    def _boom(_profile_id: str) -> Any:
        raise RuntimeError("boom")

    plugin_any._get_profile_history_path = _boom
    deleted = plugin._reset_profile_history("default")
    assert deleted is False
    assert list(plugin_any._temp_history["tool0"]) == []


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


def test_calculate_linear_eta_edge_cases(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    _set_time(monkeypatch, 100.0)

    # time_diff <= 0
    plugin._temp_history["tool0"] = deque(
        [(100.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60
    )
    assert plugin._calculate_linear_eta("tool0", 50.0) is None

    # temp_diff <= 0
    plugin._temp_history["tool0"] = deque(
        [(95.0, 30.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )
    assert plugin._calculate_linear_eta("tool0", 50.0) is None

    # remaining <= 0
    plugin._temp_history["tool0"] = deque(
        [(95.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60
    )
    assert plugin._calculate_linear_eta("tool0", 25.0) is None


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


def test_calculate_exponential_eta_returns_zero_when_within_epsilon(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    target = 100.0
    _set_time(monkeypatch, 100.0)
    # 6+ points, last is within 0.5C of target.
    plugin._temp_history["tool0"] = deque(
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
    eta = plugin._calculate_exponential_eta("tool0", target)
    assert eta == 0.0


def test_calculate_exponential_eta_returns_none_when_not_heating(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    target = 100.0
    _set_time(monkeypatch, 100.0)
    # Temperatures essentially flat -> not heating in window.
    plugin._temp_history["tool0"] = deque(
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
    assert plugin._calculate_exponential_eta("tool0", target) is None


def test_calculate_exponential_eta_valueerror_falls_back_to_linear(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    target = 100.0
    _set_time(monkeypatch, 100.0)

    # Data that reaches the final log() call.
    plugin._temp_history["tool0"] = deque(
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
    orig_log = octoprint_temp_eta.math.log

    def _fake_log(x: float) -> float:
        if abs(float(x) - float(ratio_to_fail)) < 1e-6:
            raise ValueError("boom")
        return orig_log(x)

    monkeypatch.setattr(octoprint_temp_eta.math, "log", _fake_log)
    plugin_any._calculate_linear_eta = lambda heater, target: 123.0

    assert plugin._calculate_exponential_eta("tool0", target) == 123.0


def test_calculate_exponential_eta_spike_protection_returns_linear_eta(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    plugin_any = cast(Any, plugin)
    target = 100.0
    _set_time(monkeypatch, 100.0)

    plugin._temp_history["tool0"] = deque(
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
    plugin_any._calculate_linear_eta = lambda heater, target: 0.1
    assert plugin._calculate_exponential_eta("tool0", target) == 0.1


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


def test_on_after_startup_registers_callback(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Startup should register the temperature callback on the printer."""
    p_any = cast(Any, plugin)
    printer = cast(DummyPrinter, p_any._printer)

    # Avoid profile/history IO in this unit test.
    monkeypatch.setattr(
        plugin, "_switch_active_profile_if_needed", lambda *a, **k: None
    )

    plugin.on_after_startup()
    assert plugin in printer.registered_callbacks


def test_broadcast_publishes_to_mqtt_when_configured(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """ETA updates should be published to MQTT when a client is configured."""
    _set_time(monkeypatch, 100.0)

    plugin._temp_history["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )
    plugin._temp_history["bed"] = deque(
        [(90.0, 20.0, 60.0), (100.0, 30.0, 60.0)], maxlen=60
    )

    data = {
        "tool0": {"actual": 20.0, "target": 50.0},
        "bed": {"actual": 30.0, "target": 60.0},
        "chamber": {"actual": 30.0, "target": 60.0},
    }

    class RecordingMQTT:
        def __init__(self) -> None:
            self.calls: List[Dict[str, Any]] = []

        def publish_eta_update(self, **kwargs: Any) -> None:
            self.calls.append(dict(kwargs))

    mqtt_client = RecordingMQTT()
    cast(Any, plugin)._mqtt_client = mqtt_client

    plugin._calculate_and_broadcast_eta(data)

    heaters = {c.get("heater") for c in mqtt_client.calls}
    assert "tool0" in heaters
    assert "bed" in heaters
    assert "chamber" not in heaters


def test_broadcast_mqtt_publish_connection_errors_are_logged(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Connection errors in MQTT publishing should be logged at error level."""
    _set_time(monkeypatch, 100.0)

    plugin._temp_history["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )

    data = {"tool0": {"actual": 20.0, "target": 50.0}}

    class RecordingLogger(DummyLogger):
        def __init__(self) -> None:
            self.error_calls: List[str] = []
            self.debug_calls: List[str] = []

        def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
            self.error_calls.append(msg % args if args else msg)

        def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
            self.debug_calls.append(msg % args if args else msg)

    class FailingMQTT:
        def publish_eta_update(self, **_kwargs: Any) -> None:
            raise ConnectionError("offline")

    logger = RecordingLogger()
    p_any = cast(Any, plugin)
    p_any._logger = logger
    p_any._mqtt_client = FailingMQTT()

    plugin._calculate_and_broadcast_eta(data)

    assert any("MQTT publish failed (connection)" in m for m in logger.error_calls)
    assert logger.debug_calls == []


def test_broadcast_mqtt_publish_other_errors_are_logged_debug(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Non-connection errors in MQTT publishing should be logged at debug level."""
    _set_time(monkeypatch, 100.0)

    plugin._temp_history["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )

    data = {"tool0": {"actual": 20.0, "target": 50.0}}

    class RecordingLogger(DummyLogger):
        def __init__(self) -> None:
            self.error_calls: List[str] = []
            self.debug_calls: List[str] = []

        def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
            self.error_calls.append(msg % args if args else msg)

        def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
            self.debug_calls.append(msg % args if args else msg)

    class FailingMQTT:
        def publish_eta_update(self, **_kwargs: Any) -> None:
            raise RuntimeError("boom")

    logger = RecordingLogger()
    p_any = cast(Any, plugin)
    p_any._logger = logger
    p_any._mqtt_client = FailingMQTT()

    plugin._calculate_and_broadcast_eta(data)

    assert logger.error_calls == []
    assert any("MQTT publish failed" in m for m in logger.debug_calls)


def test_broadcast_filters_unsupported_heaters(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """ETA updates should only be sent for heaters supported by the active profile."""
    _set_time(monkeypatch, 100.0)
    plugin._temp_history["tool0"] = deque(
        [(90.0, 10.0, 50.0), (100.0, 20.0, 50.0)], maxlen=60
    )
    plugin._temp_history["bed"] = deque(
        [(90.0, 20.0, 60.0), (100.0, 30.0, 60.0)], maxlen=60
    )

    data = {
        "tool0": {"actual": 20.0, "target": 50.0},
        "bed": {"actual": 30.0, "target": 60.0},
        "chamber": {"actual": 30.0, "target": 60.0},
    }

    plugin._calculate_and_broadcast_eta(data)

    pm = cast(DummyPluginManager, cast(Any, plugin)._plugin_manager)
    heaters = [
        m["payload"].get("heater")
        for m in pm.messages
        if m["payload"].get("type") == "eta_update"
    ]
    assert "tool0" in heaters
    assert "bed" in heaters
    assert "chamber" not in heaters


def test_suppress_while_printing_clears_once(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """When suppression is enabled, the plugin clears UI once and stops sending ETAs."""
    p_any = cast(Any, plugin)
    p_any._printer = DummyPrinter(printing=True)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["suppress_while_printing"], True)

    _set_time(monkeypatch, 100.0)
    plugin._temp_history["tool0"] = deque(maxlen=60)
    plugin._temp_history["bed"] = deque(maxlen=60)

    plugin.on_printer_add_temperature({"tool0": {"actual": 10.0, "target": 50.0}})

    pm = cast(DummyPluginManager, p_any._plugin_manager)
    # Should have emitted clear messages for known heaters.
    clears = [m for m in pm.messages if m["payload"].get("eta") is None]
    assert clears

    before = len(pm.messages)
    # Second callback while still printing should not spam additional clears.
    _set_time(monkeypatch, 101.0)
    plugin.on_printer_add_temperature({"tool0": {"actual": 12.0, "target": 50.0}})
    assert len(pm.messages) == before


def test_persist_and_restore_profile_history(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Persisted history should be restored on startup (force profile switch)."""
    p1 = TempETAPlugin()
    p1_any = cast(Any, p1)
    p1_any._identifier = "temp_eta"
    p1_any._plugin_version = "0.0.0"
    p1_any._logger = DummyLogger()
    p1_any._plugin_manager = DummyPluginManager()
    p1_any._printer = DummyPrinter(printing=False)
    p1_any._printer_profile_manager = DummyPrinterProfileManager(
        {
            "id": "default",
            "name": "Default",
            "heatedBed": True,
            "heatedChamber": False,
            "extruder": {"count": 1},
        }
    )
    p1_any._settings = DummySettings(
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
    )

    _set_plugin_data_folder(p1, tmp_path)
    p1_any._active_profile_id = "default"

    _set_time(monkeypatch, 100.0)
    p1._temp_history = {
        "tool0": deque([(95.0, 20.0, 50.0), (100.0, 30.0, 50.0)], maxlen=60)
    }
    p1._history_dirty = True
    p1._persist_current_profile_history()
    assert (tmp_path / "history_default.json").exists()

    # Restore in a new instance.
    p2 = TempETAPlugin()
    p2_any = cast(Any, p2)
    p2_any._identifier = "temp_eta"
    p2_any._plugin_version = "0.0.0"
    p2_any._logger = DummyLogger()
    p2_any._plugin_manager = DummyPluginManager()
    p2_any._printer = DummyPrinter(printing=False)
    p2_any._printer_profile_manager = p1_any._printer_profile_manager
    p2_any._settings = p1_any._settings
    _set_plugin_data_folder(p2, tmp_path)

    _set_time(monkeypatch, 100.0)
    p2._switch_active_profile_if_needed(force=True)
    assert "tool0" in p2._temp_history
    assert len(p2._temp_history["tool0"]) == 2


def test_reset_all_profile_histories_deletes_files_and_clears_ui(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin, tmp_path: Path
) -> None:
    """Reset should delete all history_*.json and clear frontend state."""
    _set_plugin_data_folder(plugin, tmp_path)
    (tmp_path / "history_default.json").write_text("{}", encoding="utf-8")
    (tmp_path / "history_other.json").write_text("{}", encoding="utf-8")

    plugin._temp_history = {"tool0": deque(maxlen=60), "bed": deque(maxlen=60)}
    deleted = plugin._reset_all_profile_histories()
    assert deleted == 2

    pm = cast(DummyPluginManager, cast(Any, plugin)._plugin_manager)
    heaters = [
        m["payload"].get("heater")
        for m in pm.messages
        if m["payload"].get("type") == "eta_update"
    ]
    assert set(heaters) == {"tool0", "bed"}


def test_reset_all_profile_histories_handles_delete_failure(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin, tmp_path: Path
) -> None:
    _set_plugin_data_folder(plugin, tmp_path)
    (tmp_path / "history_default.json").write_text("{}", encoding="utf-8")

    plugin._temp_history = {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)}

    def _boom_unlink(self: Path) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(Path, "unlink", _boom_unlink)
    deleted = plugin._reset_all_profile_histories()
    assert deleted == 0

    pm = cast(DummyPluginManager, cast(Any, plugin)._plugin_manager)
    assert any(
        m["payload"].get("heater") == "tool0" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_on_api_command_reset_settings_defaults(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """API reset should restore defaults and emit a settings_reset message."""
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["threshold_start"], 42.0)
    settings.set(["debug_logging"], True)

    # Avoid depending on Flask in unit tests.
    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)

    resp = plugin.on_api_command("reset_settings_defaults", {})
    assert resp.get("success") is True
    assert settings.get_float(["threshold_start"]) == 5.0
    assert settings.get_boolean(["debug_logging"]) is False

    pm = cast(DummyPluginManager, p_any._plugin_manager)
    assert any(m["payload"].get("type") == "settings_reset" for m in pm.messages)


def test_on_api_command_reset_settings_defaults_swallows_send_errors(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["threshold_start"], 42.0)

    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)

    class _BoomPluginManager(DummyPluginManager):
        def send_plugin_message(self, identifier: str, payload: Dict[str, Any]) -> None:
            raise RuntimeError("boom")

    p_any._plugin_manager = _BoomPluginManager()
    resp = plugin.on_api_command("reset_settings_defaults", {})
    assert resp.get("success") is True


def test_on_settings_save_disabling_plugin_clears_frontend(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Disabling the plugin via settings save should clear all displayed heaters."""
    p_any = cast(Any, plugin)
    settings = cast(DummySettings, p_any._settings)
    settings.set(["enabled"], True)
    plugin._temp_history = {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)}

    # Simulate OctoPrint saving settings and setting enabled=False.
    def _fake_save(_self: Any, _data: Dict[str, Any]) -> Dict[str, Any]:
        settings.set(["enabled"], False)
        return _data

    monkeypatch.setattr(
        octoprint_temp_eta.octoprint.plugin.SettingsPlugin,
        "on_settings_save",
        _fake_save,
    )
    plugin.on_settings_save({"enabled": False})

    pm = cast(DummyPluginManager, p_any._plugin_manager)
    assert any(
        m["payload"].get("heater") == "tool0" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_debug_log_settings_snapshot_throttles(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Settings snapshot logging should be throttled and safe."""
    plugin._debug_logging_enabled = True
    calls: List[str] = []

    def _dbg(msg: str, *args: Any) -> None:
        calls.append(msg)

    monkeypatch.setattr(plugin, "_debug_log", _dbg)

    plugin._debug_log_settings_snapshot(100.0)
    plugin._debug_log_settings_snapshot(120.0)
    assert len(calls) == 1

    # Past the throttle window.
    plugin._debug_log_settings_snapshot(200.0)
    assert len(calls) == 2


def test_get_profile_history_path_sanitizes(
    tmp_path: Path, plugin: TempETAPlugin
) -> None:
    """Profile ids should be sanitized to a safe filename."""
    _set_plugin_data_folder(plugin, tmp_path)
    p = plugin._get_profile_history_path("weird/..\\profile id")
    assert p.parent == tmp_path
    assert "history_" in p.name
    assert "/" not in p.name
    assert "\\" not in p.name


def test_load_profile_history_filters_old_and_future(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: TempETAPlugin
) -> None:
    """Loader should ignore samples outside the allowed time window."""
    _set_plugin_data_folder(plugin, tmp_path)
    plugin._persist_max_age_seconds = 10.0

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

    loaded = plugin._load_profile_history("default")
    assert "tool0" in loaded
    assert list(loaded["tool0"]) == [(95.0, 20.0, 50.0)]


def test_reset_profile_history_deletes_file_and_clears(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: TempETAPlugin
) -> None:
    """Reset profile history should delete file and clear UI."""
    _set_plugin_data_folder(plugin, tmp_path)
    (tmp_path / "history_default.json").write_text("{}", encoding="utf-8")
    plugin._temp_history = {"tool0": deque([(1.0, 10.0, 50.0)], maxlen=60)}

    deleted = plugin._reset_profile_history("default")
    assert deleted is True
    assert not (tmp_path / "history_default.json").exists()

    pm = cast(DummyPluginManager, cast(Any, plugin)._plugin_manager)
    assert any(
        m["payload"].get("heater") == "tool0" and m["payload"].get("eta") is None
        for m in pm.messages
    )


def test_persist_current_profile_history_early_returns(
    tmp_path: Path, plugin: TempETAPlugin
) -> None:
    _set_plugin_data_folder(plugin, tmp_path)
    plugin_any = cast(Any, plugin)

    # Missing profile id.
    plugin_any._active_profile_id = ""
    plugin_any._history_dirty = True
    plugin._persist_current_profile_history()
    assert not (tmp_path / "history_default.json").exists()

    # Dirty but no samples.
    plugin_any._active_profile_id = "default"
    plugin_any._history_dirty = True
    plugin._temp_history = {"tool0": deque([], maxlen=60)}
    plugin._persist_current_profile_history()
    assert not (tmp_path / "history_default.json").exists()


def test_on_event_disconnect_persists_then_clears(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: TempETAPlugin
) -> None:
    """Disconnect should persist history (best effort) and clear all heaters."""
    _set_plugin_data_folder(plugin, tmp_path)
    p_any = cast(Any, plugin)
    p_any._active_profile_id = "default"
    plugin._temp_history = {"tool0": deque([(95.0, 20.0, 50.0)], maxlen=60)}
    plugin._cooldown_history = {"tool0": deque([(95.0, 20.0)], maxlen=60)}
    plugin._history_dirty = True

    _set_time(monkeypatch, 100.0)
    plugin.on_event("Disconnected", {})

    assert (tmp_path / "history_default.json").exists()
    assert len(plugin._temp_history["tool0"]) == 0
    assert len(plugin._cooldown_history["tool0"]) == 0


def test_on_event_error_persists_then_clears(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, plugin: TempETAPlugin
) -> None:
    _set_plugin_data_folder(plugin, tmp_path)
    p_any = cast(Any, plugin)
    p_any._active_profile_id = "default"
    plugin._temp_history = {"tool0": deque([(95.0, 20.0, 50.0)], maxlen=60)}
    plugin._cooldown_history = {"tool0": deque([(95.0, 20.0)], maxlen=60)}
    plugin._history_dirty = True

    _set_time(monkeypatch, 100.0)
    plugin.on_event("Error", {})

    assert (tmp_path / "history_default.json").exists()
    assert len(plugin._temp_history["tool0"]) == 0
    assert len(plugin._cooldown_history["tool0"]) == 0


def test_on_event_print_started_resets_suppression_flag(plugin: TempETAPlugin) -> None:
    p_any = cast(Any, plugin)
    p_any._suppressing_due_to_print = True
    plugin.on_event("PrintStarted", {})
    assert p_any._suppressing_due_to_print is False


def test_on_event_shutdown_disconnects_mqtt(plugin: TempETAPlugin) -> None:
    """Shutdown should disconnect the MQTT client when present."""
    p_any = cast(Any, plugin)

    class RecordingMQTT:
        def __init__(self) -> None:
            self.disconnected = False

        def disconnect(self) -> None:
            self.disconnected = True

    mqtt_client = RecordingMQTT()
    p_any._mqtt_client = mqtt_client

    plugin.on_event("Shutdown", {})
    assert mqtt_client.disconnected is True


def test_get_update_information_contains_current_version(plugin: TempETAPlugin) -> None:
    """Software update hook should include the current plugin version."""
    cast(Any, plugin)._plugin_version = "0.5.0rc1"
    info = plugin.get_update_information()
    assert "temp_eta" in info
    assert info["temp_eta"]["current"] == "0.5.0rc1"
    assert info["temp_eta"]["repo"] == "OctoPrint-TempETA"


def test_on_api_command_unknown_returns_error(
    monkeypatch: pytest.MonkeyPatch, plugin: TempETAPlugin
) -> None:
    """Unknown API commands should return a structured error."""
    monkeypatch.setattr(octoprint_temp_eta, "jsonify", lambda payload: payload)
    resp = plugin.on_api_command("nope", {})
    assert resp.get("success") is False


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
