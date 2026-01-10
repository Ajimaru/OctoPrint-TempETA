# coding=utf-8
from __future__ import absolute_import

import json
import math
import re
import threading
import time
from collections import deque
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable

try:
    import octoprint.plugin  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    # Allow importing this module in environments where OctoPrint isn't installed
    # (e.g. CI or static analysis). The real runtime always provides these.
    class _OctoPrintPluginStubs:
        class StartupPlugin:
            pass

        class TemplatePlugin:
            pass

        class SettingsPlugin:
            @staticmethod
            def on_settings_save(self: Any, data: Dict[str, Any]) -> Dict[str, Any]:
                return data

        class AssetPlugin:
            pass

        class EventHandlerPlugin:
            pass

        class SimpleApiPlugin:
            pass

    class _OctoPrintStubs:
        plugin = _OctoPrintPluginStubs

    octoprint = _OctoPrintStubs()  # type: ignore

try:
    from flask import jsonify  # type: ignore
except ModuleNotFoundError:  # pragma: no cover

    def jsonify(*_args: Any, **_kwargs: Any) -> Any:
        raise RuntimeError("Flask is required to use the plugin's API endpoints")


try:
    from flask_babel import gettext  # type: ignore
except ModuleNotFoundError:  # pragma: no cover

    def gettext(message: str) -> str:
        return message


@runtime_checkable
class LoggerLike(Protocol):
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...


@runtime_checkable
class SettingsLike(Protocol):
    def get_boolean(self, path: Sequence[str]) -> bool: ...

    def get_float(self, path: Sequence[str]) -> float: ...

    def get_int(self, path: Sequence[str]) -> int: ...

    def get(self, path: Sequence[str]) -> Any: ...

    def set(self, path: Sequence[str], value: Any) -> None: ...

    def save(self) -> None: ...


@runtime_checkable
class PluginManagerLike(Protocol):
    def send_plugin_message(self, identifier: str, payload: Dict[str, Any]) -> None: ...


@runtime_checkable
class PrinterProfileManagerLike(Protocol):
    def get_current_or_default(self) -> Dict[str, Any]: ...


@runtime_checkable
class PrinterLike(Protocol):
    def register_callback(self, callback: Any) -> None: ...

    def is_printing(self) -> bool: ...

    def is_paused(self) -> bool: ...

    def get_state_id(self) -> str: ...


class TempETAPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.SimpleApiPlugin,
):
    """Main plugin implementation for Temperature ETA.

    Implements OctoPrint Issue #469: Show estimated time remaining
    for printer heating (bed, hotend, chamber).
    """

    # OctoPrint injects these attributes at runtime. Define them explicitly so
    # static type checkers (Pylance/Pyright) don't treat them as Optional/None.
    _logger: LoggerLike
    _settings: SettingsLike
    _printer: PrinterLike
    _printer_profile_manager: PrinterProfileManagerLike
    _plugin_manager: PluginManagerLike
    _identifier: str
    _plugin_version: str

    def __init__(self):
        """Initialize plugin with temperature history tracking."""
        super().__init__()
        self._lock = threading.Lock()

        self._debug_logging_enabled = False
        self._last_debug_log_time = 0.0
        self._last_heater_support_decision = {}

        # Number of temperature samples to keep per heater.
        # This is configurable via settings (history_size). We cache the active
        # value here for fast access in the 2Hz callback.
        self._default_history_size = 60
        self._history_maxlen = self._default_history_size

        # Persist history per printer profile (file per profile id).
        # Note: ETA uses only the most recent seconds of history, so we keep
        # persistence bounded by both maxlen and a max-age filter on load.
        self._active_profile_id: Optional[str] = None
        self._persist_interval = 10.0
        self._last_persist_time = 0.0
        self._persist_max_age_seconds = 180.0
        self._history_dirty = False

        self._temp_history = {
            "bed": deque(maxlen=self._history_maxlen),
            "tool0": deque(maxlen=self._history_maxlen),
            "chamber": deque(maxlen=self._history_maxlen),
        }
        self._last_update_time = 0

        # When enabled, suppress ETA updates while a print job is active.
        # This keeps the UI focused on the pre-print heat-up phase.
        self._suppressing_due_to_print = False

    def _suppress_while_printing_enabled(self) -> bool:
        """Return whether ETA display should be suppressed during active prints."""
        if not getattr(self, "_settings", None):
            return True
        try:
            return bool(self._settings.get_boolean(["suppress_while_printing"]))
        except Exception:
            return True

    def _is_print_job_active(self) -> bool:
        """Return True if OctoPrint considers a print job active.

        We treat paused/pausing/resuming as active as well.
        """
        printer = getattr(self, "_printer", None)
        if printer is None:
            return False

        try:
            if hasattr(printer, "is_printing") and printer.is_printing():
                return True
        except Exception:
            pass

        try:
            if hasattr(printer, "is_paused") and printer.is_paused():
                return True
        except Exception:
            pass

        try:
            if hasattr(printer, "get_state_id"):
                state_id = printer.get_state_id()
                return state_id in ("PRINTING", "PAUSED", "PAUSING", "RESUMING")
        except Exception:
            pass

        return False

    def _refresh_debug_logging_flag(self) -> None:
        """Refresh debug logging flag from settings."""
        if not getattr(self, "_settings", None):
            self._debug_logging_enabled = False
            return
        try:
            self._debug_logging_enabled = bool(
                self._settings.get_boolean(["debug_logging"])
            )
        except Exception:
            self._debug_logging_enabled = False

    def _debug_log(self, message: str, *args: Any) -> None:
        """Log debug information when enabled (info-level for visibility)."""
        if not self._debug_logging_enabled:
            return
        try:
            self._logger.info("[debug] " + message, *args)
        except Exception:
            # Never fail the callback/logging due to formatting issues.
            pass

    def _debug_log_throttled(
        self, now: float, interval: float, message: str, *args: Any
    ) -> None:
        """Throttled debug logging to avoid flooding the log."""
        if not self._debug_logging_enabled:
            return
        if (now - self._last_debug_log_time) < interval:
            return
        self._last_debug_log_time = now
        self._debug_log(message, *args)

    def on_after_startup(self):
        """Called after OctoPrint startup, register for temperature updates."""
        self._logger.info("Temperature ETA Plugin started")
        # Register for temperature callbacks
        self._printer.register_callback(self)

        self._refresh_debug_logging_flag()
        self._debug_log("Debug logging enabled")

        # Apply configured history size now that settings are available.
        self._set_history_maxlen(self._read_history_maxlen_setting())

        # Load persisted history for the active printer profile.
        self._switch_active_profile_if_needed(force=True)

    def _get_current_profile_id(self) -> str:
        """Return current printer profile id or a stable fallback."""
        try:
            profile = self._printer_profile_manager.get_current_or_default()
            if isinstance(profile, dict):
                profile_id = profile.get("id")
                if profile_id:
                    return str(profile_id)
        except Exception:
            pass
        return "default"

    def _get_profile_history_path(self, profile_id: str) -> Path:
        """Return the history file path for a given profile id."""
        safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", profile_id or "default")
        folder = Path(self.get_plugin_data_folder())
        folder.mkdir(parents=True, exist_ok=True)
        return folder / f"history_{safe}.json"

    def _reset_profile_history(self, profile_id: str) -> bool:
        """Delete persisted history for a profile and clear in-memory/UI state.

        Args:
            profile_id (str): Printer profile id.

        Returns:
            bool: True if a file was deleted, False if nothing was deleted.
        """
        deleted = False
        try:
            path = self._get_profile_history_path(profile_id)
            if path.exists():
                path.unlink()
                deleted = True
        except Exception:
            self._logger.debug(
                "Failed to delete history file for profile '%s'",
                str(profile_id),
                exc_info=True,
            )

        with self._lock:
            heaters = list(self._temp_history.keys())
            for h in heaters:
                self._temp_history[h].clear()
            self._history_dirty = False

        self._send_clear_messages(heaters)
        return deleted

    def _reset_all_profile_histories(self) -> int:
        """Delete all persisted per-profile history files for this plugin.

        Returns:
            int: Number of history files deleted.
        """
        folder = Path(self.get_plugin_data_folder())
        deleted_count = 0

        try:
            folder.mkdir(parents=True, exist_ok=True)
            for path in folder.glob("history_*.json"):
                try:
                    if path.is_file():
                        path.unlink()
                        deleted_count += 1
                except Exception:
                    self._logger.debug(
                        "Failed to delete history file '%s'", str(path), exc_info=True
                    )
        except Exception:
            self._logger.debug(
                "Failed to enumerate history files in '%s'", str(folder), exc_info=True
            )

        with self._lock:
            heaters = list(self._temp_history.keys())
            for h in heaters:
                self._temp_history[h].clear()
            self._history_dirty = False

        self._send_clear_messages(heaters)
        return deleted_count

    def _reset_user_settings_to_defaults(self) -> None:
        """Reset user-editable plugin settings to their default values.

        This intentionally does not touch persisted history files. Those are handled
        by the dedicated history reset button/command.
        """
        if not getattr(self, "_settings", None):
            return

        defaults = self.get_settings_defaults()
        keys = (
            "enabled",
            "suppress_while_printing",
            "show_in_sidebar",
            "show_in_navbar",
            "show_in_tab",
            "temp_display",
            "threshold_start",
            "threshold_unit",
            "algorithm",
            "update_interval",
            "history_size",
            "debug_logging",
        )

        for key in keys:
            if key in defaults:
                self._settings.set([key], defaults[key])

        try:
            self._settings.save()
        except Exception:
            # Best-effort: UI should still refresh, and errors are logged by OctoPrint.
            pass

        # Apply settings that affect cached runtime state.
        self._refresh_debug_logging_flag()
        self._set_history_maxlen(self._read_history_maxlen_setting())

    def _load_profile_history(self, profile_id: str) -> Dict[str, deque]:
        """Load persisted history for a profile id.

        Returns a dict mapping heater name to a deque with current maxlen.
        """
        path = self._get_profile_history_path(profile_id)
        if not path.exists():
            return {}

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            self._logger.debug(
                "Failed to read history file for profile '%s'",
                profile_id,
                exc_info=True,
            )
            return {}

        samples = payload.get("samples") if isinstance(payload, dict) else None
        if not isinstance(samples, dict):
            return {}

        now = time.time()
        min_ts = now - self._persist_max_age_seconds

        loaded: Dict[str, deque] = {}
        for heater, points in samples.items():
            if not isinstance(heater, str) or not isinstance(points, list):
                continue

            cleaned = []
            for p in points:
                if not (isinstance(p, (list, tuple)) and len(p) >= 3):
                    continue
                try:
                    ts = float(p[0])
                    actual = float(p[1])
                    target = float(p[2])
                except Exception:
                    continue

                if ts < min_ts or ts > now + 5:
                    continue
                cleaned.append((ts, actual, target))

            if cleaned:
                loaded[heater] = deque(
                    cleaned[-self._history_maxlen :], maxlen=self._history_maxlen
                )

        return loaded

    def _persist_current_profile_history(self) -> None:
        """Persist current in-memory history to the active profile's file."""
        profile_id = getattr(self, "_active_profile_id", None)
        if not profile_id:
            return
        if not self._history_dirty:
            return
        try:
            path = self._get_profile_history_path(profile_id)
            with self._lock:
                samples = {
                    heater: [[ts, actual, target] for (ts, actual, target) in history]
                    for heater, history in self._temp_history.items()
                }

            total_samples = sum(len(v) for v in samples.values())
            if total_samples <= 0:
                return

            payload = {
                "version": 1,
                "saved_at": time.time(),
                "profile_id": profile_id,
                "history_size": self._history_maxlen,
                "samples": samples,
            }
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            self._history_dirty = False
            self._debug_log(
                "Persisted history profile=%s samples=%d path=%s",
                profile_id,
                total_samples,
                str(path),
            )
        except Exception:
            self._logger.debug(
                "Failed to persist history for profile '%s'",
                str(profile_id),
                exc_info=True,
            )

    def _maybe_persist_history(self, now: float) -> None:
        """Persist history occasionally to avoid frequent disk writes."""
        if (now - self._last_persist_time) < self._persist_interval:
            return
        self._last_persist_time = now
        self._persist_current_profile_history()

    def _switch_active_profile_if_needed(self, force: bool = False) -> None:
        """Persist + swap history when active printer profile changes."""
        profile_id = self._get_current_profile_id()
        if not force and profile_id == self._active_profile_id:
            return

        old_profile_id = self._active_profile_id

        old_heaters = []
        with self._lock:
            old_heaters = list(self._temp_history.keys())

        if self._active_profile_id is not None:
            self._persist_current_profile_history()

        self._active_profile_id = profile_id
        # On startup we restore persisted history for the active profile.
        # On runtime profile switches we intentionally start with an empty history
        # so the ETA uses only live samples from the new profile.
        loaded = self._load_profile_history(profile_id) if force else {}
        self._debug_log(
            "Profile switch %s -> %s (force=%s, restore_persisted=%s)",
            str(old_profile_id),
            str(profile_id),
            str(force),
            str(force),
        )

        if self._debug_logging_enabled:
            try:
                profile = self._printer_profile_manager.get_current_or_default()
                if isinstance(profile, dict):
                    profile_name = profile.get("name", "unknown")
                    heated_bed = bool(profile.get("heatedBed", False))
                    heated_chamber = bool(profile.get("heatedChamber", False))
                    extruder_data = (
                        profile.get("extruder", {})
                        if isinstance(profile.get("extruder", {}), dict)
                        else {}
                    )
                    extruder_count = int(extruder_data.get("count", 0) or 0)
                    self._debug_log(
                        "Profile summary id=%s name=%s extruders=%d heatedBed=%s heatedChamber=%s",
                        str(profile_id),
                        str(profile_name),
                        extruder_count,
                        str(heated_bed),
                        str(heated_chamber),
                    )
            except Exception:
                self._debug_log("Profile summary unavailable id=%s", str(profile_id))

        with self._lock:
            # IMPORTANT: Do not carry over samples from the previous profile.
            # Start strictly from what's persisted for this profile (or empty).
            new_history: Dict[str, deque] = {}
            for heater, history in loaded.items():
                new_history[heater] = deque(history, maxlen=self._history_maxlen)

            self._temp_history = new_history

        # Loaded state is considered clean until we append new samples.
        self._history_dirty = False

        if not force:
            self._debug_log(
                "Cleared live (RAM) history for new profile=%s", str(profile_id)
            )

        # Reset cached heater support decisions for the new profile.
        self._last_heater_support_decision = {}

        # Clear any stale UI values that might linger across profile switches.
        self._send_clear_messages(old_heaters)

    def _read_history_maxlen_setting(self) -> int:
        """Read and sanitize history size setting.

        Returns:
            int: Max number of samples to keep per heater.
        """
        if not getattr(self, "_settings", None):
            return self._default_history_size

        try:
            value = int(self._settings.get_int(["history_size"]))
        except Exception:
            value = self._default_history_size

        # UI constrains to 10..300; keep backend aligned.
        return max(10, min(300, value))

    def _set_history_maxlen(self, maxlen: int) -> None:
        """Update internal history deques to a new maxlen.

        Rebuilds existing deques to apply the new maxlen and trims old samples if
        needed. Must be fast and thread-safe.

        Args:
            maxlen (int): New maximum length for all heater histories.
        """
        if maxlen <= 0:
            maxlen = self._default_history_size

        with self._lock:
            if maxlen == self._history_maxlen:
                return

            self._history_maxlen = maxlen

            self._debug_log("Updated history_size maxlen=%d", self._history_maxlen)

            for heater, history in list(self._temp_history.items()):
                new_history = deque(history, maxlen=maxlen)
                self._temp_history[heater] = new_history

            # Persist trimmed/expanded histories.
            self._history_dirty = True

    def _is_heater_supported(self, heater_name):
        """Check if heater is part of the active printer profile.

        Only show heaters that are actually configured in the active printer profile.

        Args:
            heater_name (str): Name of heater (tool0, tool1, bed, chamber)

        Returns:
            bool: True if heater is supported by current profile
        """

        def _log_support_if_changed(supported: bool, details: str) -> None:
            if not self._debug_logging_enabled:
                return
            key = str(heater_name)
            prev = self._last_heater_support_decision.get(key)
            if prev is None or bool(prev) != bool(supported):
                self._last_heater_support_decision[key] = bool(supported)
                self._debug_log(
                    "Heater support heater=%s supported=%s %s",
                    str(heater_name),
                    str(bool(supported)),
                    details,
                )

        try:
            profile = self._printer_profile_manager.get_current_or_default()
            if not isinstance(profile, dict) or not profile:
                _log_support_if_changed(False, "(no profile)")
                return False

            profile_name = profile.get("name", "unknown")
            heated_bed = bool(profile.get("heatedBed", False))
            heated_chamber = bool(profile.get("heatedChamber", False))
            extruder_data = (
                profile.get("extruder", {})
                if isinstance(profile.get("extruder", {}), dict)
                else {}
            )
            extruder_count = int(extruder_data.get("count", 0) or 0)

            if heater_name == "bed":
                supported = heated_bed
                _log_support_if_changed(
                    supported, f"profile={profile_name} heatedBed={heated_bed}"
                )
                return supported

            if heater_name == "chamber":
                supported = heated_chamber
                _log_support_if_changed(
                    supported, f"profile={profile_name} heatedChamber={heated_chamber}"
                )
                return supported

            if isinstance(heater_name, str) and heater_name.startswith("tool"):
                try:
                    tool_idx = int(heater_name.replace("tool", ""))
                except (ValueError, TypeError):
                    _log_support_if_changed(
                        False, f"profile={profile_name} invalid_tool_index"
                    )
                    return False

                supported = tool_idx < extruder_count
                _log_support_if_changed(
                    supported,
                    f"profile={profile_name} tool_idx={tool_idx} extruder_count={extruder_count}",
                )
                return supported

            _log_support_if_changed(False, f"profile={profile_name} unknown_heater")
            return False
        except Exception:
            if self._debug_logging_enabled:
                self._debug_log("Heater support error heater=%s", str(heater_name))
            return False

    # Temperature callback handler
    def on_printer_add_temperature(self, data):
        """Called when new temperature data is available (~2Hz).

        Args:
            data (dict): Temperature data from OctoPrint
                {
                    "bed": {"actual": float, "target": float},
                    "tool0": {"actual": float, "target": float},
                    ...
                }
        """
        if not self._settings.get_boolean(["enabled"]):
            return

        # Ensure we are tracking the right profile's history.
        self._switch_active_profile_if_needed()

        # If enabled, suppress ETA completely while OctoPrint considers a print job active.
        if self._suppress_while_printing_enabled() and self._is_print_job_active():
            # Clear once when suppression starts to avoid stale countdowns.
            if not self._suppressing_due_to_print:
                self._suppressing_due_to_print = True
                self._clear_all_heaters_frontend()
            return

        # If we were suppressing but the condition no longer applies (e.g. warm-up resumed or print ended), re-enable.
        if self._suppressing_due_to_print:
            self._suppressing_due_to_print = False

        current_time = time.time()
        threshold = self._settings.get_float(["threshold_start"])

        # Log all heaters received from OctoPrint
        heaters_in_data = [k for k, v in data.items() if isinstance(v, dict)]
        if heaters_in_data:
            self._logger.debug(
                f"Received temperature data for heaters: {heaters_in_data}"
            )

        epsilon_hold = 0.2

        recorded_count = 0
        with self._lock:
            # Update temperature history for each heater (dynamically register new heizers)
            for heater, temps in data.items():
                # Skip non-dict values (like timestamps)
                if not isinstance(temps, dict):
                    continue

                # Only record history while ETA could be shown:
                # - target must be set
                # - we must be below target
                # - remaining must be >= configured threshold
                target_raw = temps.get("target", 0)
                actual_raw = temps.get("actual")
                if actual_raw is None:
                    continue
                try:
                    target = float(target_raw or 0)
                    actual = float(actual_raw)
                except Exception:
                    continue

                if target <= 0:
                    continue

                remaining = target - actual
                # Don't record while holding temperature at/near target.
                # This avoids persistent history updates when the printer keeps a target set.
                if remaining <= epsilon_hold:
                    continue
                if remaining < threshold:
                    continue

                # Auto-create history for new heizers
                if heater not in self._temp_history:
                    self._temp_history[heater] = deque(maxlen=self._history_maxlen)

                self._temp_history[heater].append((current_time, actual, target))
                self._history_dirty = True
                recorded_count += 1

        # Avoid flooding logs while idle/holding temperature: log far less often
        # when we didn't record any samples.
        debug_interval = 5.0 if recorded_count > 0 else 60.0
        self._debug_log_throttled(
            current_time,
            debug_interval,
            "Temp callback profile=%s heaters=%d recorded=%d threshold=%.2f",
            str(self._active_profile_id),
            len(heaters_in_data),
            recorded_count,
            float(threshold),
        )

        # Update frontend at configurable interval (default 1Hz)
        if current_time - self._last_update_time >= self._settings.get_float(
            ["update_interval"]
        ):
            self._last_update_time = current_time
            self._calculate_and_broadcast_eta(data)
            self._maybe_persist_history(current_time)

    def on_printer_send_current_data(self, data):
        """Stub: Called when current printer data is sent (required by callback interface)."""
        pass

    def on_printer_add_log(self, data):
        """Stub: Called when log entry is added (required by callback interface)."""
        pass

    # EventHandlerPlugin
    def on_event(self, event, payload):
        """Handle OctoPrint events to keep UI state consistent.

        Clears all ETAs immediately on disconnect or printer errors so the navbar/tab
        do not keep showing stale countdowns.

        Args:
            event (str): OctoPrint event name
            payload (dict): Event payload
        """
        if event in (
            "Disconnected",
            "Error",
            "Shutdown",
        ):  # clear UI on connection loss
            # Persist what we have before clearing.
            self._persist_current_profile_history()
            with self._lock:
                heaters = list(self._temp_history.keys())
                for h in heaters:
                    self._temp_history[h].clear()

            self._send_clear_messages(heaters)

        # Reset suppression flag on job lifecycle changes; actual suppression is decided in the temperature callback.
        if event in (
            "PrintStarted",
            "PrintResumed",
            "PrintDone",
            "PrintFailed",
            "PrintCancelled",
        ):
            self._suppressing_due_to_print = False

    def _calculate_and_broadcast_eta(self, data):
        """Calculate ETA for each heater and send to frontend.

        Filters heaters based on active printer profile configuration.

        Args:
            data (dict): Current temperature data with all available heaters
        """
        algorithm = self._settings.get(["algorithm"])
        threshold = self._settings.get_float(["threshold_start"])

        with self._lock:
            # Process all heaters in data (dynamically support tool0, tool1, tool2, etc)
            for heater, heater_data in data.items():
                # Skip non-dict values (like timestamps)
                if not isinstance(heater_data, dict):
                    continue

                # Filter by printer profile - only send supported heaters to frontend
                if not self._is_heater_supported(heater):
                    continue

                # Auto-create history for new heizers if not exists
                if heater not in self._temp_history:
                    self._temp_history[heater] = deque(maxlen=self._history_maxlen)

                # OctoPrint may include non-numeric or None values (e.g. during reconnect).
                # Never allow exceptions to bubble out of the temperature callback.
                target_raw = heater_data.get("target", 0)
                actual_raw = heater_data.get("actual", 0)

                try:
                    target = float(target_raw or 0)
                except Exception:
                    target = 0.0

                try:
                    actual = float(actual_raw or 0)
                except Exception:
                    actual = 0.0

                # Only calculate ETA if heating and within threshold
                if target <= 0:
                    # No target set
                    eta = None
                elif actual >= target:
                    # Already at or above target
                    eta = None
                elif (target - actual) >= threshold:
                    # Still far from target - calculate ETA
                    if algorithm == "exponential":
                        eta = self._calculate_exponential_eta(heater, target)
                    else:
                        eta = self._calculate_linear_eta(heater, target)

                    # Hide ETA if less than 1 second (avoid flashing 0:00)
                    if eta is not None and eta < 1:
                        eta = None
                else:
                    # Very close to target
                    eta = None

                # Send message to frontend (ALWAYS, even when eta is None to clear display)
                self._plugin_manager.send_plugin_message(
                    self._identifier,
                    {
                        "type": "eta_update",
                        "heater": heater,
                        "eta": eta,
                        "target": target,
                        "actual": actual,
                    },
                )

    def _calculate_linear_eta(self, heater, target):
        """Calculate ETA assuming constant heating rate.

        Args:
            heater (str): Heater name (bed, tool0, chamber)
            target (float): Target temperature

        Returns:
            float: Estimated seconds to target, or None if insufficient data
        """
        history = self._temp_history.get(heater, deque())
        if len(history) < 2:
            return None

        # Use last 10 seconds of data for rate calculation
        now = time.time()
        recent = [h for h in history if h[0] > now - 10]

        if len(recent) < 2:
            return None

        # rate = ΔT / Δt (°C per second)
        time_diff = recent[-1][0] - recent[0][0]
        temp_diff = recent[-1][1] - recent[0][1]

        if time_diff <= 0 or temp_diff <= 0:
            return None

        rate = temp_diff / time_diff
        remaining = target - recent[-1][1]

        if remaining <= 0:
            return None

        eta = remaining / rate
        return max(0, eta)

    def _calculate_exponential_eta(self, heater, target):
        """Calculate ETA accounting for thermal asymptotic behavior.

        Uses model: T(t) = T_final - (T_final - T_0) * e^(-t/tau)

        Args:
            heater (str): Heater name
            target (float): Target temperature

        Returns:
            float: Estimated seconds to target, or None if insufficient data
        """
        history = self._temp_history.get(heater, deque())
        if len(history) < 3:
            return None

        # Use a recent window for the fit
        now = time.time()
        window_seconds = 30
        recent = [h for h in history if h[0] > now - window_seconds]

        if len(recent) < 6:
            return self._calculate_linear_eta(heater, target)

        # Current sample
        t_now, temp_now, _ = recent[-1]
        remaining_now = target - temp_now
        if remaining_now <= 0:
            return None

        # We model the approach to target as asymptotic. Since reaching target exactly
        # would be infinite time, estimate the time until we are within epsilon.
        epsilon_c = 0.5
        if remaining_now <= epsilon_c:
            return 0.0

        # Build regression data for ln(target - T).
        # Exclude points too close to target (noise dominates) and invalid samples.
        t0 = recent[0][0]
        xs = []
        ys = []
        for ts, temp, _ in recent:
            delta = target - temp
            if delta <= epsilon_c:
                continue
            x = ts - t0
            if x < 0:
                continue
            xs.append(x)
            ys.append(math.log(delta))

        if len(xs) < 6:
            return self._calculate_linear_eta(heater, target)

        span = xs[-1] - xs[0]
        if span < 5:
            return self._calculate_linear_eta(heater, target)

        # Require we are actually heating in this window.
        if (recent[-1][1] - recent[0][1]) <= 0.2:
            return None

        # Linear regression: y = a + b*x, where b should be negative.
        x_mean = sum(xs) / len(xs)
        y_mean = sum(ys) / len(ys)
        sxx = 0.0
        sxy = 0.0
        for x, y in zip(xs, ys):
            dx = x - x_mean
            dy = y - y_mean
            sxx += dx * dx
            sxy += dx * dy

        if sxx <= 0:
            return self._calculate_linear_eta(heater, target)

        slope = sxy / sxx
        if slope >= -1e-4:
            # Not decaying fast enough or unstable -> fallback.
            return self._calculate_linear_eta(heater, target)

        tau = -1.0 / slope
        if tau <= 0 or tau > 2000:
            return self._calculate_linear_eta(heater, target)

        # ETA to reach epsilon band.
        try:
            eta = tau * math.log(remaining_now / epsilon_c)
        except ValueError:
            return self._calculate_linear_eta(heater, target)

        if eta < 0:
            eta = 0.0

        # Protect against spikes: if exponential estimate is wildly larger than
        # the linear estimate on the same data, trust the linear estimate.
        linear_eta = self._calculate_linear_eta(heater, target)
        if linear_eta is not None and eta > (linear_eta * 5):
            return linear_eta

        return eta

    # SettingsPlugin mixin
    def get_settings_defaults(self):
        """Return the default settings for the plugin.

        Returns:
            dict: Dictionary containing default plugin settings.
        """
        return dict(
            enabled=True,
            suppress_while_printing=False,
            show_in_sidebar=True,
            show_in_navbar=True,
            show_in_tab=True,
            show_progress_bars=True,
            show_historical_graph=False,
            historical_graph_window_seconds=180,
            temp_display="octoprint",
            threshold_unit="octoprint",
            debug_logging=False,
            threshold_start=5.0,
            algorithm="linear",
            update_interval=1.0,
            history_size=60,
        )

    # TemplatePlugin mixin
    def is_template_autoescaped(self) -> bool:  # pyright: ignore
        """Enable autoescaping for all plugin templates.

        Opt-in to OctoPrint's template autoescaping (OctoPrint 1.11+) to reduce
        XSS risk from unescaped injected variables.

        Returns:
            bool: True to enable autoescaping.
        """
        return True

    def get_template_configs(self):
        """Configure which templates to use and how to bind them.

        Returns:
            list: List of template configuration dictionaries.
        """
        return [
            dict(type="navbar", custom_bindings=True),
            dict(
                type="sidebar",
                custom_bindings=False,
                name=gettext("Temperature ETA"),
                icon="fa fa-clock",
            ),
            # Use OctoPrint's default settingsViewModel binding for settings UI.
            dict(type="settings", custom_bindings=True),
            dict(type="tab", custom_bindings=False),
        ]

    def on_settings_save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Persist settings and clear UI/state when disabling the plugin.

        OctoPrint applies settings changes only on save. When the plugin is disabled,
        we actively clear any previously shown countdowns in navbar/tab so the UI
        does not keep showing stale values.

        Args:
            data (dict): Settings data posted from the UI.
        """
        if not getattr(self, "_settings", None):
            return {}

        was_enabled = bool(self._settings.get_boolean(["enabled"]))
        old_debug = bool(getattr(self, "_debug_logging_enabled", False))
        old_history_maxlen = self._read_history_maxlen_setting()
        saved = octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        is_enabled = bool(self._settings.get_boolean(["enabled"]))

        self._refresh_debug_logging_flag()
        if old_debug != bool(self._debug_logging_enabled):
            self._logger.info(
                "Debug logging %s",
                "enabled" if self._debug_logging_enabled else "disabled",
            )

        new_history_maxlen = self._read_history_maxlen_setting()
        if new_history_maxlen != old_history_maxlen:
            self._set_history_maxlen(new_history_maxlen)

        if was_enabled and not is_enabled:
            self._clear_all_heaters_frontend()

        return saved if isinstance(saved, dict) else {}

    def _clear_all_heaters_frontend(self):
        """Clear ETA display in the frontend for all known heaters."""
        if not getattr(self, "_plugin_manager", None):
            return

        with self._lock:
            heaters = list(self._temp_history.keys())
            for heater in heaters:
                self._temp_history[heater].clear()

        self._send_clear_messages(heaters)

    def _send_clear_messages(self, heaters) -> None:
        """Send eta_update clear messages for a list of heaters."""
        if not getattr(self, "_plugin_manager", None):
            return

        for heater in heaters or []:
            self._plugin_manager.send_plugin_message(
                self._identifier,
                {
                    "type": "eta_update",
                    "heater": heater,
                    "eta": None,
                    "target": None,
                    "actual": None,
                },
            )

    # AssetPlugin mixin
    def get_assets(self):
        """Return static assets (JS, CSS, LESS) to be included.

        Returns:
            dict: Dictionary with asset types and their file paths.
        """
        return dict(
            js=["js/temp_eta.js"],
            less=["less/temp_eta.less"],
        )

    # SimpleApiPlugin mixin
    def is_api_protected(self) -> bool:  # type: ignore[override]
        """Whether the Simple API requires an authenticated user.

        OctoPrint's default for this will switch from False to True in the
        future. We explicitly opt in to avoid relying on defaults.
        """
        return True

    def is_api_adminonly(self) -> bool:  # type: ignore[override]
        """Whether the Simple API is restricted to admin users."""
        return True

    def get_api_commands(self) -> Dict[str, list]:  # type: ignore[override]
        """Return supported Simple API commands for the plugin."""
        return {
            "reset_profile_history": [],
            "reset_settings_defaults": [],
        }

    def on_api_command(self, command: str, data: Dict[str, Any]):  # type: ignore[override]
        """Handle Simple API commands."""
        if command == "reset_profile_history":
            deleted_count = self._reset_all_profile_histories()
            profile_id = self._get_current_profile_id()
            logger = getattr(self, "_logger", None)
            if logger is not None:
                logger.info(
                    "Reset persisted history for all profiles (trigger_profile=%s deleted_files=%d)",
                    str(profile_id),
                    int(deleted_count),
                )
            return jsonify(
                {
                    "success": True,
                    "profile_id": profile_id,
                    "deleted_files": deleted_count,
                }
            )

        if command == "reset_settings_defaults":
            self._reset_user_settings_to_defaults()
            logger = getattr(self, "_logger", None)
            if logger is not None:
                logger.info("Restored plugin settings defaults (user-editable keys)")

            # Notify all connected clients so the settings UI can refresh via requestData().
            if getattr(self, "_plugin_manager", None):
                try:
                    self._plugin_manager.send_plugin_message(
                        self._identifier, {"type": "settings_reset"}
                    )
                except Exception:
                    pass

            return jsonify({"success": True, "message": gettext("Defaults restored.")})

        return jsonify({"success": False, "error": "unknown_command"})

    # Softwareupdate hook
    def get_update_information(self):
        """Provide update information for the Software Update plugin.

        Returns:
            dict: Update configuration for the plugin.
        """
        return dict(
            temp_eta=dict(
                displayName="Temperature ETA Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="Ajimaru",
                repo="OctoPrint-TempETA",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/Ajimaru/OctoPrint-TempETA/archive/{target_version}.zip",
            )
        )


__plugin_name__ = "Temperature ETA"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = TempETAPlugin()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
