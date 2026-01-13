"""Unit tests for MQTT client wrapper.

Tests MQTT connection management, message publishing, and state transitions.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock, patch

import pytest

from octoprint_temp_eta.mqtt_client import MQTTClientWrapper


class DummyLogger:
    def __init__(self) -> None:
        self.info_calls: List[str] = []
        self.error_calls: List[str] = []
        self.debug_calls: List[str] = []

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.info_calls.append(msg % args if args else msg)

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
