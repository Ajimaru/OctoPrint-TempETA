# Configuration Reference

Complete reference for all OctoPrint-TempETA configuration options.

This page provides the complete reference for plugin configuration. For implementation details, see [Settings Architecture](../architecture/settings.md).

## Configuration File

Settings are stored in OctoPrint's `config.yaml`:

**Location**: `~/.octoprint/config.yaml` (Linux/Mac) or `%APPDATA%\OctoPrint\config.yaml` (Windows)

```yaml
plugins:
  temp_eta:
    # Configuration here
```

## Complete Configuration Example

```yaml
plugins:
  temp_eta:
    # === General Settings ===
    enabled: true
    algorithm: "linear"
    update_interval: 1.0
    min_rate: 0.1
    max_eta: 3600
    
    # === Heating Settings ===
    heating_enabled: true
    heating_threshold: 1.0
    heating_sound_enabled: false
    heating_sound_file: "default"
    heating_notification_enabled: true
    
    # === Cooling Settings ===
    cooling_enabled: true
    cooling_threshold: 1.0
    cooling_sound_enabled: false
    cooling_sound_file: "default"
    cooling_notification_enabled: true
    
    # === Display Settings ===
    show_in_graph: true
    show_in_sidebar: true
    show_in_navbar: false
    time_format: "auto"
    show_rate: true
    show_percentage: false
    
    # === MQTT Settings ===
    mqtt_enabled: false
    mqtt_broker: "localhost"
    mqtt_port: 1883
    mqtt_username: ""
    mqtt_password: ""
    mqtt_tls_enabled: false
    mqtt_tls_insecure: false
    mqtt_ca_cert: ""
    mqtt_topic_prefix: "octoprint/temp_eta"
    mqtt_retain: false
    mqtt_qos: 0
    mqtt_keepalive: 60
    
    # === Advanced Settings ===
    history_max_age: 60
    history_max_samples: 120
    exponential_window: 30
    linear_window: 10
    exponential_max_tau: 300
    calculation_interval: 0.5
    cleanup_interval: 5.0
    debug_logging: false
```

## Setting Details

### enabled

Enable or disable the plugin globally.

- **Type**: Boolean
- **Default**: `true`
- **Example**: `enabled: false`

### algorithm

ETA calculation algorithm.

- **Type**: String
- **Default**: `"linear"`
- **Options**: `"linear"`, `"exponential"`
- **Example**: `algorithm: "exponential"`

**Linear**: Fast, simple, works well for constant heating.
**Exponential**: More accurate near target, requires more data.

### update_interval

How often to send UI updates (seconds).

- **Type**: Float
- **Default**: `1.0`
- **Range**: `0.5` - `5.0`
- **Example**: `update_interval: 2.0`

Lower values = more responsive, higher CPU usage.

### min_rate

Minimum temperature change rate to show ETA (°C/s).

- **Type**: Float
- **Default**: `0.1`
- **Range**: `0.01` - `1.0`
- **Example**: `min_rate: 0.05`

If rate is lower, ETA shows "stalled".

### max_eta

Maximum ETA to display (seconds).

- **Type**: Integer
- **Default**: `3600` (1 hour)
- **Range**: `60` - `7200`
- **Example**: `max_eta: 1800`

Longer ETAs show "calculating".

### heating_enabled

Show ETA for heating.

- **Type**: Boolean
- **Default**: `true`
- **Example**: `heating_enabled: false`

### heating_threshold

Temperature difference to start showing heating ETA (°C).

- **Type**: Float
- **Default**: `1.0`
- **Range**: `0.1` - `10.0`
- **Example**: `heating_threshold: 2.0`

Prevents showing ETA for tiny temperature changes.

### heating_sound_enabled

Play sound when heating completes.

- **Type**: Boolean
- **Default**: `false`
- **Example**: `heating_sound_enabled: true`

### heating_sound_file

Sound file to play on heating complete.

- **Type**: String
- **Default**: `"default"`
- **Example**: `heating_sound_file: "chime.mp3"`

Place custom sounds in `octoprint_temp_eta/static/sounds/`.

### cooling_enabled

Show ETA for cooling.

- **Type**: Boolean
- **Default**: `true`
- **Example**: `cooling_enabled: false`

### cooling_threshold

Temperature difference to start showing cooling ETA (°C).

- **Type**: Float
- **Default**: `1.0`
- **Range**: `0.1` - `10.0`
- **Example**: `cooling_threshold: 2.0`

### show_in_graph

Display ETA in temperature graph.

- **Type**: Boolean
- **Default**: `true`
- **Example**: `show_in_graph: false`

### show_in_sidebar

Display ETA in sidebar widget.

- **Type**: Boolean
- **Default**: `true`
- **Example**: `show_in_sidebar: false`

### time_format

ETA display format.

- **Type**: String
- **Default**: `"auto"`
- **Options**: `"auto"`, `"seconds"`, `"minutes"`, `"hours"`, `"hms"`
- **Example**: `time_format: "hms"`

