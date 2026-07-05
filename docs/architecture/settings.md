# Settings Architecture

How OctoPrint-TempETA defines, validates, applies and caches its settings.

For the key-by-key reference (types, defaults, ranges) see
[Configuration Reference](../reference/configuration.md).

## Overview

```text
Settings UI (temp_eta_settings.jinja2)
      │  client-side validation (min/max, blocked save)
      ▼
on_settings_save(data)
      │  _sanitize_settings_payload(data)   ← server-side clamping
      ▼
octoprint.plugin.SettingsPlugin.on_settings_save
      │  persists to config.yaml
      ▼
post-save refresh:
      • _refresh_debug_logging_flag()
      • _refresh_runtime_caches()          ← hot-path value cache
      • _set_history_maxlen(...)           ← resize history deques
      • _configure_mqtt_client()           ← reconnect/disconnect broker
      • clear frontend if plugin was just disabled
```

## Defaults

`get_settings_defaults()` in `octoprint_temp_eta/__init__.py` is the single
source of truth for every key and its default. OctoPrint only writes keys to
`config.yaml` when they differ from these defaults.

## Validation layers

Settings pass through two independent validation layers:

1. **Client-side** — the settings dialog validates every
   `input[type="number"]` against its `min`/`max` attributes on
   input/change/blur, marks invalid fields (`aria-invalid`, Bootstrap error
   classes) and blocks saving via `onSettingsBeforeSave` until fixed. The
   heating threshold gets special handling because it is entered in the
   selected display unit (°C or °F delta) but stored in °C.
2. **Server-side** — `_sanitize_settings_payload()` clamps every posted
   numeric value to its allowed range as a safety net (the UI can be
   bypassed via the REST API). Empty or unparsable values fall back to a
   safe default instead of failing the save; the optional
   `cooldown_ambient_temp` becomes `None` when invalid or out of range.

There is deliberately **no settings migration logic**: new keys simply get
their default from `get_settings_defaults()`, and obsolete keys in
`config.yaml` are ignored.

## Runtime caches (hot path)

The temperature callback runs at ~2 Hz and must not hit OctoPrint's settings
machinery on every sample. Frequently needed values are cached on the plugin
instance and refreshed on startup, on settings save, and (as a safety net)
at most every 5 seconds from the callback itself:

- `_threshold_start_c` ← `threshold_start`
- `_update_interval_s` ← `update_interval`
- `_history_maxlen` ← `history_size` (also resizes the per-heater deques)
- `_debug_logging_enabled` ← `debug_logging`
- persistence tuning (`persist_backoff_*`, `persist_max_json_bytes`)

Out-of-range values read from `config.yaml` are ignored and the previous
(cached or default) value keeps applying — a hand-edited bad value can't
break the callback.

Less frequently used settings (algorithm selection, cooldown configuration,
UI visibility flags) are read directly from `self._settings` when needed,
each wrapped defensively so a settings hiccup never raises into OctoPrint's
callback thread.

## Applying changes

`on_settings_save` compares before/after state and applies side effects only
when relevant:

- **Plugin disabled** → clears all heater ETAs in every connected frontend so
  no stale countdown lingers.
- **`history_size` changed** → rebuilds the history deques with the new
  `maxlen` (trimming oldest samples if shrunk) and marks history dirty for
  persistence.
- **Debug flag flipped** → logs the transition once.
- **Always** → reconfigures the MQTT client; the wrapper itself decides
  whether it needs to connect, reconnect or disconnect.

## Frontend binding

The settings template uses `custom_bindings: True`. The view model binds it
lazily when the settings dialog opens (with retries, because OctoPrint
injects the template asynchronously) and unbinds on close. The settings
object is resolved defensively (`_resolveSettingsRoot`) because different
OctoPrint versions nest the settings view model differently, with a fallback
to the last known-good object during transient reloads.

## Maintenance actions

Two admin-only Simple API commands (buttons on the Maintenance tab):

- `reset_profile_history` — deletes all persisted per-profile history files
  and clears in-memory + frontend state.
- `reset_settings_defaults` — resets the user-editable keys back to their
  defaults (persistence tuning and history files are untouched) and
  broadcasts `settings_reset` so open settings dialogs refresh.

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
// Observables live under the plugin's settings namespace:
var ps = self.settings.plugins.temp_eta;

// Get setting
var algorithm = ps.algorithm();

// Set setting (persisted when the settings dialog is saved)
ps.algorithm("exponential");
```

## Next Steps

- [Configuration Reference](../reference/configuration.md) - All keys, types, defaults, ranges
- [Python API](../api/python.md) - Programmatic access
- [OctoPrint Integration](octoprint-integration.md) - Settings plugin implementation
- [Frontend Settings](../frontend/ui-placements.md) - Settings UI
