# flake8: noqa
# pylint: disable=line-too-long
"""MQTT publisher for Temperature ETA plugin.

Delegates all MQTT communication to the official OctoPrint-MQTT plugin via
its ``mqtt_publish`` helper. This plugin never opens its own broker
connection: broker host, credentials, and TLS are configured in the
OctoPrint-MQTT plugin. Integration is strictly publish-only - the plugin
cannot be controlled via MQTT.

Optionally publishes retained Home Assistant autodiscovery configs so the
per-heater ETA sensors appear automatically as a device in Home Assistant.
"""

import math
import re
import threading
import time
from typing import Any, Callable, Optional


class MqttPublisher:
    """Thread-safe MQTT publisher backed by the OctoPrint-MQTT plugin helper.

    Keeps the exact topic scheme and payload format of the previous built-in
    client (``{base}/{heater}/eta`` and ``{base}/{heater}/state_change``),
    including per-heater publish throttling and state transition events.
    """

    # object-id -> (display name, extra Home Assistant discovery config attributes)
    SENSOR_DEFINITIONS = {
        "eta_seconds": (
            "ETA",
            {
                "value_template": "{{ value_json.eta_seconds }}",
                "unit_of_measurement": "s",
                "icon": "mdi:timer-sand",
            },
        ),
        "state": (
            "State",
            {
                "value_template": "{{ value_json.state if value_json.state else 'idle' }}",
                "icon": "mdi:thermometer-lines",
            },
        ),
        "actual": (
            "Temperature",
            {
                "value_template": "{{ value_json.actual }}",
                "unit_of_measurement": "°C",
                "device_class": "temperature",
                "state_class": "measurement",
                "icon": "mdi:thermometer",
            },
        ),
        "target": (
            "Target temperature",
            {
                "value_template": "{{ value_json.target }}",
                "unit_of_measurement": "°C",
                "device_class": "temperature",
                "icon": "mdi:thermometer-chevron-up",
            },
        ),
    }

    def __init__(self, logger: Any, plugin_version: str = ""):
        """Initialize the publisher.

        Args:
            logger: Logger instance for debug/info messages
            plugin_version: Plugin version, used in discovery device info
        """
        self._logger = logger
        self._plugin_version = plugin_version
        self._lock = threading.Lock()

        # mqtt_publish helper from the OctoPrint-MQTT plugin, acquired in
        # initialize(); None while the MQTT plugin is not available.
        self._mqtt_publish: Optional[Callable[..., Any]] = None

        self._enabled = False

        # Publishing settings
        self._base_topic = "octoprint/temp_eta"
        self._qos = 0
        self._retain = False
        self._publish_interval = 1.0

        # Home Assistant autodiscovery settings
        self._discovery_enabled = False
        self._discovery_prefix = "homeassistant"
        self._instance_slug = ""

        # State tracking for state transition events.
        # Publish throttling is tracked per heater: a shared timestamp would let
        # the first heater in every broadcast batch consume the publish slot and
        # permanently starve the others.
        self._last_published_time: dict[str, float] = {}
        self._last_heater_state: dict[str, Optional[str]] = {}

        # Identity of the last published discovery configs, so retained
        # topics can be cleared even after the identity changed:
        # (discovery_prefix, instance_slug, heaters tuple)
        self._last_discovery_identity: Optional[tuple[str, str, tuple[str, ...]]] = None

    def initialize(self, plugin_manager: Any) -> None:
        """Acquire the mqtt_publish helper from the OctoPrint-MQTT plugin.

        Call from ``on_after_startup`` (all plugins are loaded by then).

        Args:
            plugin_manager: OctoPrint plugin manager instance
        """
        helper = self._acquire_helper(plugin_manager)
        with self._lock:
            self._mqtt_publish = helper
        if helper is not None:
            self._logger.info("MQTT plugin helper found, MQTT publishing available")
        else:
            self._logger.info(
                "OctoPrint-MQTT plugin not available, MQTT publishing disabled. "
                "Install and enable the OctoPrint-MQTT plugin to use MQTT features."
            )

    def _acquire_helper(self, plugin_manager: Any) -> Optional[Callable[..., Any]]:
        """Fetch the mqtt_publish helper, returning None when unavailable."""
        try:
            helpers = plugin_manager.get_helpers("mqtt", "mqtt_publish")
        except (AttributeError, TypeError, ValueError) as e:
            self._logger.debug("Could not query MQTT plugin helpers: %s", str(e))
            return None
        if helpers and "mqtt_publish" in helpers:
            return helpers["mqtt_publish"]
        return None

    def is_mqtt_plugin_available(self) -> bool:
        """Check whether the OctoPrint-MQTT publish helper was acquired.

        Returns:
            bool: True if the OctoPrint-MQTT plugin is installed and enabled
        """
        with self._lock:
            return self._mqtt_publish is not None

    def is_operational(self) -> bool:
        """Check whether publishing is enabled and the helper is available."""
        with self._lock:
            return self._mqtt_publish is not None and self._enabled

    def configure(self, settings: dict[str, Any]) -> None:
        """Update MQTT configuration from plugin settings.

        Args:
            settings: Dictionary with MQTT configuration keys
        """
        with self._lock:
            self._enabled = bool(settings.get("mqtt_enabled", False))

            base_topic = str(
                settings.get("mqtt_base_topic", "octoprint/temp_eta")
            ).strip()
            use_appearance_name = bool(settings.get("mqtt_use_appearance_name", True))
            appearance_name = str(settings.get("mqtt_appearance_name") or "").strip()
            custom_identifier = str(settings.get("mqtt_custom_identifier", "")).strip()

            # Build final topic with optional identifier suffix
            self._base_topic = self._build_final_topic(
                base_topic, use_appearance_name, appearance_name, custom_identifier
            )
            self._instance_slug = self._build_instance_slug(
                use_appearance_name, appearance_name, custom_identifier
            )

            self._qos = self._coerce_int(
                settings.get("mqtt_qos"), default=0, lo=0, hi=2
            )
            self._retain = bool(settings.get("mqtt_retain", False))
            self._publish_interval = self._coerce_float(
                settings.get("mqtt_publish_interval"), default=1.0, lo=0.0, hi=3600.0
            )

            self._discovery_enabled = bool(
                settings.get("mqtt_discovery_enabled", False)
            )
            self._discovery_prefix = (
                str(settings.get("mqtt_discovery_prefix") or "homeassistant")
                .strip()
                .strip("/")
            ) or "homeassistant"

    @staticmethod
    def _coerce_int(raw: Any, default: int, lo: int, hi: int) -> int:
        """Coerce a settings value to an int clamped to [lo, hi].

        Settings may arrive as str/None/garbage (e.g. hand-edited config.yaml);
        configuration must never raise into OctoPrint's settings-save flow.
        """
        try:
            value = int(float(raw))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return default
        return max(lo, min(hi, value))

    @staticmethod
    def _coerce_float(raw: Any, default: float, lo: float, hi: float) -> float:
        """Coerce a settings value to a finite float clamped to [lo, hi]."""
        try:
            value = float(raw)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return default
        if not math.isfinite(value):
            return default
        return max(lo, min(hi, value))

    def _build_final_topic(
        self,
        base_topic: str,
        use_appearance_name: bool,
        appearance_name: str,
        custom_identifier: str,
    ) -> str:
        """Build the final MQTT base topic with optional identifier suffix.

        Args:
            base_topic: Base MQTT topic
            use_appearance_name: Whether to append appearance name
            appearance_name: Printer appearance name from OctoPrint settings
            custom_identifier: Custom identifier to append (fallback)

        Returns:
            str: Final MQTT base topic
        """
        topic = (base_topic or "octoprint/temp_eta").rstrip("/")

        suffix = ""
        if use_appearance_name and appearance_name:
            suffix = self._sanitize_topic_segment(appearance_name)
        elif custom_identifier:
            suffix = self._sanitize_topic_segment(custom_identifier)

        if suffix:
            return f"{topic}/{suffix}"

        return topic

    def _build_instance_slug(
        self,
        use_appearance_name: bool,
        appearance_name: str,
        custom_identifier: str,
    ) -> str:
        """Build a slug identifying this OctoPrint instance in discovery ids.

        Uses the same identifier preference as the topic suffix so unique_ids
        stay stable and per-instance when several instances share one broker.
        """
        if use_appearance_name and appearance_name:
            return self._slugify(appearance_name)
        if custom_identifier:
            return self._slugify(custom_identifier)
        return "octoprint"

    @staticmethod
    def _slugify(value: str) -> str:
        """Reduce a value to a Home Assistant compatible object-id slug."""
        return re.sub(r"[^a-z0-9_]+", "_", value.strip().lower()).strip("_") or (
            "octoprint"
        )

    @staticmethod
    def _sanitize_topic_segment(segment: str) -> str:
        """Sanitize a user-supplied MQTT topic segment.

        MQTT PUBLISH topic names must not contain the wildcard characters
        ``+`` or ``#`` (these are only valid in subscriptions) nor the null
        character. Leading/trailing slashes are also stripped so the segment
        joins cleanly with the base topic without producing empty levels.

        Args:
            segment: Raw user-supplied segment (appearance name or identifier)

        Returns:
            str: Sanitized segment safe to append to a base topic, possibly
            empty if nothing usable remains.
        """
        sanitized = segment.strip()
        for char in ("+", "#", "\x00"):
            sanitized = sanitized.replace(char, "")
        return sanitized.strip("/")

    def publish_eta_update(
        self,
        heater: str,
        eta: Optional[float],
        eta_kind: Optional[str],
        target: Optional[float],
        actual: Optional[float],
        cooldown_target: Optional[float] = None,
    ) -> None:
        """Publish ETA update for a heater.

        Args:
            heater: Heater name (bed, tool0, chamber)
            eta: ETA in seconds, or None
            eta_kind: "heating", "cooling", or None
            target: Target temperature
            actual: Actual temperature
            cooldown_target: Cooldown target temperature (if applicable)
        """
        with self._lock:
            if not self._enabled or self._mqtt_publish is None:
                return

            # Check if we should publish based on the per-heater interval
            now = time.time()
            if (
                now - self._last_published_time.get(heater, 0.0)
            ) < self._publish_interval:
                return

            self._last_published_time[heater] = now

            # Determine state for transition detection
            current_state = None
            if eta_kind == "heating" and eta is not None:
                current_state = "heating"
            elif eta_kind == "cooling" and eta is not None:
                current_state = "cooling"
            elif target is not None and actual is not None:
                if abs(target - actual) <= 1.0:
                    current_state = "at_target"
                elif cooldown_target is not None and actual is not None:
                    if abs(cooldown_target - actual) <= 1.0:
                        current_state = "cooled_down"

            # Detect state transitions
            last_state = self._last_heater_state.get(heater)
            state_changed = last_state != current_state
            self._last_heater_state[heater] = current_state

            # Build payload
            payload = {
                "heater": heater,
                "eta_seconds": eta,
                "eta_kind": eta_kind,
                "target": target,
                "actual": actual,
                "cooldown_target": cooldown_target,
                "timestamp": now,
                "state": current_state,
            }

            # Publish ETA data
            topic = f"{self._base_topic}/{heater}/eta"
            self._publish_message(topic, payload)

            # Publish state transition event if state changed
            if state_changed and current_state is not None:
                event_payload = {
                    "heater": heater,
                    "state": current_state,
                    "previous_state": last_state,
                    "timestamp": now,
                    "actual": actual,
                    "target": target,
                }
                event_topic = f"{self._base_topic}/{heater}/state_change"
                self._publish_message(event_topic, event_payload)

                self._logger.info(
                    "MQTT: %s state changed from %s to %s",
                    heater,
                    last_state or "unknown",
                    current_state,
                )

    def publish_discovery(self, heaters: list[str]) -> None:
        """Publish retained Home Assistant autodiscovery configs.

        Args:
            heaters: Heater names to publish sensors for (e.g. tool0, bed)
        """
        with self._lock:
            if (
                self._mqtt_publish is None
                or not self._enabled
                or not self._discovery_enabled
                or not heaters
            ):
                return

            for heater in heaters:
                for object_id in self.SENSOR_DEFINITIONS:
                    topic = self._discovery_topic(
                        self._discovery_prefix, self._instance_slug, heater, object_id
                    )
                    payload = self._build_discovery_payload(heater, object_id)
                    # Discovery configs are always retained, otherwise Home
                    # Assistant loses them on restart.
                    self._publish_message(topic, payload, retained=True)

            self._last_discovery_identity = (
                self._discovery_prefix,
                self._instance_slug,
                tuple(heaters),
            )
            self._logger.info(
                "Published MQTT discovery configs for %d heater(s) as instance '%s'",
                len(heaters),
                self._instance_slug,
            )

    def clear_retained_topics(self) -> None:
        """Clear previously published retained discovery configs.

        Publishes empty retained payloads (Home Assistant convention for
        removing discovered entities). Uses the identity of the last
        published discovery configs so the old topics are cleared even when
        prefix/identifier changed in the same settings save.
        """
        with self._lock:
            if self._mqtt_publish is None or self._last_discovery_identity is None:
                return

            prefix, instance_slug, heaters = self._last_discovery_identity
            for heater in heaters:
                for object_id in self.SENSOR_DEFINITIONS:
                    topic = self._discovery_topic(
                        prefix, instance_slug, heater, object_id
                    )
                    self._publish_message(topic, "", retained=True)

            self._last_discovery_identity = None
            self._logger.info(
                "Cleared retained MQTT discovery topics for instance '%s'",
                instance_slug,
            )

    @staticmethod
    def _discovery_topic(
        prefix: str, instance_slug: str, heater: str, object_id: str
    ) -> str:
        """Build a Home Assistant discovery config topic."""
        return f"{prefix}/sensor/temp_eta_{instance_slug}/{heater}_{object_id}/config"

    def _build_discovery_payload(self, heater: str, object_id: str) -> dict[str, Any]:
        """Build a Home Assistant discovery config payload (lock must be held)."""
        display_name, extra_config = self.SENSOR_DEFINITIONS[object_id]
        state_topic = f"{self._base_topic}/{heater}/eta"
        payload: dict[str, Any] = {
            "name": f"{heater} {display_name}",
            "unique_id": f"temp_eta_{self._instance_slug}_{heater}_{object_id}",
            "state_topic": state_topic,
            "device": {
                "identifiers": [f"temp_eta_{self._instance_slug}"],
                "name": f"TempETA ({self._instance_slug})",
                "manufacturer": "OctoPrint",
                "model": "OctoPrint-TempETA",
                "sw_version": self._plugin_version,
            },
        }
        payload.update(extra_config)
        return payload

    def _publish_message(
        self,
        topic: str,
        payload: Any,
        retained: Optional[bool] = None,
    ) -> None:
        """Publish a message via the OctoPrint-MQTT helper (lock must be held).

        Dict payloads are passed as-is; the MQTT plugin serializes them to
        JSON. ``allow_queueing`` stays False on purpose: ETA values are
        per-second telemetry, delivering stale messages after a broker
        reconnect would actively mislead consumers.

        Args:
            topic: MQTT topic
            payload: Message payload (dict or string)
            retained: Override for the retain flag; defaults to the
                configured mqtt_retain setting
        """
        if self._mqtt_publish is None:
            return

        if retained is None:
            retained = self._retain

        try:
            result = self._mqtt_publish(
                topic,
                payload,
                retained=retained,
                qos=self._qos,
                allow_queueing=False,
            )
            if result is False:
                # OctoPrint-MQTT is not connected to the broker right now.
                self._logger.debug(
                    "MQTT publish skipped (broker not connected): topic=%s", topic
                )
        except Exception as e:  # pylint: disable=broad-except
            # Never let helper errors escape into the temperature broadcast
            # or settings-save paths.
            self._logger.debug("MQTT publish error: %s", str(e))
