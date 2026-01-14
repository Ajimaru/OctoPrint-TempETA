"""Unit tests for MQTT client wrapper.

Tests MQTT connection management, message publishing, and state transitions.
"""

from __future__ import annotations

import time
from typing import Any, List
from unittest.mock import MagicMock, Mock, patch

import pytest

from octoprint_temp_eta.mqtt_client import MQTTClientWrapper


class DummyLogger:
    def __init__(self) -> None:
        self.info_calls: List[str] = []
        self.warning_calls: List[str] = []
        self.error_calls: List[str] = []
        self.debug_calls: List[str] = []

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.info_calls.append(msg % args if args else msg)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.warning_calls.append(msg % args if args else msg)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.error_calls.append(msg % args if args else msg)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.debug_calls.append(msg % args if args else msg)


@pytest.fixture
def logger() -> DummyLogger:
    """Create a dummy logger for testing."""
    return DummyLogger()


@pytest.fixture
def mqtt_wrapper(logger: DummyLogger) -> MQTTClientWrapper:
    """Create an MQTT wrapper instance."""
    return MQTTClientWrapper(logger, "temp_eta")


def test_mqtt_wrapper_initialization(mqtt_wrapper: MQTTClientWrapper) -> None:
    """Test MQTT wrapper initializes with correct defaults."""
    assert mqtt_wrapper is not None
    assert not mqtt_wrapper.is_connected()
    assert mqtt_wrapper._enabled is False
    assert mqtt_wrapper._broker_host == ""
    assert mqtt_wrapper._broker_port == 1883
    assert mqtt_wrapper._base_topic == "octoprint/temp_eta"
    assert mqtt_wrapper._qos == 0
    assert mqtt_wrapper._retain is False


def test_mqtt_configure_disabled(mqtt_wrapper: MQTTClientWrapper) -> None:
    """Test configuring MQTT when disabled."""
    settings = {
        "mqtt_enabled": False,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
    }
    mqtt_wrapper.configure(settings)
    assert not mqtt_wrapper._enabled
    assert not mqtt_wrapper.is_connected()


