"""Unit tests for MQTT client wrapper.

Tests MQTT connection management, message publishing, and state transitions.
"""

from __future__ import annotations

import ssl
import time
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from octoprint_temp_eta.mqtt_client import MQTTClientWrapper


class DummyLogger:
    """Minimal logger test double collecting formatted messages."""

    def __init__(self) -> None:
        self.info_calls: list[str] = []
        self.warning_calls: list[str] = []
        self.error_calls: list[str] = []
        self.debug_calls: list[str] = []

    def info(self, msg: str, *args: Any) -> None:
        """Record an info log message for later assertions."""
        self.info_calls.append(msg % args if args else msg)

    def warning(self, msg: str, *args: Any) -> None:
        """Record a warning log message for later assertions."""
        self.warning_calls.append(msg % args if args else msg)

    def error(self, msg: str, *args: Any) -> None:
        """Record an error log message for later assertions."""
        self.error_calls.append(msg % args if args else msg)

    def debug(self, msg: str, *args: Any) -> None:
        """Record a debug log message for later assertions."""
        self.debug_calls.append(msg % args if args else msg)


class MQTTClientWrapperHarness(MQTTClientWrapper):
    """MQTT wrapper variant exposing controlled helpers for tests."""

    def set_internal_state(self, **values: Any) -> None:
        """Set wrapper internals through a dedicated test-only helper."""
        for name, value in values.items():
            setattr(self, f"_{name}", value)

    def get_internal_state(self, name: str) -> Any:
        """Read wrapper internals through a dedicated test-only helper."""
        return getattr(self, f"_{name}")

    def get_heater_state(self, heater: str) -> str | None:
        """Return tracked state for a heater."""
        return self._last_heater_state.get(heater)

    def schedule_connect_locked(self) -> None:
        """Run scheduling path while holding the wrapper lock."""
        with self._lock:
            self._schedule_connect()

    def run_connect_thread(self) -> None:
        """Execute the internal connect thread body synchronously."""
        self._connect_thread()

    def run_on_connect(self, rc: int) -> None:
        """Invoke the connect callback with minimal dummy arguments."""
        self._on_connect(client=None, userdata=None, flags={}, rc=rc)

    def run_on_disconnect(self, rc: int) -> None:
        """Invoke the disconnect callback with minimal dummy arguments."""
        self._on_disconnect(client=None, userdata=None, rc=rc)

    def publish_message(self, topic: str, payload: dict[str, Any]) -> None:
        """Invoke internal publish logic through a test helper."""
        self._publish_message(topic, payload)


@pytest.fixture(name="test_logger")
def fixture_test_logger() -> DummyLogger:
    """Create a dummy logger for testing."""
    return DummyLogger()


@pytest.fixture(name="wrapper")
def fixture_wrapper(test_logger: DummyLogger) -> MQTTClientWrapperHarness:
    """Create a testable MQTT wrapper instance."""
    return MQTTClientWrapperHarness(test_logger, "temp_eta")


def test_mqtt_wrapper_initialization(wrapper: MQTTClientWrapperHarness) -> None:
    """Test MQTT wrapper initializes with correct defaults."""
    assert wrapper is not None
    assert not wrapper.is_connected()
    assert wrapper.get_internal_state("enabled") is False
    assert wrapper.get_internal_state("broker_host") == ""
    assert wrapper.get_internal_state("broker_port") == 1883
    assert wrapper.get_internal_state("base_topic") == "octoprint/temp_eta"
    assert wrapper.get_internal_state("qos") == 0
    assert wrapper.get_internal_state("retain") is False


def test_mqtt_configure_disabled(wrapper: MQTTClientWrapperHarness) -> None:
    """Test configuring MQTT when disabled."""
    settings = {
        "mqtt_enabled": False,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
    }
    wrapper.configure(settings)
    assert not wrapper.get_internal_state("enabled")
    assert not wrapper.is_connected()


def test_mqtt_configure_enabled_no_host(wrapper: MQTTClientWrapperHarness) -> None:
    """Test configuring MQTT when enabled but no host provided."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "",
        "mqtt_broker_port": 1883,
    }
    wrapper.configure(settings)
    assert wrapper.get_internal_state("enabled")
    assert not wrapper.is_connected()


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_configure_enabled_with_host(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """Test configuring MQTT with valid host triggers connection."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.MQTT_ERR_SUCCESS = 0

    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
        "mqtt_username": "",
        "mqtt_password": "",
        "mqtt_use_tls": False,
        "mqtt_tls_insecure": False,
        "mqtt_base_topic": "octoprint/temp_eta",
        "mqtt_qos": 0,
        "mqtt_retain": False,
        "mqtt_publish_interval": 1.0,
    }

    wrapper.configure(settings)
    time.sleep(0.1)

    assert wrapper.get_internal_state("enabled")
    assert wrapper.get_internal_state("broker_host") == "test-broker"