- `auto`: Chooses best format based on time
- `seconds`: "90s"
- `minutes`: "1.5m"
- `hours`: "0.5h"
- `hms`: "01:30:00"

### show_rate

Show temperature change rate.

- **Type**: Boolean
- **Default**: `true`
- **Example**: `show_rate: false`

Displays rate like "+1.5°C/s".

### mqtt_enabled

Enable MQTT publishing.

- **Type**: Boolean
- **Default**: `false`
- **Example**: `mqtt_enabled: true`

### mqtt_broker

MQTT broker hostname or IP.

- **Type**: String
- **Default**: `"localhost"`
- **Example**: `mqtt_broker: "192.168.1.100"`

### mqtt_port

MQTT broker port.

- **Type**: Integer
- **Default**: `1883`
- **Range**: `1` - `65535`
- **Example**: `mqtt_port: 8883` (SSL/TLS)

### mqtt_username

MQTT username (optional).

- **Type**: String
- **Default**: `""`
- **Example**: `mqtt_username: "octoprint"`

### mqtt_password

MQTT password (optional).

- **Type**: String
- **Default**: `""`
- **Example**: `mqtt_password: "secret123"`

**Security**: Store securely, don't commit to git.

### mqtt_tls_enabled

Use TLS/SSL for MQTT.

- **Type**: Boolean
- **Default**: `false`
- **Example**: `mqtt_tls_enabled: true`

### mqtt_topic_prefix

MQTT topic prefix.

- **Type**: String
- **Default**: `"octoprint/temp_eta"`
- **Example**: `mqtt_topic_prefix: "3dprinter/eta"`

Full topics: `{prefix}/tool0`, `{prefix}/bed`, etc.

### mqtt_retain

Set retain flag on MQTT messages.

- **Type**: Boolean
- **Default**: `false`
- **Example**: `mqtt_retain: true`

Retained messages persist on broker.

### mqtt_qos

MQTT Quality of Service level.

- **Type**: Integer
- **Default**: `0`
- **Options**: `0`, `1`, `2`
- **Example**: `mqtt_qos: 1`

- `0`: At most once
- `1`: At least once
- `2`: Exactly once

### history_max_age

Maximum age of temperature history (seconds).

- **Type**: Integer
- **Default**: `60`
- **Range**: `10` - `300`
- **Example**: `history_max_age: 120`

Older data is automatically deleted.

### history_max_samples

Maximum number of samples per heater.

- **Type**: Integer
- **Default**: `120`
- **Range**: `10` - `1000`
- **Example**: `history_max_samples: 200`

Limits memory usage.

### exponential_window

Time window for exponential fitting (seconds).

- **Type**: Integer
- **Default**: `30`
- **Range**: `10` - `60`
- **Example**: `exponential_window: 45`

Only used with exponential algorithm.

### linear_window

Time window for linear calculation (seconds).

- **Type**: Integer
- **Default**: `10`
- **Range**: `5` - `30`
- **Example**: `linear_window: 15`

Only used with linear algorithm.

### debug_logging

Enable debug logging.

- **Type**: Boolean
- **Default**: `false`
- **Example**: `debug_logging: true`

Increases log verbosity. Useful for troubleshooting.

## Environment Variables

Some settings can be overridden via environment variables (for testing):

```bash
export OCTOPET_ALGORITHM=exponential
export OCTOPET_MIN_RATE=0.05
export OCTOPET_DEBUG=1
```

## Programmatic Access

### Python

```python
# Get setting
algorithm = self._settings.get(["algorithm"])

# Set setting
self._settings.set(["algorithm"], "exponential")

# Save
self._settings.save()
```

### REST API

```bash
# Get settings
curl http://octopi.local/api/settings

# Update settings
curl -X POST \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"plugins": {"temp_eta": {"algorithm": "exponential"}}}' \
  http://octopi.local/api/settings
```

## Validation

Settings are validated on save:

- Type checking
- Range validation
- Enum validation
- Cross-setting validation

Invalid settings are rejected with error message.

## Migration

Settings are automatically migrated between versions:

```python
def on_settings_migrate(self, target, current):
    if current < 2:
        # Migrate v1 to v2
        self._settings.set(["new_setting"], default_value)
```

## Backup

Backup configuration:

```bash
cp ~/.octoprint/config.yaml ~/.octoprint/config.yaml.backup
```

## Reset to Defaults

Via UI: Settings → Temperature ETA → Reset to Defaults

Via config file: Delete `plugins.temp_eta` section

Via API:

```bash
curl -X DELETE \
  -H "X-Api-Key: YOUR_KEY" \
  http://octopi.local/api/settings/plugins/temp_eta
```

## Next Steps

- [Settings Architecture](../architecture/settings.md) - Implementation details
- [OctoPrint Integration](../architecture/octoprint-integration.md) - Settings plugin
- [Python API](../api/python.md) - Programmatic access
