"""Unit tests for the MQTT publisher.

Tests delegation to the OctoPrint-MQTT plugin helper, topic building,
publish throttling, state transitions, and Home Assistant autodiscovery.
"""

from __future__ import annotations

import time
from typing import Any
from unittest.mock import Mock

import pytest

from octoprint_temp_eta.mqtt_publisher import MqttPublisher


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


class MqttPublisherHarness(MqttPublisher):
    """Publisher variant exposing controlled helpers for tests."""

    def set_internal_state(self, **values: Any) -> None:
        """Set publisher internals through a dedicated test-only helper."""
        for name, value in values.items():
            setattr(self, f"_{name}", value)

    def get_internal_state(self, name: str) -> Any:
        """Read publisher internals through a dedicated test-only helper."""
        return getattr(self, f"_{name}")

    def get_heater_state(self, heater: str) -> str | None:
        """Return tracked state for a heater."""
        return self._last_heater_state.get(heater)


class FakePluginManager:
    """plugin_manager test double serving configurable helpers."""

    def __init__(self, helpers: Any) -> None:
        self._helpers = helpers
        self.requested: list[tuple[Any, ...]] = []

    def get_helpers(self, *args: Any) -> Any:
        """Record the request and return the configured helpers."""
        self.requested.append(args)
        return self._helpers


@pytest.fixture(name="test_logger")
def fixture_test_logger() -> DummyLogger:
    """Create a dummy logger for testing."""
    return DummyLogger()


@pytest.fixture(name="publisher")
def fixture_publisher(test_logger: DummyLogger) -> MqttPublisherHarness:
    """Create a testable MQTT publisher instance."""
    return MqttPublisherHarness(test_logger, plugin_version="1.2.3")


@pytest.fixture(name="fake_publish")
def fixture_fake_publish() -> Mock:
    """Create a fake mqtt_publish helper reporting success."""
    return Mock(return_value=True)


def _connect(
    publisher: MqttPublisherHarness, fake_publish: Mock, **settings: Any
) -> None:
    """Wire the fake helper into the publisher and configure it enabled."""
    publisher.set_internal_state(mqtt_publish=fake_publish)
    config: dict[str, Any] = {
        "mqtt_enabled": True,
        "mqtt_base_topic": "octoprint/temp_eta",
        "mqtt_use_appearance_name": False,
        "mqtt_appearance_name": "",
        "mqtt_custom_identifier": "",
        "mqtt_qos": 0,
        "mqtt_retain": False,
        "mqtt_publish_interval": 0.0,
    }
    config.update(settings)
    publisher.configure(config)


# ---------------------------------------------------------------- lifecycle


def test_initialization_defaults(publisher: MqttPublisherHarness) -> None:
    """Publisher initializes disabled without a helper."""
    assert publisher.is_mqtt_plugin_available() is False
    assert publisher.is_operational() is False
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta"


def test_initialize_acquires_helper(
    publisher: MqttPublisherHarness, fake_publish: Mock, test_logger: DummyLogger
) -> None:
    """initialize() acquires the mqtt_publish helper when available."""
    manager = FakePluginManager({"mqtt_publish": fake_publish})

    publisher.initialize(manager)

    assert publisher.is_mqtt_plugin_available() is True
    assert manager.requested == [("mqtt", "mqtt_publish")]
    assert any("available" in msg for msg in test_logger.info_calls)


@pytest.mark.parametrize("helpers", [None, {}, {"other": object()}])
def test_initialize_without_helper(
    publisher: MqttPublisherHarness, test_logger: DummyLogger, helpers: Any
) -> None:
    """initialize() tolerates a missing MQTT plugin."""
    publisher.initialize(FakePluginManager(helpers))

    assert publisher.is_mqtt_plugin_available() is False
    assert any("not available" in msg for msg in test_logger.info_calls)


def test_initialize_survives_helper_query_error(
    publisher: MqttPublisherHarness,
) -> None:
    """initialize() never raises when get_helpers is broken."""
    manager = Mock()
    manager.get_helpers.side_effect = AttributeError("boom")

    publisher.initialize(manager)

    assert publisher.is_mqtt_plugin_available() is False


