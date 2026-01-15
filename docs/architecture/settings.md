# Settings Reference

Complete reference for all OctoPrint-TempETA configuration options.

## Configuration Structure

Settings are stored in OctoPrint's `config.yaml`:

```yaml
plugins:
  temp_eta:
    # ... settings here
```

## General Settings

### enabled

- **Type**: `boolean`
- **Default**: `true`
- **Description**: Enable/disable the plugin globally

```yaml
enabled: true
```

### algorithm

- **Type**: `string`
- **Default**: `"linear"`
- **Options**: `"linear"`, `"exponential"`
- **Description**: ETA calculation algorithm

```yaml
algorithm: "linear"
```

### update_interval

- **Type**: `float`
- **Default**: `1.0`
- **Range**: `0.5` - `5.0`
- **Unit**: seconds
- **Description**: How often to send updates to frontend

```yaml
update_interval: 1.0
```

### min_rate

- **Type**: `float`
- **Default**: `0.1`
- **Range**: `0.01` - `1.0`
- **Unit**: °C/s
- **Description**: Minimum temperature change rate to show ETA

```yaml
min_rate: 0.1
```

### max_eta

- **Type**: `integer`
- **Default**: `3600`
- **Range**: `60` - `7200`
- **Unit**: seconds
- **Description**: Maximum ETA to display (longer = "calculating")

```yaml
max_eta: 3600
```

## Heating ETA Settings

### heating_enabled

- **Type**: `boolean`
- **Default**: `true`
- **Description**: Show ETA for heating

```yaml
heating_enabled: true
```

### heating_threshold

- **Type**: `float`
- **Default**: `1.0`
- **Range**: `0.1` - `10.0`
- **Unit**: °C
- **Description**: Temperature difference to start showing ETA

```yaml
heating_threshold: 1.0
```

### heating_sound_enabled

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Play sound when heating completes

```yaml
heating_sound_enabled: false
```

### heating_sound_file

- **Type**: `string`
- **Default**: `"default"`
- **Description**: Sound file to play

```yaml
heating_sound_file: "default"
```

## Cool-down ETA Settings

### cooling_enabled

- **Type**: `boolean`
- **Default**: `true`
- **Description**: Show ETA for cooling

```yaml
cooling_enabled: true
```

### cooling_threshold

- **Type**: `float`
- **Default**: `1.0`
- **Range**: `0.1` - `10.0`
- **Unit**: °C
- **Description**: Temperature difference to start showing ETA

```yaml
cooling_threshold: 1.0
```

### cooling_sound_enabled

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Play sound when cooling completes

```yaml
cooling_sound_enabled: false
```

### cooling_sound_file

- **Type**: `string`
- **Default**: `"default"`
- **Description**: Sound file to play

```yaml
cooling_sound_file: "default"
```

## Display Settings

### show_in_graph

- **Type**: `boolean`
- **Default**: `true`
- **Description**: Show ETA in temperature graph

```yaml
show_in_graph: true
```

### show_in_sidebar

- **Type**: `boolean`
- **Default**: `true`
- **Description**: Show ETA in sidebar

```yaml
show_in_sidebar: true
```

### time_format

- **Type**: `string`
- **Default**: `"auto"`
- **Options**: `"auto"`, `"seconds"`, `"minutes"`, `"hours"`
- **Description**: ETA display format

```yaml
time_format: "auto"
```

## MQTT Settings

### mqtt_enabled

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Enable MQTT publishing

```yaml
mqtt_enabled: false
```

### mqtt_broker

- **Type**: `string`
- **Default**: `"localhost"`
- **Description**: MQTT broker hostname/IP

```yaml
mqtt_broker: "localhost"
```

### mqtt_port

- **Type**: `integer`
- **Default**: `1883`
- **Range**: `1` - `65535`
- **Description**: MQTT broker port

```yaml
mqtt_port: 1883
```

### mqtt_username

- **Type**: `string`
- **Default**: `""`
- **Description**: MQTT username (optional)

```yaml
mqtt_username: ""
```

### mqtt_password

- **Type**: `string`
- **Default**: `""`
- **Description**: MQTT password (optional)