def test_mqtt_publish_eta_update_disabled(
    wrapper: MQTTClientWrapperHarness, test_logger: DummyLogger
) -> None:
    """Test publishing ETA update when MQTT is disabled."""
    wrapper.set_internal_state(enabled=False, connected=False)

    wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    assert len(test_logger.error_calls) == 0


def test_mqtt_publish_eta_update_not_connected(
    wrapper: MQTTClientWrapperHarness, test_logger: DummyLogger
) -> None:
    """Test publishing ETA update when not connected."""
    wrapper.set_internal_state(enabled=True, connected=False)

    wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    assert len(test_logger.error_calls) == 0


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_eta_update_connected(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """Test publishing ETA update when connected."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.MQTT_ERR_SUCCESS = 0

    wrapper.set_internal_state(
        enabled=True,
        connected=True,
        client=mock_client,
        base_topic="test/topic",
        qos=0,
        retain=False,
    )

    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    assert mock_client.publish.called


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_state_transition_detection(
    mock_mqtt: Mock,
    wrapper: MQTTClientWrapperHarness,
    test_logger: DummyLogger,
) -> None:
    """Test state transition detection and event publishing."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.MQTT_ERR_SUCCESS = 0

    wrapper.set_internal_state(
        enabled=True,
        connected=True,
        client=mock_client,
        base_topic="test/topic",
        last_published_time=0.0,
    )

    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    wrapper.set_internal_state(last_published_time=0.0)
    wrapper.publish_eta_update(
        heater="bed", eta=115.0, eta_kind="heating", target=60.0, actual=42.0
    )

    wrapper.set_internal_state(last_published_time=0.0)
    wrapper.publish_eta_update(
        heater="bed", eta=None, eta_kind=None, target=60.0, actual=60.0
    )

    assert any("state changed" in call for call in test_logger.info_calls)


def test_mqtt_disconnect(wrapper: MQTTClientWrapperHarness) -> None:
    """Test MQTT disconnect functionality."""
    mock_client = MagicMock()
    wrapper.set_internal_state(client=mock_client, connected=True)

    wrapper.disconnect()

    assert mock_client.loop_stop.called
    assert mock_client.disconnect.called
    assert not wrapper.get_internal_state("connected")


def test_mqtt_publish_interval_throttling(wrapper: MQTTClientWrapperHarness) -> None:
    """Test publish interval throttling."""
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    wrapper.set_internal_state(
        enabled=True,
        connected=True,
        client=mock_client,
        publish_interval=1.0,
        last_published_time=time.time(),
    )

    wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    assert not mock_client.publish.called


def test_mqtt_qos_levels(wrapper: MQTTClientWrapperHarness) -> None:
    """Test QoS level configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
        "mqtt_qos": 2,
        "mqtt_retain": True,
        "mqtt_publish_interval": 0.5,
    }

    wrapper.configure(settings)

    assert wrapper.get_internal_state("qos") == 2
    assert wrapper.get_internal_state("retain") is True
    assert wrapper.get_internal_state("publish_interval") == 0.5


def test_mqtt_tls_configuration(wrapper: MQTTClientWrapperHarness) -> None:
    """Test TLS/SSL configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 8883,
        "mqtt_use_tls": True,
        "mqtt_tls_insecure": True,
    }

    wrapper.configure(settings)

    assert wrapper.get_internal_state("use_tls") is True
    assert wrapper.get_internal_state("tls_insecure") is True


def test_mqtt_authentication_configuration(
    wrapper: MQTTClientWrapperHarness,
) -> None:
    """Test authentication configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
        "mqtt_username": "testuser",
        "mqtt_password": "testpass",
    }

    wrapper.configure(settings)

    assert wrapper.get_internal_state("username") == "testuser"
    assert wrapper.get_internal_state("password") == "testpass"


def test_mqtt_base_topic_configuration(wrapper: MQTTClientWrapperHarness) -> None:
    """Test base topic configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
        "mqtt_base_topic": "custom/topic/path",
    }

    wrapper.configure(settings)

    assert wrapper.get_internal_state("base_topic") == "custom/topic/path"


def test_mqtt_schedule_connect_logs_when_mqtt_unavailable(
    wrapper: MQTTClientWrapperHarness, test_logger: DummyLogger
) -> None:
    """Schedule connect should log and return if paho-mqtt isn't available."""
    wrapper.set_internal_state(enabled=True, broker_host="example")

    with patch("octoprint_temp_eta.mqtt_client.mqtt", None):
        wrapper.schedule_connect_locked()

    assert any("MQTT support disabled" in msg for msg in test_logger.warning_calls)