def test_mqtt_configure_enabled_no_host(
    mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Test configuring MQTT when enabled but no host provided."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "",
        "mqtt_broker_port": 1883,
    }
    mqtt_wrapper.configure(settings)
    assert mqtt_wrapper._enabled
    # Should not attempt connection without host
    assert not mqtt_wrapper.is_connected()


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_configure_enabled_with_host(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
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

    mqtt_wrapper.configure(settings)

    # Brief sleep to allow background thread to start (connection is async)
    # This is necessary because the actual MQTT connection happens in a daemon thread
    time.sleep(0.1)

    # Verify connection attempt was initiated
    assert mqtt_wrapper._enabled
    assert mqtt_wrapper._broker_host == "test-broker"


def test_mqtt_publish_eta_update_disabled(
    mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Test publishing ETA update when MQTT is disabled."""
    mqtt_wrapper._enabled = False
    mqtt_wrapper._connected = False

    mqtt_wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    # Should not log any errors or attempts
    assert len(logger.error_calls) == 0


def test_mqtt_publish_eta_update_not_connected(
    mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Test publishing ETA update when not connected."""
    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = False

    mqtt_wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    # Should not attempt to publish
    assert len(logger.error_calls) == 0


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_eta_update_connected(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Test publishing ETA update when connected."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.MQTT_ERR_SUCCESS = 0

    # Set up wrapper as connected
    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client
    mqtt_wrapper._base_topic = "test/topic"
    mqtt_wrapper._qos = 0
    mqtt_wrapper._retain = False

    # Mock successful publish
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    mqtt_wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    # Verify publish was called
    assert mock_client.publish.called


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_state_transition_detection(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Test state transition detection and event publishing."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.MQTT_ERR_SUCCESS = 0

    # Set up wrapper as connected
    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client
    mqtt_wrapper._base_topic = "test/topic"
    mqtt_wrapper._last_published_time = 0.0

    # Mock successful publish
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    # First call - should detect heating state
    mqtt_wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    # Second call with same state - should not publish state change
    mqtt_wrapper._last_published_time = 0.0  # Reset to allow publish
    mqtt_wrapper.publish_eta_update(
        heater="bed", eta=115.0, eta_kind="heating", target=60.0, actual=42.0
    )

    # Third call with different state - should publish state change
    mqtt_wrapper._last_published_time = 0.0  # Reset to allow publish
    mqtt_wrapper.publish_eta_update(
        heater="bed", eta=None, eta_kind=None, target=60.0, actual=60.0
    )

    # Verify state transitions were logged
    assert any("state changed" in call for call in logger.info_calls)


def test_mqtt_disconnect(mqtt_wrapper: MQTTClientWrapper) -> None:
    """Test MQTT disconnect functionality."""
    mock_client = MagicMock()
    mqtt_wrapper._client = mock_client
    mqtt_wrapper._connected = True

    mqtt_wrapper.disconnect()

    assert mock_client.loop_stop.called
    assert mock_client.disconnect.called
    assert not mqtt_wrapper._connected


def test_mqtt_publish_interval_throttling(
    mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Test publish interval throttling."""
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client
    mqtt_wrapper._publish_interval = 1.0
    mqtt_wrapper._last_published_time = time.time()

    # Try to publish immediately after setting last publish time
    mqtt_wrapper.publish_eta_update(
        heater="bed", eta=120.0, eta_kind="heating", target=60.0, actual=40.0
    )

    # Should not publish due to throttling
    assert not mock_client.publish.called


def test_mqtt_qos_levels(mqtt_wrapper: MQTTClientWrapper) -> None:
    """Test QoS level configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
        "mqtt_qos": 2,
        "mqtt_retain": True,
        "mqtt_publish_interval": 0.5,
    }

    mqtt_wrapper.configure(settings)

    assert mqtt_wrapper._qos == 2
    assert mqtt_wrapper._retain is True
    assert mqtt_wrapper._publish_interval == 0.5


def test_mqtt_tls_configuration(mqtt_wrapper: MQTTClientWrapper) -> None:
    """Test TLS/SSL configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 8883,
        "mqtt_use_tls": True,
        "mqtt_tls_insecure": True,
    }

    mqtt_wrapper.configure(settings)

    assert mqtt_wrapper._use_tls is True
    assert mqtt_wrapper._tls_insecure is True


def test_mqtt_authentication_configuration(mqtt_wrapper: MQTTClientWrapper) -> None:
    """Test authentication configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
        "mqtt_username": "testuser",
        "mqtt_password": "testpass",
    }

    mqtt_wrapper.configure(settings)

    assert mqtt_wrapper._username == "testuser"
    assert mqtt_wrapper._password == "testpass"


def test_mqtt_base_topic_configuration(mqtt_wrapper: MQTTClientWrapper) -> None:
    """Test base topic configuration."""
    settings = {
        "mqtt_enabled": True,
        "mqtt_broker_host": "test-broker",
        "mqtt_broker_port": 1883,
        "mqtt_base_topic": "custom/topic/path",
    }

    mqtt_wrapper.configure(settings)

    assert mqtt_wrapper._base_topic == "custom/topic/path"


def test_mqtt_schedule_connect_logs_when_mqtt_unavailable(
    mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Schedule connect should log and return if paho-mqtt isn't available."""
    mqtt_wrapper._enabled = True
    mqtt_wrapper._broker_host = "example"

    with patch("octoprint_temp_eta.mqtt_client.mqtt", None):
        with mqtt_wrapper._lock:
            mqtt_wrapper._schedule_connect()

    assert any("MQTT support disabled" in msg for msg in logger.warning_calls)


def test_mqtt_connect_thread_respects_retry_interval(
    mqtt_wrapper: MQTTClientWrapper,
) -> None:
    """Connect thread should early-return when inside retry interval."""
    mqtt_wrapper._connect_retry_interval = 30.0

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        mqtt_wrapper._last_connect_attempt = 80.0
        mqtt_wrapper._connect_thread()

    # No side effects expected (still not connecting/connected)
    assert mqtt_wrapper._client is None
    assert mqtt_wrapper._connected is False


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_falls_back_to_paho_v1_api(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """If paho-mqtt 2.x callback API isn't available, wrapper should fall back."""
    mock_client = MagicMock()

    def _client_factory(*_args: Any, **kwargs: Any) -> Any:
        if "callback_api_version" in kwargs:
            raise TypeError("no callback API")
        return mock_client

    mock_mqtt.Client.side_effect = _client_factory
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    mqtt_wrapper._enabled = True
    mqtt_wrapper._broker_host = "broker"
    mqtt_wrapper._broker_port = 1883
    mqtt_wrapper._connect_retry_interval = 0.0
    mqtt_wrapper._last_connect_attempt = 0.0

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        mqtt_wrapper._connect_thread()

    assert any("Using paho-mqtt 1.x API" in msg for msg in logger.debug_calls)
    assert mock_client.connect.called
    assert mock_client.loop_start.called


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_tls_insecure(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper
) -> None:
    """TLS insecure mode should disable certificate verification."""
    import ssl

    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    mqtt_wrapper._enabled = True
    mqtt_wrapper._broker_host = "broker"
    mqtt_wrapper._broker_port = 8883
    mqtt_wrapper._use_tls = True
    mqtt_wrapper._tls_insecure = True
    mqtt_wrapper._connect_retry_interval = 0.0

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        mqtt_wrapper._connect_thread()

    mock_client.tls_set.assert_called_with(cert_reqs=ssl.CERT_NONE)
    mock_client.tls_insecure_set.assert_called_with(True)


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_tls_secure(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper
) -> None:
    """TLS secure mode should require certificate verification."""
    import ssl

    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    mqtt_wrapper._enabled = True
    mqtt_wrapper._broker_host = "broker"
    mqtt_wrapper._broker_port = 8883
    mqtt_wrapper._use_tls = True
    mqtt_wrapper._tls_insecure = False
    mqtt_wrapper._connect_retry_interval = 0.0

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        mqtt_wrapper._connect_thread()

    mock_client.tls_set.assert_called_with(cert_reqs=ssl.CERT_REQUIRED)


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_handles_connect_error(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Connection errors should be logged and internal state reset."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()
    mock_client.connect.side_effect = RuntimeError("boom")

    mqtt_wrapper._enabled = True
    mqtt_wrapper._broker_host = "broker"
    mqtt_wrapper._broker_port = 1883
    mqtt_wrapper._connect_retry_interval = 0.0
    mqtt_wrapper._connecting = True

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        mqtt_wrapper._connect_thread()

    assert any("MQTT connection failed" in msg for msg in logger.error_calls)
    assert mqtt_wrapper._connected is False
    assert mqtt_wrapper._connecting is False
    assert mqtt_wrapper._client is None


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_message_logs_failure_rc(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Non-success publish rc should produce a debug log."""
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.rc = 7
    mock_client.publish.return_value = mock_result
    mock_mqtt.MQTT_ERR_SUCCESS = 0

    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client

    mqtt_wrapper._publish_message("topic", {"k": "v"})
    assert any("MQTT publish failed" in msg for msg in logger.debug_calls)


def test_mqtt_publish_message_logs_exception(
    mqtt_wrapper: MQTTClientWrapper, logger: DummyLogger
) -> None:
    """Publish exceptions should be caught and logged at debug level."""
    mock_client = MagicMock()
    mock_client.publish.side_effect = RuntimeError("boom")

    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client

    mqtt_wrapper._publish_message("topic", {"k": "v"})
    assert any("MQTT publish error" in msg for msg in logger.debug_calls)


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_eta_update_sets_cooled_down_state(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper
) -> None:
    """Cooldown target proximity should set cooled_down state and publish events."""
    mock_client = MagicMock()
    mock_mqtt.MQTT_ERR_SUCCESS = 0
    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client
    mqtt_wrapper._base_topic = "test/topic"
    mqtt_wrapper._last_published_time = 0.0
    mqtt_wrapper._publish_interval = 0.0

    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    mqtt_wrapper.publish_eta_update(
        heater="bed",
        eta=None,
        eta_kind=None,
        target=0.0,
        actual=20.2,
        cooldown_target=20.0,
    )

    assert mqtt_wrapper._last_heater_state.get("bed") == "cooled_down"
    assert mock_client.publish.call_count >= 2


def test_mqtt_configure_disabling_disconnects_existing_client(
    mqtt_wrapper: MQTTClientWrapper,
) -> None:
    """Disabling MQTT should disconnect an existing client."""
    mock_client = MagicMock()
    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client

    mqtt_wrapper.configure({"mqtt_enabled": False})

    assert mock_client.loop_stop.called
    assert mock_client.disconnect.called
    assert mqtt_wrapper._client is None
    assert mqtt_wrapper._connected is False


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_disconnects_existing_client(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper
) -> None:
    """Connect thread should disconnect an existing client before reconnecting."""
    old_client = MagicMock()
    new_client = MagicMock()
    mock_mqtt.Client.return_value = new_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()

    mqtt_wrapper._enabled = True
    mqtt_wrapper._broker_host = "broker"
    mqtt_wrapper._broker_port = 1883
    mqtt_wrapper._client = old_client
    mqtt_wrapper._connect_retry_interval = 0.0

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        mqtt_wrapper._connect_thread()

    assert old_client.disconnect.called
    assert mqtt_wrapper._client is new_client


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_connect_thread_cleanup_ignores_loop_stop_errors(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper
) -> None:
    """Loop-stop failures during error cleanup should be swallowed."""
    mock_client = MagicMock()
    mock_mqtt.Client.return_value = mock_client
    mock_mqtt.CallbackAPIVersion.VERSION2 = object()
    mock_client.connect.side_effect = RuntimeError("boom")
    mock_client.loop_stop.side_effect = RuntimeError("loop stop boom")

    mqtt_wrapper._enabled = True
    mqtt_wrapper._broker_host = "broker"
    mqtt_wrapper._broker_port = 1883
    mqtt_wrapper._connect_retry_interval = 0.0

    with patch("octoprint_temp_eta.mqtt_client.time.time", lambda: 100.0):
        mqtt_wrapper._connect_thread()

    assert mqtt_wrapper._client is None


def test_mqtt_on_connect_sets_connected_and_logs(logger: DummyLogger) -> None:
    """_on_connect should update internal state for success and failure."""
    wrapper = MQTTClientWrapper(logger, "temp_eta")
    wrapper._broker_host = "broker"
    wrapper._broker_port = 1883
    wrapper._connecting = True

    wrapper._on_connect(client=None, userdata=None, flags={}, rc=0)
    assert wrapper.is_connected() is True
    assert any("MQTT connected" in msg for msg in logger.info_calls)

    wrapper._on_connect(client=None, userdata=None, flags={}, rc=1)
    assert wrapper.is_connected() is False
    assert any("MQTT connection failed with code" in msg for msg in logger.error_calls)


def test_mqtt_on_disconnect_logs_retry(logger: DummyLogger) -> None:
    """_on_disconnect should log when rc indicates an unexpected disconnect."""
    wrapper = MQTTClientWrapper(logger, "temp_eta")
    wrapper._connected = True
    wrapper._connecting = True

    wrapper._on_disconnect(client=None, userdata=None, rc=1)
    assert wrapper.is_connected() is False
    assert any("will retry" in msg for msg in logger.info_calls)


def test_mqtt_disconnect_internal_ignores_exceptions(
    mqtt_wrapper: MQTTClientWrapper,
) -> None:
    """Disconnect should swallow client API errors and reset state."""
    mock_client = MagicMock()
    mock_client.loop_stop.side_effect = RuntimeError("boom")
    mock_client.disconnect.side_effect = RuntimeError("boom")

    mqtt_wrapper._client = mock_client
    mqtt_wrapper._connected = True

    mqtt_wrapper.disconnect()
    assert mqtt_wrapper._client is None
    assert mqtt_wrapper._connected is False


@patch("octoprint_temp_eta.mqtt_client.mqtt")
def test_mqtt_publish_eta_update_sets_cooling_state(
    mock_mqtt: Mock, mqtt_wrapper: MQTTClientWrapper
) -> None:
    """Cooling ETA updates should set cooling state."""
    mock_client = MagicMock()
    mock_mqtt.MQTT_ERR_SUCCESS = 0
    mqtt_wrapper._enabled = True
    mqtt_wrapper._connected = True
    mqtt_wrapper._client = mock_client
    mqtt_wrapper._base_topic = "test/topic"
    mqtt_wrapper._last_published_time = 0.0
    mqtt_wrapper._publish_interval = 0.0

    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    mqtt_wrapper.publish_eta_update(
        heater="bed",
        eta=30.0,
        eta_kind="cooling",
        target=0.0,
        actual=50.0,
        cooldown_target=None,
    )

    assert mqtt_wrapper._last_heater_state.get("bed") == "cooling"


def test_mqtt_publish_message_returns_when_not_connected(
    mqtt_wrapper: MQTTClientWrapper,
) -> None:
    """_publish_message should no-op if there is no client or no connection."""
    mqtt_wrapper._connected = False
    mqtt_wrapper._client = None
    mqtt_wrapper._publish_message("topic", {"k": "v"})
