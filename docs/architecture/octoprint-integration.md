# OctoPrint Integration

This page describes how OctoPrint-TempETA integrates with OctoPrint's plugin
framework. All snippets below mirror the actual implementation in
`octoprint_temp_eta/__init__.py`.

## Temperature source: PrinterCallback

The plugin's data source is **not** an event handler — it registers itself as
an `octoprint.printer.PrinterCallback` and receives temperature updates
directly:

```python
class TempETAPlugin(octoprint.printer.PrinterCallback, ...):
    def on_after_startup(self):
        self._printer.register_callback(self)

    def on_printer_add_temperature(self, data):
        # data = {"bed": {"actual": 40.2, "target": 60.0}, "tool0": {...}, ...}
        ...
```

`on_printer_add_temperature` fires at roughly 2 Hz whenever OctoPrint polls
the printer. This is the plugin's hot path: it records history samples,
computes ETAs, broadcasts them to the frontend and (optionally) publishes to
MQTT. Everything in this path is wrapped defensively — an exception here
would hit OctoPrint's printer communication thread.

The callback interface also requires `on_printer_send_current_data`,
`on_printer_add_log` and `on_printer_add_message`; the plugin implements them
as no-op stubs.

## Plugin Mixins

### StartupPlugin

```python
def on_after_startup(self):
    """Called after OctoPrint startup, register for temperature updates."""
    self._logger.info("Temperature ETA Plugin started")
    self._printer.register_callback(self)

    self._refresh_debug_logging_flag()
    self._refresh_runtime_caches()
    self._set_history_maxlen(self._read_history_maxlen_setting())

    # Load persisted history for the active printer profile.
    self._switch_active_profile_if_needed(force=True)

    # Initialize MQTT client
    if MQTTClientWrapper is not None:
        self._mqtt_client = MQTTClientWrapper(self._logger, self._identifier)
        self._configure_mqtt_client()
```

There is no `on_shutdown` handler; MQTT is disconnected from the `Shutdown`
event instead (see EventHandlerPlugin below).

### TemplatePlugin

```python
def get_template_configs(self):
    return [
        {"type": "navbar", "custom_bindings": True},
        {
            "type": "sidebar",
            "custom_bindings": False,
            "name": gettext("Temperature ETA"),
            "icon": "fa fa-clock",
        },
        {"type": "settings", "custom_bindings": True},
        {"type": "tab", "custom_bindings": False},
    ]
```

Template files follow OctoPrint's naming convention and need no explicit
`template` key:

```text
octoprint_temp_eta/templates/
├── temp_eta_navbar.jinja2
├── temp_eta_settings.jinja2
├── temp_eta_sidebar.jinja2
└── temp_eta_tab.jinja2
```

The plugin also opts into template autoescaping (OctoPrint 1.11+) to reduce
XSS risk:

```python
def is_template_autoescaped(self) -> bool:
    return True
```

### SettingsPlugin

`get_settings_defaults()` is the single source of truth for all keys (see
the [Configuration Reference](../reference/configuration.md)).
`on_settings_save` sanitizes the posted payload, delegates to OctoPrint, then
applies side effects — see [Settings Architecture](settings.md) for the full
flow. The plugin has no settings versioning/migration; new keys simply get
defaults.

### AssetPlugin

```python
def get_assets(self):
    return {
        "js": ["js/temp_eta.js"],
        # Ship pre-compiled CSS rather than LESS: OctoPrint only compiles
        # LESS when a server-side compiler is present, which is not
        # guaranteed on a pip-installed plugin.
        "css": ["css/temp_eta.css"],
    }
```

Note the deliberate omission of the `less` asset type: the `.less` source
stays in the tree as the editable origin, but the shipped stylesheet is the
pre-compiled `temp_eta.css` (regenerate with
`npx less less/temp_eta.less css/temp_eta.css`).

```text
octoprint_temp_eta/static/
├── js/temp_eta.js          # Knockout view model (runtime)
├── js/temp_eta.docs.js     # JSDoc-only, not loaded by OctoPrint
├── css/temp_eta.css        # shipped stylesheet (compiled from LESS)
├── less/temp_eta.less      # editable source
├── img/temp_eta.svg
└── sounds/
    ├── heating_done.wav
    └── cooling_done.wav
```

Assets are served at `/plugin/temp_eta/static/...`.

### EventHandlerPlugin

Events are used only to keep UI/state consistent — temperature data itself
arrives via the printer callback:

```python
def on_event(self, event, _payload):
    if event in ("Disconnected", "Error", "Shutdown"):
        # Persist what we have, then clear histories and frontend ETAs
        self._persist_current_profile_history()
        ...
        if event == "Shutdown" and mqtt_client is not None:
            mqtt_client.disconnect()

    if event in ("PrintStarted", "PrintResumed", "PrintDone",
                 "PrintFailed", "PrintCancelled"):
        # Reset the "suppress while printing" latch; the temperature
        # callback re-evaluates suppression on the next sample.
        ...
```

### SimpleApiPlugin

The Simple API is authenticated and admin-only:

```python
def is_api_protected(self) -> bool:
    return True

def is_api_adminonly(self) -> bool:
    return True

def get_api_commands(self):
    return {
        "reset_profile_history": [],
        "reset_settings_defaults": [],
    }
```