def test_mqtt_connect_thread_respects_retry_interval(
    wrapper: MQTTClientWrapperHarness,
) -> None:
    """Connect thread should early-return when inside retry interval."""
    wrapper.set_internal_state(connect_retry_interval=30.0)

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        wrapper.set_internal_state(last_connect_attempt=80.0)
        wrapper.run_connect_thread()

    assert wrapper.get_internal_state("client") is None
    assert wrapper.get_internal_state("connected") is False


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_falls_back_to_paho_v1_api(
    mock_mqtt: Mock,
    wrapper: MQTTClientWrapperHarness,
    test_logger: DummyLogger,
) -> None:
    """If paho-mqtt 2.x callback API isn't available, wrapper should fall back."""
    mock_client = MagicMock()

    def client_factory(*_args: Any, **kwargs: Any) -> Any:
        """Raise once for callback API usage, then return mock client."""
        if "callback_api_version" in kwargs:
            raise TypeError("no callback API")
        return mock_client

    mock_mqtt.Client.side_effect = client_factory
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    wrapper.set_internal_state(
        enabled=True,
        broker_host="broker",
        broker_port=1883,
        connect_retry_interval=0.0,
        last_connect_attempt=0.0,
    )

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        wrapper.run_connect_thread()

    assert any("Using paho-mqtt 1.x API" in msg for msg in test_logger.debug_calls)
    assert mock_client.connect.called
    assert mock_client.loop_start.called


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_tls_insecure(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """TLS insecure mode should disable certificate verification."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    wrapper.set_internal_state(
        enabled=True,
        broker_host="broker",
        broker_port=8883,
        use_tls=True,
        tls_insecure=True,
        connect_retry_interval=0.0,
    )

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        wrapper.run_connect_thread()

    mock_client.tls_set.assert_called_with(cert_reqs=ssl.CERT_NONE)
    mock_client.tls_insecure_set.assert_called_with(True)


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_tls_secure(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """TLS secure mode should require certificate verification."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    wrapper.set_internal_state(
        enabled=True,
        broker_host="broker",
        broker_port=8883,
        use_tls=True,
        tls_insecure=False,
        connect_retry_interval=0.0,
    )

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        wrapper.run_connect_thread()

    mock_client.tls_set.assert_called_with(cert_reqs=ssl.CERT_REQUIRED)


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_handles_connect_error(
    mock_mqtt: Mock,
    wrapper: MQTTClientWrapperHarness,
    test_logger: DummyLogger,
) -> None:
    """Connection errors should be logged and internal state reset."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()
    mock_client.connect.side_effect = RuntimeError("boom")

    wrapper.set_internal_state(
        enabled=True,
        broker_host="broker",
        broker_port=1883,
        connect_retry_interval=0.0,
        connecting=True,
    )

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        wrapper.run_connect_thread()

    assert any("MQTT connection failed" in msg for msg in test_logger.error_calls)
    assert wrapper.get_internal_state("connected") is False
    assert wrapper.get_internal_state("connecting") is False
    assert wrapper.get_internal_state("client") is None


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_message_logs_failure_rc(
    mock_mqtt: Mock,
    wrapper: MQTTClientWrapperHarness,
    test_logger: DummyLogger,
) -> None:
    """Non-success publish rc should produce a debug log."""
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.rc = 7
    mock_client.publish.return_value = mock_result
    mock_mqtt.MQTT_ERR_SUCCESS = 0

    wrapper.set_internal_state(enabled=True, connected=True, client=mock_client)

    wrapper.publish_message("topic", {"k": "v"})
    assert any("MQTT publish failed" in msg for msg in test_logger.debug_calls)


def test_mqtt_publish_message_logs_exception(
    wrapper: MQTTClientWrapperHarness, test_logger: DummyLogger
) -> None:
    """Publish exceptions should be caught and logged at debug level."""
    mock_client = MagicMock()
    mock_client.publish.side_effect = RuntimeError("boom")

    wrapper.set_internal_state(enabled=True, connected=True, client=mock_client)

    wrapper.publish_message("topic", {"k": "v"})
    assert any("MQTT publish error" in msg for msg in test_logger.debug_calls)


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_eta_update_sets_cooled_down_state(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """Cooldown target proximity should set cooled_down state and publish events."""
    mock_client = MagicMock()
    mock_mqtt.MQTT_ERR_SUCCESS = 0
    wrapper.set_internal_state(
        enabled=True,
        connected=True,
        client=mock_client,
        base_topic="test/topic",
        last_published_time=0.0,
        publish_interval=0.0,
    )

    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    wrapper.publish_eta_update(
        heater="bed",
        eta=None,
        eta_kind=None,
        target=0.0,
        actual=20.2,
        cooldown_target=20.0,
    )

    assert wrapper.get_heater_state("bed") == "cooled_down"
    assert mock_client.publish.call_count >= 2


def test_mqtt_configure_disabling_disconnects_existing_client(
    wrapper: MQTTClientWrapperHarness,
) -> None:
    """Disabling MQTT should disconnect an existing client."""
    mock_client = MagicMock()
    wrapper.set_internal_state(enabled=True, connected=True, client=mock_client)

    wrapper.configure({"mqtt_enabled": False})

    assert mock_client.loop_stop.called
    assert mock_client.disconnect.called
    assert wrapper.get_internal_state("client") is None
    assert wrapper.get_internal_state("connected") is False


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_disconnects_existing_client(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """Connect thread should disconnect an existing client before reconnecting."""
    old_client = MagicMock()
    new_client = MagicMock()
    mock_mqtt.Client.return_value = new_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    wrapper.set_internal_state(
        enabled=True,
        broker_host="broker",
        broker_port=1883,
        client=old_client,
        connect_retry_interval=0.0,
    )

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        wrapper.run_connect_thread()

    assert old_client.disconnect.called
    assert wrapper.get_internal_state("client") is new_client


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_cleanup_ignores_loop_stop_errors(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """Loop-stop failures during error cleanup should be swallowed."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()
    mock_client.connect.side_effect = RuntimeError("boom")
    mock_client.loop_stop.side_effect = RuntimeError("loop stop boom")

    wrapper.set_internal_state(
        enabled=True,
        broker_host="broker",
        broker_port=1883,
        connect_retry_interval=0.0,
    )

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        wrapper.run_connect_thread()

    assert wrapper.get_internal_state("client") is None