def test_is_operational_requires_helper_and_enabled(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """is_operational() is True only with helper present and enabled."""
    assert publisher.is_operational() is False

    _connect(publisher, fake_publish)
    assert publisher.is_operational() is True

    publisher.configure({"mqtt_enabled": False})
    assert publisher.is_operational() is False
    assert publisher.is_mqtt_plugin_available() is True


# ---------------------------------------------------------------- configure


def test_configure_reads_settings(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """configure() applies publishing settings."""
    _connect(
        publisher,
        fake_publish,
        mqtt_qos=2,
        mqtt_retain=True,
        mqtt_publish_interval=5.0,
        mqtt_discovery_enabled=True,
        mqtt_discovery_prefix="ha/",
    )

    assert publisher.get_internal_state("qos") == 2
    assert publisher.get_internal_state("retain") is True
    assert publisher.get_internal_state("publish_interval") == 5.0
    assert publisher.get_internal_state("discovery_enabled") is True
    assert publisher.get_internal_state("discovery_prefix") == "ha"


def test_configure_tolerates_invalid_numeric_settings(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """configure() falls back to defaults for garbage numeric values."""
    _connect(
        publisher,
        fake_publish,
        mqtt_qos="not-a-number",
        mqtt_publish_interval=float("inf"),
    )

    assert publisher.get_internal_state("qos") == 0
    assert publisher.get_internal_state("publish_interval") == 1.0


def test_configure_clamps_numeric_settings(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """configure() clamps qos and interval into their valid ranges."""
    _connect(publisher, fake_publish, mqtt_qos=7, mqtt_publish_interval=99999.0)

    assert publisher.get_internal_state("qos") == 2
    assert publisher.get_internal_state("publish_interval") == 3600.0


# ------------------------------------------------------------ topic building


def test_topic_default_base(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Empty base topic falls back to the default."""
    _connect(publisher, fake_publish, mqtt_base_topic="")
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta"


def test_topic_strips_trailing_slash(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Trailing slashes on the base topic are stripped."""
    _connect(publisher, fake_publish, mqtt_base_topic="my/topic/")
    assert publisher.get_internal_state("base_topic") == "my/topic"


def test_topic_appends_appearance_name(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Appearance name is appended as topic suffix when enabled."""
    _connect(
        publisher,
        fake_publish,
        mqtt_use_appearance_name=True,
        mqtt_appearance_name="My Printer",
    )
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta/My Printer"


def test_topic_falls_back_to_custom_identifier(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Custom identifier is used when appearance name is disabled."""
    _connect(
        publisher,
        fake_publish,
        mqtt_use_appearance_name=False,
        mqtt_appearance_name="My Printer",
        mqtt_custom_identifier="printer1",
    )
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta/printer1"


def test_topic_falls_back_when_appearance_name_missing(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Custom identifier is used when the appearance name is empty."""
    _connect(
        publisher,
        fake_publish,
        mqtt_use_appearance_name=True,
        mqtt_appearance_name="",
        mqtt_custom_identifier="printer1",
    )
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta/printer1"


def test_topic_no_suffix(publisher: MqttPublisherHarness, fake_publish: Mock) -> None:
    """No suffix is appended without appearance name or identifier."""
    _connect(publisher, fake_publish)
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta"


def test_topic_sanitizes_wildcards_and_slashes(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Wildcards and surrounding slashes are removed from suffixes."""
    _connect(
        publisher,
        fake_publish,
        mqtt_use_appearance_name=True,
        mqtt_appearance_name="/my+printer#1/",
    )
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta/myprinter1"


def test_topic_suffix_only_wildcards_yields_no_suffix(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """A suffix consisting only of wildcards is dropped entirely."""
    _connect(
        publisher,
        fake_publish,
        mqtt_use_appearance_name=True,
        mqtt_appearance_name="+#",
    )
    assert publisher.get_internal_state("base_topic") == "octoprint/temp_eta"


def test_instance_slug_from_appearance_name(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Discovery instance slug is derived from the appearance name."""
    _connect(
        publisher,
        fake_publish,
        mqtt_use_appearance_name=True,
        mqtt_appearance_name="My Printer #1",
    )
    assert publisher.get_internal_state("instance_slug") == "my_printer_1"


def test_instance_slug_default(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Discovery instance slug falls back to a generic default."""
    _connect(publisher, fake_publish)
    assert publisher.get_internal_state("instance_slug") == "octoprint"


# ------------------------------------------------------------------ publish


def test_publish_eta_update_disabled(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """No publish happens when MQTT is disabled."""
    _connect(publisher, fake_publish, mqtt_enabled=False)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)

    fake_publish.assert_not_called()


def test_publish_eta_update_without_helper(
    publisher: MqttPublisherHarness,
) -> None:
    """No publish (and no error) happens when the helper is missing."""
    publisher.configure({"mqtt_enabled": True})

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)

    assert publisher.get_heater_state("bed") is None


def test_publish_eta_update_delegates_to_helper(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """ETA updates are published via the helper with the raw dict payload."""
    _connect(publisher, fake_publish, mqtt_qos=1, mqtt_retain=True)

    publisher.publish_eta_update(
        heater="bed",
        eta=42.5,
        eta_kind="heating",
        target=60.0,
        actual=30.0,
        cooldown_target=None,
    )

    topics = [call.args[0] for call in fake_publish.call_args_list]
    assert "octoprint/temp_eta/bed/eta" in topics
    eta_call = fake_publish.call_args_list[topics.index("octoprint/temp_eta/bed/eta")]
    payload = eta_call.args[1]
    assert isinstance(payload, dict)
    assert payload["heater"] == "bed"
    assert payload["eta_seconds"] == 42.5
    assert payload["eta_kind"] == "heating"
    assert payload["target"] == 60.0
    assert payload["actual"] == 30.0
    assert payload["state"] == "heating"
    assert eta_call.kwargs["retained"] is True
    assert eta_call.kwargs["qos"] == 1
    assert eta_call.kwargs["allow_queueing"] is False


def test_publish_state_transition_event(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """State changes publish an additional state_change event."""
    _connect(publisher, fake_publish)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)
    publisher.publish_eta_update("bed", None, None, 60.0, 59.5)

    topics = [call.args[0] for call in fake_publish.call_args_list]
    assert topics.count("octoprint/temp_eta/bed/state_change") == 2
    last_event = fake_publish.call_args_list[-1].args[1]
    assert last_event["state"] == "at_target"
    assert last_event["previous_state"] == "heating"
    assert publisher.get_heater_state("bed") == "at_target"


def test_publish_no_state_event_when_unchanged(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """No state_change event is published when the state stays the same."""
    _connect(publisher, fake_publish)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)
    publisher.publish_eta_update("bed", 41.0, "heating", 60.0, 31.0)

    topics = [call.args[0] for call in fake_publish.call_args_list]
    assert topics.count("octoprint/temp_eta/bed/state_change") == 1


def test_publish_cooled_down_state(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Cooldown completion is detected as cooled_down state."""
    _connect(publisher, fake_publish)

    publisher.publish_eta_update("bed", 100.0, "cooling", 0.0, 60.0, 25.0)
    publisher.publish_eta_update("bed", None, None, 0.0, 25.2, 25.0)

    assert publisher.get_heater_state("bed") == "cooled_down"


def test_publish_interval_throttling(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Publishes are throttled per publish interval."""
    _connect(publisher, fake_publish, mqtt_publish_interval=100.0)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)
    publisher.publish_eta_update("bed", 41.0, "heating", 60.0, 31.0)

    eta_topics = [
        call.args[0]
        for call in fake_publish.call_args_list
        if call.args[0].endswith("/eta")
    ]
    assert eta_topics == ["octoprint/temp_eta/bed/eta"]


def test_publish_interval_is_tracked_per_heater(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """One heater's publish never consumes another heater's slot."""
    _connect(publisher, fake_publish, mqtt_publish_interval=100.0)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)
    publisher.publish_eta_update("tool0", 21.0, "heating", 200.0, 100.0)

    eta_topics = [
        call.args[0]
        for call in fake_publish.call_args_list
        if call.args[0].endswith("/eta")
    ]
    assert eta_topics == [
        "octoprint/temp_eta/bed/eta",
        "octoprint/temp_eta/tool0/eta",
    ]


def test_publish_interval_expiry_allows_next_publish(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """A publish goes through again after the interval expired."""
    _connect(publisher, fake_publish, mqtt_publish_interval=100.0)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)
    publisher.set_internal_state(last_published_time={"bed": time.time() - 101.0})
    publisher.publish_eta_update("bed", 41.0, "heating", 60.0, 31.0)

    eta_topics = [
        call.args[0]
        for call in fake_publish.call_args_list
        if call.args[0].endswith("/eta")
    ]
    assert len(eta_topics) == 2


def test_publish_helper_returning_false_logs_debug(
    publisher: MqttPublisherHarness, test_logger: DummyLogger
) -> None:
    """A helper returning False (broker offline) is logged at debug."""
    fake_publish = Mock(return_value=False)
    _connect(publisher, fake_publish)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)

    assert any("not connected" in msg for msg in test_logger.debug_calls)


def test_publish_helper_exception_is_swallowed(
    publisher: MqttPublisherHarness, test_logger: DummyLogger
) -> None:
    """Helper errors never escape into the caller."""
    fake_publish = Mock(side_effect=RuntimeError("boom"))
    _connect(publisher, fake_publish)

    publisher.publish_eta_update("bed", 42.0, "heating", 60.0, 30.0)

    assert any("MQTT publish error" in msg for msg in test_logger.debug_calls)


# ---------------------------------------------------------------- discovery


def test_publish_discovery(publisher: MqttPublisherHarness, fake_publish: Mock) -> None:
    """Discovery configs are published retained for every heater/sensor."""
    _connect(
        publisher,
        fake_publish,
        mqtt_use_appearance_name=True,
        mqtt_appearance_name="My Printer",
        mqtt_discovery_enabled=True,
    )

    publisher.publish_discovery(["tool0", "bed"])

    calls = fake_publish.call_args_list
    assert len(calls) == 2 * len(MqttPublisher.SENSOR_DEFINITIONS)
    topics = [call.args[0] for call in calls]
    assert "homeassistant/sensor/temp_eta_my_printer/bed_eta_seconds/config" in topics
    for call in calls:
        assert call.kwargs["retained"] is True
        payload = call.args[1]
        assert payload["state_topic"].startswith("octoprint/temp_eta/My Printer/")
        assert payload["device"]["identifiers"] == ["temp_eta_my_printer"]
        assert payload["device"]["sw_version"] == "1.2.3"
        assert payload["unique_id"].startswith("temp_eta_my_printer_")


def test_publish_discovery_requires_enabled_and_discovery(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Discovery is a no-op when disabled or discovery is off."""
    _connect(publisher, fake_publish, mqtt_discovery_enabled=False)
    publisher.publish_discovery(["bed"])
    fake_publish.assert_not_called()

    _connect(publisher, fake_publish, mqtt_enabled=False, mqtt_discovery_enabled=True)
    publisher.publish_discovery(["bed"])
    fake_publish.assert_not_called()


def test_clear_retained_topics_uses_last_identity(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Clearing publishes empty retained payloads on the OLD topics."""
    _connect(
        publisher,
        fake_publish,
        mqtt_custom_identifier="old_name",
        mqtt_discovery_enabled=True,
    )
    publisher.publish_discovery(["bed"])
    fake_publish.reset_mock()

    # Identity changes, then discovery is cleared: old topics must be used.
    _connect(
        publisher,
        fake_publish,
        mqtt_custom_identifier="new_name",
        mqtt_discovery_enabled=True,
    )
    publisher.clear_retained_topics()

    assert fake_publish.call_count == len(MqttPublisher.SENSOR_DEFINITIONS)
    for call in fake_publish.call_args_list:
        assert "temp_eta_old_name" in call.args[0]
        assert call.args[1] == ""
        assert call.kwargs["retained"] is True

    # Second clear is a no-op (identity consumed).
    fake_publish.reset_mock()
    publisher.clear_retained_topics()
    fake_publish.assert_not_called()


def test_clear_retained_topics_noop_without_discovery(
    publisher: MqttPublisherHarness, fake_publish: Mock
) -> None:
    """Clearing without previously published discovery is a no-op."""
    _connect(publisher, fake_publish)

    publisher.clear_retained_topics()

    fake_publish.assert_not_called()
