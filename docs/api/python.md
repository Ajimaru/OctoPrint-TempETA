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

### Plugin Integration

```python
import octoprint.plugin

class MyPlugin(octoprint.plugin.OctoPrintPlugin):
    def on_after_startup(self):
        # Access TempETA plugin
        temp_eta = self._plugin_manager.get_plugin("temp_eta")

        if temp_eta:
            # Get current ETA
            eta_data = temp_eta.get_current_eta()
            self._logger.info(f"Current ETA: {eta_data}")
```

## Threading Considerations

All public methods are thread-safe when accessed through the plugin instance. However, when using calculator or MQTT client directly, ensure proper synchronization:

```python
import threading

class SafeCalculator:
    def __init__(self):
        self._calculator = ETACalculator()
        self._lock = threading.RLock()

    def calculate(self, history, target):
        with self._lock:
            return self._calculator.calculate_eta(history, target)
```

## Error Handling

All methods handle errors gracefully and return `None` or default values on failure:

```python
try:
    eta = calculator.calculate_eta(history, target)
    if eta is None:
        print("Insufficient data for ETA calculation")
    else:
        print(f"ETA: {eta:.1f}s")
except Exception as e:
    logger.error(f"Calculation failed: {e}")
```

## Type Hints

The codebase uses Python type hints for better IDE support:

```python
from typing import Optional, Deque, Tuple

def calculate_eta(
    history: Deque[Tuple[float, float, float]],
    target: float
) -> Optional[float]:
    """
    Calculate ETA to target temperature.

    Args:
        history: Temperature history deque
        target: Target temperature

    Returns:
        ETA in seconds, or None if calculation fails
    """
    pass
```

## Logging

Use the provided logger for all log messages:

```python
self._logger.debug("Debug message")
self._logger.info("Info message")
self._logger.warning("Warning message")
self._logger.error("Error message")
self._logger.exception("Exception with traceback")
```

## Next Steps

- [JavaScript API](javascript.md) - Frontend API reference
- [Algorithms](../architecture/algorithms.md) - ETA calculation details
- [Testing](../development/testing.md) - Unit tests and examples
