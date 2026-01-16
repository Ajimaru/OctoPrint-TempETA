# Python API

Auto-generated Python API documentation for OctoPrint-TempETA.

## Main Plugin Class

::: octoprint_temp_eta
    handler: python
    options:
      members_order: source
      show_source: true
      filters:
        - "!^_"
        - "!^__"

## Calculator Module

::: octoprint_temp_eta.calculator
    handler: python
    options:
      members_order: source
      show_source: true
      filters:
        - "!^_"

## MQTT Client Module

::: octoprint_temp_eta.mqtt_client
    handler: python
    options:
      members_order: source
      show_source: true
      filters:
        - "!^_"

## Usage Examples

### Using the Calculator

```python
from octoprint_temp_eta.calculator import ETACalculator
from collections import deque
import time

# Create calculator instance
calculator = ETACalculator(
    algorithm="linear",
    min_rate=0.1,
    max_eta=3600
)

# Create temperature history
history = deque()
for i in range(10):
    timestamp = time.time() + i
    temperature = 25 + i * 2  # Heating at 2°C/s
    target = 200
    history.append((timestamp, temperature, target))

# Calculate ETA
eta_seconds = calculator.calculate_eta(history, target)
print(f"ETA: {eta_seconds:.1f} seconds")
```

### Using the MQTT Client

```python
from octoprint_temp_eta.mqtt_client import MQTTClient
import logging

# Create logger
logger = logging.getLogger(__name__)

# Create MQTT client
mqtt_client = MQTTClient(
    broker="localhost",
    port=1883,
    username="user",
    password="pass",
    tls_enabled=False,
    logger=logger
)

# Connect
mqtt_client.connect()

# Publish ETA data
mqtt_client.publish_eta(
    heater="tool0",
    current=50.0,
    target=200.0,
    eta_seconds=120,
    rate=1.5
)

# Disconnect
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
