# Configuration Reference

Complete reference for all OctoPrint-TempETA configuration options.

Every key below exists in the plugin's `get_settings_defaults()` in
`octoprint_temp_eta/__init__.py`. Values posted through the settings UI are
additionally sanitized server-side (`_sanitize_settings_payload`), so
out-of-range values are clamped and unparsable values fall back to a safe
default. For implementation details see
[Settings Architecture](../architecture/settings.md).

## Configuration File

Settings are stored in OctoPrint's `config.yaml`:

**Location**: `~/.octoprint/config.yaml` (Linux/macOS) or `%APPDATA%\OctoPrint\config.yaml` (Windows)

Only keys that differ from the defaults are written to the file:

```yaml
plugins:
  temp_eta:
    algorithm: exponential
    threshold_start: 10.0
```

## Complete Configuration Example

All keys with their default values:

```yaml
plugins:
  temp_eta:
    # === General ===
    enabled: true
    enable_heating_eta: true
    suppress_while_printing: false
    show_in_sidebar: true
    show_in_navbar: true
    show_in_tab: true
    show_progress_bars: true
    show_historical_graph: true
    historical_graph_window_seconds: 180
    temp_display: octoprint # octoprint | c | cf
    threshold_unit: octoprint # octoprint | c | f
    threshold_start: 5.0 # delta in °C
    algorithm: linear # linear | exponential
    update_interval: 1.0
    history_size: 60
    debug_logging: false

    # === Status colors ===
    color_mode: bands # bands | status
    color_heating: "#5cb85c"
    color_cooling: "#337ab7"
    color_idle: "#777777"

    # === Sound alerts ===
    sound_enabled: false
    sound_target_reached: false
    sound_cooldown_finished: false
    sound_volume: 0.5
    sound_min_interval_s: 10.0

    # === Browser notifications ===
    notification_enabled: false
    notification_target_reached: false
    notification_cooldown_finished: false
    notification_timeout_s: 6.0
    notification_min_interval_s: 10.0

    # === Cool-down ETA ===
    enable_cooldown_eta: true
    cooldown_mode: threshold # threshold | ambient
    cooldown_target_tool0: 50.0
    cooldown_target_bed: 40.0
    cooldown_target_chamber: 30.0
    cooldown_ambient_temp: null # optional fixed ambient (°C)
    cooldown_hysteresis_c: 1.0
    cooldown_fit_window_seconds: 120

    # === MQTT ===
    mqtt_enabled: false
    mqtt_broker_host: ""
    mqtt_broker_port: 1883
    mqtt_username: ""
    mqtt_password: ""
    mqtt_use_tls: false
    mqtt_tls_insecure: false
    mqtt_base_topic: octoprint/temp_eta
    mqtt_use_appearance_name: true
    mqtt_custom_identifier: ""
    mqtt_qos: 0
    mqtt_retain: false
    mqtt_publish_interval: 1.0

    # === Persistence (advanced, config.yaml only) ===
    persist_backoff_reset_s: 30.0
    persist_backoff_initial_s: 60.0
    persist_backoff_max_s: 300.0
    persist_max_json_bytes: 262144
```

## General Settings

### enabled

Master switch for the plugin. When disabled, no history is recorded and all
UI placements are hidden.

- **Type**: Boolean — **Default**: `true`

### enable_heating_eta

Compute and show heating ETAs. Cool-down ETAs are controlled separately by
`enable_cooldown_eta`.

- **Type**: Boolean — **Default**: `true`

### suppress_while_printing

Hide ETAs while OctoPrint considers a print job active (printing, paused,
pausing, resuming). Useful to keep the UI focused on the pre-print heat-up.

- **Type**: Boolean — **Default**: `false`

### show_in_sidebar / show_in_navbar / show_in_tab

Independently enable each UI placement.

- **Type**: Boolean — **Default**: `true` (each)

### show_progress_bars

Show progress-to-target bars in the sidebar and tab views.

- **Type**: Boolean — **Default**: `true`

### show_historical_graph

Show the per-heater temperature history chart in the tab's history sub-tab.

- **Type**: Boolean — **Default**: `true`

### historical_graph_window_seconds

Time window of the history chart.

- **Type**: Integer — **Default**: `180` — **Range**: `30` – `1800`

### temp_display

How temperatures are formatted in the plugin's UI.