`GET /api/plugin/temp_eta` returns the MQTT integration status for the
settings UI:

```json
{ "mqtt_available": true, "mqtt_enabled": false, "mqtt_connected": false }
```

**Example requests:**

```bash
# MQTT status
curl -H "X-Api-Key: YOUR_API_KEY" http://octopi.local/api/plugin/temp_eta

# Delete persisted history for all printer profiles
curl -X POST \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "reset_profile_history"}' \
  http://octopi.local/api/plugin/temp_eta
```

Current ETA values are **not** exposed via the Simple API — consume them via
plugin messages (frontend) or MQTT instead.

## Plugin Registration

The plugin uses module-level registration (no `__plugin_load__` /
`__plugin_check__` functions):

```python
__plugin_name__ = "Temperature ETA"
__plugin_author__ = "Ajimaru"
__plugin_url__ = "https://github.com/Ajimaru/OctoPrint-TempETA"
__plugin_description__ = (
    "OctoPrint plugin to show estimated time remaining for printer heating"
)
__plugin_license__ = "AGPL-3.0-or-later"
__plugin_version__ = VERSION  # from octoprint_temp_eta/_version.py
__plugin_pythoncompat__ = ">=3.9,<4"
__plugin_implementation__ = TempETAPlugin()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config":
        __plugin_implementation__.get_update_information
}
```

Optional imports (OctoPrint itself, Flask, Flask-Babel, paho-mqtt) are
guarded with fallback stubs so the module can be imported in CI and static
analysis environments where OctoPrint is not installed.

## WebSocket Communication

### Send Message to Frontend

Every ETA update is broadcast as a flat payload:

```python
self._plugin_manager.send_plugin_message(
    self._identifier,
    {
        "type": "eta_update",
        "heater": "tool0",
        "eta": 120.0,            # seconds, or None
        "eta_kind": "heating",   # "heating" | "cooling" | None
        "target": 200.0,
        "actual": 25.0,
        "cooldown_target": None,
        "cooldown_mode": None,   # "threshold" | "ambient" | None
    },
)
```

Other message types: `history_reset` (clear client-side graph buffers) and
`settings_reset` (refresh open settings dialogs).

### Receive in Frontend

```javascript
self.onDataUpdaterPluginMessage = (plugin, data) => {
  if (plugin !== "temp_eta") return;

  if (data.type === "eta_update") {
    // register heater lazily, update observables, trigger alerts
  }
};
```

## Plugin Dependencies

```toml
# pyproject.toml
[project]
dependencies = [
    "paho-mqtt>=2.0.0,<3.0.0"
]
```

OctoPrint itself is the runtime environment, not a pip dependency of the
plugin. The MQTT wrapper degrades gracefully when paho-mqtt is missing.
There are **no** numpy/scipy dependencies — all ETA math is pure Python.

## Plugin Hooks

### Software Update Hook

```python
def get_update_information(self):
    return {
        "temp_eta": {
            "displayName": "Temperature ETA Plugin",
            "displayVersion": self._plugin_version,
            "type": "github_release",
            "user": "Ajimaru",
            "repo": "OctoPrint-TempETA",
            "current": self._plugin_version,
            "pip": "https://github.com/Ajimaru/OctoPrint-TempETA/archive/{target_version}.zip",
        }
    }
```

## Logging

The plugin uses the `self._logger` injected by OctoPrint
(`octoprint.plugins.temp_eta`). To see verbose output, enable the plugin's
**Debug logging** setting — debug messages are emitted at info level with a
`[debug]` prefix, so no logger reconfiguration is needed. Alternatively:

```text
Settings → Logging → Add logger
Logger: octoprint.plugins.temp_eta
Level: DEBUG
```

## Error Handling

The guiding rule: **never raise into OctoPrint's core threads.** The
temperature callback, event handler and settings hooks catch expected error
types (`_EXPECTED_ERRORS` in `__init__.py`), log at debug level and continue.
The MQTT wrapper connects in a background thread and retries with a 30 s
backoff, so a broker outage never blocks temperature processing.

## Testing with OctoPrint

### Development Setup

```bash
# Install OctoPrint
pip install "OctoPrint>=1.11.0,<2"

# Install plugin in dev mode
pip install -e .

# Run OctoPrint
octoprint serve --debug
```

See [.development/README.md](https://github.com/Ajimaru/OctoPrint-TempETA/tree/main/.development)
for the project's setup and restart helper scripts.

### Virtual Printer

Use OctoPrint's virtual printer for testing:

```text
Settings → Serial Connection → Enable virtual printer
Connect to VIRTUAL
```

## Best Practices

1. **Use OctoPrint's systems**: Don't reinvent logging, settings, etc.
2. **Handle errors gracefully**: Plugin failures shouldn't crash OctoPrint
3. **Respect threading**: Use locks for shared data
4. **Log appropriately**: Debug logs for development, info for users
5. **Document settings**: Provide clear descriptions
6. **Test thoroughly**: Test with virtual and real printers
7. **Follow conventions**: Use OctoPrint's coding style

## Next Steps

- [Plugin API Reference](../api/python.md) - Detailed API documentation
- [Settings Architecture](settings.md) - Settings flow and validation
- [Testing Guide](../development/testing.md) - How to test the plugin
