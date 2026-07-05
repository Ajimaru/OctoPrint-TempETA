# Python API

Auto-generated Python API documentation for OctoPrint-TempETA.

## Main Plugin Class

::: octoprint_temp_eta.TempETAPlugin
    handler: python
    options:
        members_order: source
        show_source: true
        filters:
            - "!^_"

## Calculator Module

::: octoprint_temp_eta.calculator
        handler: python
        options:
            members_order: source
            show_source: true
            filters:
                - "!^_"

## MQTT Client Module

::: octoprint_temp_eta.mqtt_client.MQTTClientWrapper
        handler: python
        options:
            members_order: source
            show_source: true
            filters:
                - "!^_"

## Usage Examples

### Using the Calculator

```python
from octoprint_temp_eta.calculator import calculate_linear_eta, calculate_exponential_eta
from collections import deque
import time

# Create temperature history
history = deque()
for i in range(10):
    timestamp = time.time() + i
    temperature = 25 + i * 0.2  # small ramp
    target = 200.0
    history.append((timestamp, temperature, target))

# Calculate ETA using linear estimator
eta_seconds = calculate_linear_eta(history, target)
print(f"Linear ETA: {eta_seconds}")

# Calculate ETA using exponential estimator (fallbacks to linear if needed)
eta_exp = calculate_exponential_eta(history, target)
print(f"Exponential ETA: {eta_exp}")
```

### Using the MQTT Client

```python
from octoprint_temp_eta.mqtt_client import MQTTClientWrapper
import logging

# Create logger
logger = logging.getLogger(__name__)

# Instantiate wrapper (note: the wrapper expects a logger and plugin identifier)
mqtt_client = MQTTClientWrapper(logger, "temp_eta")

# Configure client via settings-like dict
mqtt_client.configure({
    "mqtt_enabled": True,
    "mqtt_broker_host": "localhost",
    "mqtt_broker_port": 1883,
    "mqtt_username": "",
    "mqtt_password": "",
    "mqtt_use_tls": False,
    "mqtt_base_topic": "octoprint/temp_eta",
    "mqtt_qos": 0,
    "mqtt_retain": False,
    "mqtt_publish_interval": 1.0,
})

# Publish a sample ETA update (heater name, eta seconds, eta kind, target, actual)
mqtt_client.publish_eta_update(
    heater="tool0",
    eta=120.0,
    eta_kind="heating",
    target=200.0,
    actual=50.0,
)

# Disconnect when done
mqtt_client.disconnect()
```

### Consuming ETA data from another plugin or client

The plugin does not expose a Python getter for current ETAs. Consume the data
through one of its public channels instead:

- **Plugin messages**: every update is broadcast via
  `send_plugin_message("temp_eta", payload)`; frontend components can listen
  in `onDataUpdaterPluginMessage` (see the [JavaScript API](javascript.md)).
- **MQTT**: enable the MQTT integration and subscribe to
  `{active_topic}/{heater}/eta` and `{active_topic}/{heater}/state_change`
  (see the README for payload formats).
- **Simple API**: `GET /api/plugin/temp_eta` returns the MQTT integration
  status; `POST` supports the `reset_profile_history` and
  `reset_settings_defaults` commands (admin only).

## Threading Considerations

The calculator functions are **pure and stateless** — they read the history
they are given and share no module state, so they are safe to call from any
thread as long as the caller does not mutate the passed history concurrently.
The plugin itself guards its history deques with an internal lock, and
`MQTTClientWrapper` serializes all its state behind its own lock.

## Error Handling

The estimators signal "no trustworthy estimate" by returning `None` rather
than raising:

```python
eta = calculate_linear_eta(history, target)
if eta is None:
    print("Insufficient data for ETA calculation")
else:
    print(f"ETA: {eta:.1f}s")
```

Invalid inputs (NaN/infinite targets, non-positive windows, malformed
samples) are filtered or rejected the same way; internal math errors in the
exponential fit degrade to the linear estimate instead of propagating.

## Type Hints

The public estimator signatures (from `octoprint_temp_eta/calculator.py`):

```python
from collections import deque
from typing import Optional

def calculate_linear_eta(
    history: deque, target: float, window_seconds: float = 10.0
) -> Optional[float]: ...

def calculate_exponential_eta(
    history: deque, target: float, window_seconds: float = 30.0
) -> Optional[float]: ...

def calculate_cooldown_linear_eta(
    cooldown_history: deque, goal_c: float, window_seconds: float = 60.0
) -> Optional[float]: ...

def calculate_cooldown_exponential_eta(
    cooldown_history: deque,
    ambient_c: float,
    goal_c: float,
    window_seconds: float = 60.0,
) -> Optional[float]: ...
```

Heating histories hold `(timestamp, actual_temp, target_temp)` tuples;
cooldown histories hold `(timestamp, actual_temp)` tuples.

## Logging

The plugin logs under the `octoprint_temp_eta` logger. Enable the
**Debug logging** setting to get verbose `[debug]`-prefixed messages (emitted
at info level so they show up without reconfiguring OctoPrint's logging).

## Next Steps

- [JavaScript API](javascript.md) - Frontend API reference
- [Algorithms](../architecture/algorithms.md) - ETA calculation details
- [Testing](../development/testing.md) - Unit tests and examples