```yaml
mqtt_password: ""
```

### mqtt_tls_enabled

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Use TLS/SSL for MQTT

```yaml
mqtt_tls_enabled: false
```

### mqtt_topic_prefix

- **Type**: `string`
- **Default**: `"octoprint/temp_eta"`
- **Description**: MQTT topic prefix

```yaml
mqtt_topic_prefix: "octoprint/temp_eta"
```

### mqtt_retain

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Set retain flag on MQTT messages

```yaml
mqtt_retain: false
```

### mqtt_qos

- **Type**: `integer`
- **Default**: `0`
- **Options**: `0`, `1`, `2`
- **Description**: MQTT quality of service level

```yaml
mqtt_qos: 0
```

## Advanced Settings

### history_max_age

- **Type**: `integer`
- **Default**: `60`
- **Range**: `10` - `300`
- **Unit**: seconds
- **Description**: Maximum age of history data

```yaml
history_max_age: 60
```

### history_max_samples

- **Type**: `integer`
- **Default**: `120`
- **Range**: `10` - `1000`
- **Description**: Maximum number of samples per heater

```yaml
history_max_samples: 120
```

### exponential_window

- **Type**: `integer`
- **Default**: `30`
- **Range**: `10` - `60`
- **Unit**: seconds
- **Description**: Time window for exponential fitting

```yaml
exponential_window: 30
```

### linear_window

- **Type**: `integer`
- **Default**: `10`
- **Range**: `5` - `30`
- **Unit**: seconds
- **Description**: Time window for linear calculation

```yaml
linear_window: 10
```

## Complete Example

```yaml
plugins:
  temp_eta:
    # General
    enabled: true
    algorithm: "linear"
    update_interval: 1.0
    min_rate: 0.1
    max_eta: 3600
    
    # Heating
    heating_enabled: true
    heating_threshold: 1.0
    heating_sound_enabled: false
    heating_sound_file: "default"
    
    # Cooling
    cooling_enabled: true
    cooling_threshold: 1.0
    cooling_sound_enabled: false
    cooling_sound_file: "default"
    
    # Display
    show_in_graph: true
    show_in_sidebar: true
    time_format: "auto"
    
    # MQTT
    mqtt_enabled: false
    mqtt_broker: "localhost"
    mqtt_port: 1883
    mqtt_username: ""
    mqtt_password: ""
    mqtt_tls_enabled: false
    mqtt_topic_prefix: "octoprint/temp_eta"
    mqtt_retain: false
    mqtt_qos: 0
    
    # Advanced
    history_max_age: 60
    history_max_samples: 120
    exponential_window: 30
    linear_window: 10
```

## Programmatic Access

### Python (Backend)

```python
# Get setting
algorithm = self._settings.get(["algorithm"])

# Set setting
self._settings.set(["algorithm"], "exponential")

# Save settings
self._settings.save()
```

### JavaScript (Frontend)

```javascript
// Get setting
var algorithm = self.settings.algorithm();

// Set setting
self.settings.algorithm("exponential");

// Save settings (triggers server update)
self.saveSettings();
```

## Validation

Settings are validated on save:

```python
def on_settings_save(self, data):
    # Validate algorithm
    if data.get("algorithm") not in ["linear", "exponential"]:
        raise ValueError("Invalid algorithm")
    
    # Validate ranges
    min_rate = data.get("min_rate", 0.1)
    if not 0.01 <= min_rate <= 1.0:
        raise ValueError("min_rate out of range")
    
    # ... more validation
    
    octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
```

## Migration

Settings are automatically migrated between versions:

```python
def get_settings_version(self):
    return 2

def on_settings_migrate(self, target, current):
    if current == 1:
        # Migrate from v1 to v2
        self._settings.set(["new_setting"], "default")
```

## Reset to Defaults

Via OctoPrint UI:

```
Settings → Temperature ETA → Reset to Defaults
```

Programmatically:

```python
self._settings.clean_all_data()
```

## Next Steps

- [Python API](../api/python.md) - Programmatic access
- [OctoPrint Integration](octoprint-integration.md) - Settings plugin implementation
- [Frontend Settings](../frontend/ui-placements.md) - Settings UI