def test_mqtt_on_connect_sets_connected_and_logs(test_logger: DummyLogger) -> None:
    """_on_connect should update internal state for success and failure."""
    wrapper = MQTTClientWrapperHarness(test_logger, "temp_eta")
    wrapper.set_internal_state(broker_host="broker", broker_port=1883, connecting=True)

    wrapper.run_on_connect(rc=0)
    assert wrapper.is_connected() is True
    assert any("MQTT connected" in msg for msg in test_logger.info_calls)

    wrapper.run_on_connect(rc=1)
    assert wrapper.is_connected() is False
    assert any(
        "MQTT connection failed with code" in msg for msg in test_logger.error_calls
    )


def test_mqtt_on_disconnect_logs_retry(test_logger: DummyLogger) -> None:
    """_on_disconnect should log when rc indicates an unexpected disconnect."""
    wrapper = MQTTClientWrapperHarness(test_logger, "temp_eta")
    wrapper.set_internal_state(connected=True, connecting=True)

    wrapper.run_on_disconnect(rc=1)
    assert wrapper.is_connected() is False
    assert any("will retry" in msg for msg in test_logger.info_calls)


def test_mqtt_disconnect_internal_ignores_exceptions(
    wrapper: MQTTClientWrapperHarness,
) -> None:
    """Disconnect should swallow client API errors and reset state."""
    mock_client = MagicMock()
    mock_client.loop_stop.side_effect = RuntimeError("boom")
    mock_client.disconnect.side_effect = RuntimeError("boom")

    wrapper.set_internal_state(client=mock_client, connected=True)

    wrapper.disconnect()
    assert wrapper.get_internal_state("client") is None
    assert wrapper.get_internal_state("connected") is False


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_eta_update_sets_cooling_state(
    mock_mqtt: Mock, wrapper: MQTTClientWrapperHarness
) -> None:
    """Cooling ETA updates should set cooling state."""
    mock_client = MagicMock()
    mock_mqtt.MQTT_ERR_SUCCESS = 0
    wrapper.set_internal_state(
        enabled=True,
        connected=True,
        client=mock_client,
        base_topic="test/topic",
        last_published_time=0.0,
        publish_interval=0.0,
    )

    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    wrapper.publish_eta_update(
        heater="bed",
        eta=30.0,
        eta_kind="cooling",
        target=0.0,
        actual=50.0,
        cooldown_target=None,
    )

    assert wrapper.get_heater_state("bed") == "cooling"


def test_mqtt_publish_message_returns_when_not_connected(
    wrapper: MQTTClientWrapperHarness,
) -> None:
    """_publish_message should no-op if there is no client or no connection."""
    wrapper.set_internal_state(connected=False, client=None)
    wrapper.publish_message("topic", {"k": "v"})
