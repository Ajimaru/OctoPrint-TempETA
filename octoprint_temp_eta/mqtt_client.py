# coding=utf-8
"""MQTT client wrapper for Temperature ETA plugin.

Handles MQTT broker connection, reconnection, and message publishing with
configurable settings for broker details, authentication, and QoS.
"""

from __future__ import absolute_import

import json
import threading
import time
from typing import Any, Dict, Optional

try:
    import paho.mqtt.client as mqtt
except ImportError:  # pragma: no cover
    mqtt = None  # type: ignore


class MQTTClientWrapper:
    """Thread-safe MQTT client wrapper for the Temperature ETA plugin.

    Manages connection lifecycle, automatic reconnection, and message publishing.
    All MQTT operations are non-blocking to avoid impacting the temperature callback.
    """

    def __init__(self, logger: Any, identifier: str):
        """Initialize MQTT client wrapper.

        Args:
            logger: Logger instance for debug/info messages
            identifier: Plugin identifier for topic prefixes
        """
        self._logger = logger
        self._identifier = identifier
        self._lock = threading.Lock()

        self._client: Optional[Any] = None
        self._enabled = False
        self._connected = False
        self._connecting = False

        # Connection settings
        self._broker_host = ""
        self._broker_port = 1883
        self._username = ""
        self._password = ""
        self._use_tls = False
        self._tls_insecure = False

        # Publishing settings
        self._base_topic = "octoprint/temp_eta"
        self._qos = 0
        self._retain = False
        self._publish_interval = 1.0

        # State tracking for state transition events
        self._last_published_time = 0.0
        self._last_heater_state: Dict[str, Optional[str]] = {}

        # Connection retry logic
        self._last_connect_attempt = 0.0
        self._connect_retry_interval = 30.0

    def configure(self, settings: Dict[str, Any]) -> None:
        """Update MQTT configuration from plugin settings.

        Args:
            settings: Dictionary with MQTT configuration keys
        """
        with self._lock:
            old_enabled = self._enabled

            self._enabled = bool(settings.get("mqtt_enabled", False))
            self._broker_host = str(settings.get("mqtt_broker_host", "")).strip()
            self._broker_port = int(settings.get("mqtt_broker_port", 1883))
            self._username = str(settings.get("mqtt_username", "")).strip()
            self._password = str(settings.get("mqtt_password", "")).strip()
            self._use_tls = bool(settings.get("mqtt_use_tls", False))
            self._tls_insecure = bool(settings.get("mqtt_tls_insecure", False))

            self._base_topic = str(
                settings.get("mqtt_base_topic", "octoprint/temp_eta")
            ).strip()
            self._qos = int(settings.get("mqtt_qos", 0))
            self._retain = bool(settings.get("mqtt_retain", False))
            self._publish_interval = float(settings.get("mqtt_publish_interval", 1.0))

            # Reconnect if settings changed and enabled
            if self._enabled and (not old_enabled or not self._connected):
                self._schedule_connect()
            elif not self._enabled and old_enabled:
                self._disconnect_internal()

    def _schedule_connect(self) -> None:
        """Schedule a connection attempt (internal, lock must be held)."""
        if mqtt is None:
            self._logger.info("MQTT support disabled: paho-mqtt not available")
            return

        if not self._broker_host:
            return

        # Start connection in background thread to avoid blocking
        if not self._connecting and not self._connected:
            self._connecting = True
            thread = threading.Thread(target=self._connect_thread, daemon=True)
            thread.start()

    def _connect_thread(self) -> None:
        """Background thread for establishing MQTT connection."""
        try:
            if mqtt is None:
                return

            now = time.time()
            if (now - self._last_connect_attempt) < self._connect_retry_interval:
                return

            self._last_connect_attempt = now

            with self._lock:
                if self._client is not None:
                    try:
                        self._client.disconnect()
                    except Exception as e:
                        # Ignore disconnect errors during reconnect, but log for diagnostics.
                        self._logger.debug(
                            "Error while disconnecting existing MQTT client: %s", str(e)
                        )
                    self._client = None

                # Create MQTT client with version-specific API
                client_id = f"{self._identifier}_{int(now)}"
                kwargs: Dict[str, Any] = {"client_id": client_id}

                callback_api_version = getattr(mqtt, "CallbackAPIVersion", None)
                if callback_api_version is not None:
                    version2 = getattr(callback_api_version, "VERSION2", None)
                    if version2 is not None:
                        kwargs["callback_api_version"] = version2

                try:
                    self._client = mqtt.Client(**kwargs)
                except TypeError as e:
                    # Fall back to paho-mqtt 1.x API
                    self._logger.debug(
                        "Using paho-mqtt 1.x API (version 2 not available): %s", str(e)
                    )
                    self._client = mqtt.Client(client_id=client_id)

                self._client.on_connect = self._on_connect
                self._client.on_disconnect = self._on_disconnect

                if self._username:
                    self._client.username_pw_set(self._username, self._password)

                if self._use_tls:
                    import ssl

                    if self._tls_insecure:
                        # Skip certificate verification (not recommended for production)
                        self._client.tls_set(cert_reqs=ssl.CERT_NONE)
                        self._client.tls_insecure_set(True)
                    else:
                        # Use default certificate verification
                        self._client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

                broker_host = self._broker_host
                broker_port = self._broker_port

            self._logger.info("MQTT connecting to %s:%d", broker_host, broker_port)
            self._client.connect(broker_host, broker_port, keepalive=60)
            self._client.loop_start()

        except Exception as e:
            self._logger.error("MQTT connection failed: %s", str(e))
            with self._lock:
                self._connecting = False
                self._connected = False
                if self._client is not None:
                    try:
                        self._client.loop_stop()
                    except Exception as loop_error:
                        # Ignore loop_stop errors during cleanup, but log for diagnostics.
                        self._logger.debug(
                            "Error while stopping MQTT network loop after failure: %s",
                            str(loop_error),
                        )
                    self._client = None

    def _on_connect(
        self, client: Any, userdata: Any, flags: Dict[str, Any], rc: int
    ) -> None:
        """Callback when MQTT connection is established.

        Args:
            client: MQTT client instance
            userdata: User data (unused)
            flags: Connection flags
            rc: Result code (0 = success)
        """
        with self._lock:
            self._connecting = False
            if rc == 0:
                self._connected = True
                self._logger.info(
                    "MQTT connected to %s:%d", self._broker_host, self._broker_port
                )
            else:
                self._connected = False
                self._logger.error("MQTT connection failed with code %d", rc)

    def _on_disconnect(self, client: Any, userdata: Any, rc: int) -> None:
        """Callback when MQTT connection is lost.

        Args:
            client: MQTT client instance
            userdata: User data (unused)
            rc: Result code
        """
        with self._lock:
            self._connected = False
            self._connecting = False
            if rc != 0:
                self._logger.info("MQTT disconnected (code %d), will retry", rc)

    def _disconnect_internal(self) -> None:
        """Disconnect MQTT client (internal, lock must be held)."""
        if self._client is not None:
            try:
                self._client.loop_stop()
                self._client.disconnect()
            except Exception as e:
                # Do not raise during shutdown; log for diagnostics instead.
                self._logger.debug("Error while disconnecting MQTT client: %s", str(e))
            self._client = None
        self._connected = False
        self._connecting = False

    def disconnect(self) -> None:
        """Disconnect MQTT client gracefully."""
        with self._lock:
            self._disconnect_internal()

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
            if not self._enabled or not self._connected:
                return

            # Check if we should publish based on interval
            now = time.time()
            if (now - self._last_published_time) < self._publish_interval:
                return

            self._last_published_time = now

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

    def _publish_message(self, topic: str, payload: Dict[str, Any]) -> None:
        """Publish a message to MQTT broker (internal, lock must be held).

        Args:
            topic: MQTT topic
            payload: Message payload dictionary
        """
        if self._client is None or not self._connected:
            return

        try:
            json_payload = json.dumps(payload, ensure_ascii=False)
            result = self._client.publish(
                topic, json_payload, qos=self._qos, retain=self._retain
            )

            mqtt_err_success = 0
            if mqtt is not None:
                mqtt_err_success = int(getattr(mqtt, "MQTT_ERR_SUCCESS", 0))

            if result.rc != mqtt_err_success:
                self._logger.debug(
                    "MQTT publish failed: topic=%s rc=%d", topic, result.rc
                )
        except Exception as e:
            self._logger.debug("MQTT publish error: %s", str(e))

    def is_connected(self) -> bool:
        """Check if MQTT client is connected.

        Returns:
            bool: True if connected
        """
        with self._lock:
            return self._connected