- **Type**: String — **Default**: `"octoprint"`
- **Options**: `"octoprint"` (follow OctoPrint's appearance setting), `"c"`
  (Celsius only), `"cf"` (Celsius + Fahrenheit)

### threshold_unit

Unit in which the heating threshold is entered in the settings dialog. The
stored `threshold_start` value is always °C.

- **Type**: String — **Default**: `"octoprint"`
- **Options**: `"octoprint"`, `"c"`, `"f"`

### threshold_start

Temperature delta (°C) below the target at which the heating countdown
starts. Larger values start the countdown earlier and give the estimator more
ramp data, which stabilizes the estimate.

- **Type**: Float — **Default**: `5.0` — **Range**: `1.0` – `50.0`

### algorithm

Heating ETA algorithm; see [Algorithms](../architecture/algorithms.md).

- **Type**: String — **Default**: `"linear"` — **Options**: `"linear"`, `"exponential"`

### update_interval

Minimum seconds between frontend/MQTT update rounds. `0` is accepted at
runtime and means "update on every temperature callback" (~2 Hz).

- **Type**: Float — **Default**: `1.0` — **UI range**: `0.1` – `5.0`

### history_size

Number of temperature samples kept per heater (heating and cooldown
histories each use this bound).

- **Type**: Integer — **Default**: `60` — **Range**: `10` – `300`

### debug_logging

Verbose `[debug]`-prefixed log output (emitted at info level so it appears
in `octoprint.log` without logging reconfiguration). Also enables throttled
`console.debug` output in the browser.

- **Type**: Boolean — **Default**: `false`

## Status Colors

### color_mode

- **Type**: String — **Default**: `"bands"`
- **Options**: `"bands"` (color by remaining time: warning under 60 s, info
  under 300 s), `"status"` (fixed colors per heating/cooling/idle state)

### color_heating / color_cooling / color_idle

CSS colors used in `status` mode (and for the history chart line).

- **Type**: String — **Defaults**: `#5cb85c` / `#337ab7` / `#777777`

## Sound Alerts

### sound_enabled

Master switch for sound alerts.

- **Type**: Boolean — **Default**: `false`

### sound_target_reached / sound_cooldown_finished

Per-event switches.

- **Type**: Boolean — **Default**: `false` (each)

### sound_volume

- **Type**: Float — **Default**: `0.5` — **Range**: `0.0` – `1.0`

### sound_min_interval_s

Minimum seconds between sounds per heater+event (rate limit).

- **Type**: Float — **Default**: `10.0` — **Range**: `0.0` – `300.0`

## Browser Notifications

### notification_enabled

Master switch for browser toast notifications.

- **Type**: Boolean — **Default**: `false`

### notification_target_reached / notification_cooldown_finished

Per-event switches.

- **Type**: Boolean — **Default**: `false` (each)

### notification_timeout_s

How long a toast stays visible.

- **Type**: Float — **Default**: `6.0` — **Range**: `1.0` – `60.0`

### notification_min_interval_s

Minimum seconds between toasts per heater+event (rate limit).

- **Type**: Float — **Default**: `10.0` — **Range**: `0.0` – `300.0`

## Cool-down ETA

### enable_cooldown_eta

Compute and show cool-down ETAs when a heater's target is switched off.

- **Type**: Boolean — **Default**: `true`

### cooldown_mode

- **Type**: String — **Default**: `"threshold"`
- **Options**: `"threshold"` (countdown to a fixed per-heater temperature),
  `"ambient"` (countdown until near ambient temperature)

### cooldown_target_tool0 / cooldown_target_bed / cooldown_target_chamber

Fixed goal temperatures (°C) for threshold mode. The tool value applies to
all tools.

- **Type**: Float — **Defaults**: `50.0` / `40.0` / `30.0`
- **Ranges**: `0` – `400` / `0` – `200` / `0` – `100`

### cooldown_ambient_temp

Optional fixed ambient temperature (°C) for ambient mode. When unset (`null`),
the plugin learns a per-heater baseline from the lowest temperature observed
while the heater is off.

- **Type**: Float or `null` — **Default**: `null` — **Accepted range**: `0` – `80`

### cooldown_hysteresis_c

Band (°C) above the goal at which the cool-down ETA disappears; in ambient
mode this is also the "near ambient" margin.

- **Type**: Float — **Default**: `1.0` — **Range**: `0.1` – `20.0`

### cooldown_fit_window_seconds

Time window of cooldown samples used for the fit.

- **Type**: Integer — **Default**: `120` — **Range**: `10` – `1800`

## MQTT

See the README for topic layout and payload formats.

### mqtt_enabled

- **Type**: Boolean — **Default**: `false`

### mqtt_broker_host

Hostname or IP of the broker. MQTT stays disconnected while empty.

- **Type**: String — **Default**: `""`

### mqtt_broker_port

- **Type**: Integer — **Default**: `1883` — **Range**: `1` – `65535`

### mqtt_username / mqtt_password

Optional authentication. Leave empty for anonymous access.

- **Type**: String — **Default**: `""` (each)

### mqtt_use_tls / mqtt_tls_insecure

Enable TLS; `mqtt_tls_insecure` skips certificate verification (self-signed
certificates — not recommended for production).

- **Type**: Boolean — **Default**: `false` (each)

### mqtt_base_topic

Root topic for all publishes.

- **Type**: String — **Default**: `"octoprint/temp_eta"`

### mqtt_use_appearance_name

Append OctoPrint's appearance name (Appearance → Title) as a topic suffix so
multiple OctoPrint instances don't collide.

- **Type**: Boolean — **Default**: `true`

### mqtt_custom_identifier

Manual topic suffix, used when `mqtt_use_appearance_name` is off or no
appearance name is configured. Wildcard characters (`+`, `#`) and slashes at
the edges are stripped.

- **Type**: String — **Default**: `""`

### mqtt_qos

- **Type**: Integer — **Default**: `0` — **Options**: `0` (at most once), `1` (at least once), `2` (exactly once)

### mqtt_retain

- **Type**: Boolean — **Default**: `false`

### mqtt_publish_interval

Minimum seconds between publishes, tracked per heater.

- **Type**: Float — **Default**: `1.0` — **Range**: `0.1` – `60.0`

## Persistence (advanced)

These keys tune how often the per-profile temperature history is written to
disk (SD card wear protection). They are not exposed in the settings UI —
edit `config.yaml` directly. Values outside the accepted range are ignored
and the default keeps applying.

### persist_backoff_reset_s

Delay before the persist scheduled after a phase ends (target reached,
disconnect).

- **Type**: Float — **Default**: `30.0` — **Accepted**: `1` – `600`

### persist_backoff_initial_s

First persist delay when a heating phase starts; subsequent persists double
the delay until `persist_backoff_max_s`.

- **Type**: Float — **Default**: `60.0` — **Accepted**: `1` – `600`

### persist_backoff_max_s

Backoff cap.

- **Type**: Float — **Default**: `300.0` — **Accepted**: `10` – `3600`

### persist_max_json_bytes

Hard size cap for a profile's history JSON; larger payloads are trimmed
(oldest samples first) before writing.

- **Type**: Integer — **Default**: `262144` (256 KiB) — **Accepted**: `16384` – `10485760`

## Programmatic Access

### Python (inside the plugin)

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
# Get settings (includes plugins.temp_eta)
curl -H "X-Api-Key: YOUR_KEY" http://octopi.local/api/settings

# Update settings
curl -X POST \
  -H "X-Api-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"plugins": {"temp_eta": {"algorithm": "exponential"}}}' \
  http://octopi.local/api/settings
```

## Validation

Two layers keep values sane:

- **Settings UI**: numeric inputs are validated client-side (min/max/range);
  saving is blocked until invalid values are fixed.
- **Server**: `_sanitize_settings_payload` clamps every posted numeric value
  to the ranges listed above; empty or unparsable values fall back to a safe
  default instead of failing the save.

## Backup

The plugin's settings live in `config.yaml` — OctoPrint's built-in backup
covers them. Persisted temperature history lives in the plugin's data folder
(`~/.octoprint/data/temp_eta/history_<profile>.json`) and is disposable
cache data; it is rebuilt from live samples.

## Reset to Defaults

- **Via UI**: Settings → Temperature ETA → Maintenance → _Restore defaults_
  (resets the user-editable keys; history files are kept).
- **Via config file**: delete the `plugins.temp_eta` section and restart.

## Next Steps

- [Settings Architecture](../architecture/settings.md) - Implementation details
- [OctoPrint Integration](../architecture/octoprint-integration.md) - Settings plugin
- [Python API](../api/python.md) - Programmatic access
