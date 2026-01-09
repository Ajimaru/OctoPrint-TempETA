# GitHub Copilot Instructions - OctoPrint Temperature ETA Plugin

**Issue**: [#469](https://github.com/OctoPrint/OctoPrint/issues/469) - Show ETA for bed/hotend heating  
**Target**: OctoPrint 1.4.0+, Python 3.7+ | Implements 2014 feature request

## Requirements

**Blueprint**: See `.development/octoprint-temp-eta-plugin-plan.md` for implementation details and task breakdown.

- Monitor temperature ~2Hz, calculate heating rate, estimate time to target
- Display countdown in navbar/sidebar with configurable threshold
- Support: tool0, bed, chamber heaters
- Algorithms: Linear (default), Exponential
- i18n: English + German
- **Stack**: Python 3.7+, Knockout.js, Jinja2, pytest, Babel

## Code Standards (CRITICAL)

**Docs**: https://docs.octoprint.org/en/main/plugins/index.html | Contributing: https://github.com/OctoPrint/OctoPrint/blob/main/CONTRIBUTING.md

**Template Autoescape**: [How do I improve my plugin's security by enabling autoescape?](https://faq.octoprint.org/plugin-autoescape)

### File Structure & Plugin Class
```
octoprint_temp_eta/__init__.py       # Main plugin
octoprint_temp_eta/static/           # JS, CSS
octoprint_temp_eta/templates/        # Jinja2 templates
translations/                         # i18n
```

```python
class TempETAPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):
    __plugin_name__ = "Temperature ETA"
    __plugin_pythoncompat__ = ">=3.7,<4"
    __plugin_implementation__ = TempETAPlugin()
```

### Code Style (OctoPrint Standard)
- **Indentation**: 4 spaces (NO TABS)
- **Language**: English only (code, comments, docs)
- **Docstrings**: All public methods/classes
- **Comments**: Explain WHY, not WHAT
- **Line length**: 120 chars max (black)
- **No dead code**: Remove all commented-out experiments
- **Import order**: stdlib → third-party → octoprint → local

**When generating code**: Follow OctoPrint standards, use English, include docstrings, test edge cases, ensure thread safety, keep performance in mind.

```python
import threading
from collections import deque
import octoprint.plugin
from .calculator import ETACalculator
```

### Testing: pytest, min 70% coverage, test edge cases, mock OctoPrint internals

### Temperature Callback (Called ~2Hz)
```python
def on_after_startup(self):
    self._printer.register_callback(self)

def on_printer_add_temperature(self, data):
    # data = {"bed": {"actual": X, "target": Y}, "tool0": {...}}
    self._update_history(data)
    self._calculate_eta()
```

### Thread Safety (CRITICAL)
```python
self._lock = threading.Lock()
with self._lock:
    self._temp_history[heater].append((time.time(), temp))
```

### Settings
```python
def get_settings_defaults(self):
    return {"threshold_start": 10.0, "algorithm": "linear"}

threshold = self._settings.get_float(["threshold_start"])
```

### Send to Frontend
```python
self._plugin_manager.send_plugin_message(
    self._identifier,
    {"type": "eta_update", "heater": "bed", "eta": 45.2}
)
```

### Logging (use self._logger)
```python
self._logger.info("ETA started")
self._logger.debug("Rate: %.2f °C/s", rate)
self._logger.error("Failed: %s", str(e))
```

## Algorithm Implementation

### Linear ETA (Default)
```python
def calculate_linear_eta(history, target):
    """Returns seconds to target, None if insufficient data."""
    if len(history) < 2:
        return None
    
    # Use last 10 seconds of data
    recent = [h for h in history if h[0] > time.time() - 10]
    if len(recent) < 2:
        return None
    
    # rate = ΔT / Δt (°C per second)
    rate = (recent[-1][1] - recent[0][1]) / (recent[-1][0] - recent[0][0])
    
    if rate <= 0:
        return None
    
    remaining = target - recent[-1][1]
    return remaining / rate
```

### Exponential ETA (Advanced)
```python
def calculate_exponential_eta(history, target):
    # Model: T(t) = T_final - (T_final - T_0) * e^(-t/tau)
    # Implementation in calculator.py
    pass
```

## Frontend Implementation

### Knockout.js ViewModel
```javascript
function TempETAViewModel(parameters) {
    var self = this;
    self.settings = parameters[0];
    self.bedETA = ko.observable(null);
    self.tool0ETA = ko.observable(null);
    
    self.formatETA = function(seconds) {
        if (!seconds || seconds <= 0) return "--:--";
        var m = Math.floor(seconds / 60);
        var s = Math.floor(seconds % 60);
        return m + ":" + (s < 10 ? "0" : "") + s;
    };
    
    self.onDataUpdaterPluginMessage = function(plugin, data) {
        if (plugin !== "temp_eta") return;
        if (data.type === "eta_update") {
            if (data.heater === "bed") self.bedETA(data.eta);
            if (data.heater === "tool0") self.tool0ETA(data.eta);
        }
    };
}

OCTOPRINT_VIEWMODELS.push({
    construct: TempETAViewModel,
    dependencies: ["settingsViewModel"],
    elements: ["#navbar_plugin_temp_eta"]
});
```

### Jinja2 Template
```jinja2
<div id="navbar_plugin_temp_eta" data-bind="visible: bedETA() !== null">
    <span><i class="fa fa-bed"></i> <span data-bind="text: formatETA(bedETA())"></span></span>
    <span><i class="fa fa-fire"></i> <span data-bind="text: formatETA(tool0ETA())"></span></span>
</div>
```

## Testing

**Unit Tests Example**:
```python
def test_linear_eta_simple():
    history = deque([(0, 20), (1, 21), (2, 22), (3, 23), (4, 24)])
    eta = calculate_linear_eta(history, 30)
    assert abs(eta - 6.0) < 0.1

def test_linear_eta_insufficient_data():
    eta = calculate_linear_eta(deque([(0, 20)]), 30)
    assert eta is None
```

## Internationalization

**Babel Translation**:
```bash
pybabel extract -F babel.cfg -o translations/messages.pot .
pybabel init -i translations/messages.pot -d translations -l de
pybabel compile -d translations
```

**In Code**:
```python
from flask_babel import gettext
message = gettext("Heating to {target}°C, ETA: {eta}").format(target=X, eta=Y)
```

**Languages**: English (primary) + German (secondary)

## Critical Rules

1. **DO NOT** use `print()` → use `self._logger`
2. **DO NOT** edit CSS directly → Edit LESS and compile
3. **DO NOT** block callback → Keep it fast (<10ms)
4. **DO NOT** assume temp increases → Handle cooling, target changes
5. **DO NOT** forget thread safety → Use locks for shared data
6. **DO NOT** use globals → Use instance variables only
7. **DO NOT** hardcode strings → Use i18n for user-facing text
8. **DO NOT** forget disabled heaters → Check if target > 0

## Performance

- Callback processing: < 10ms (2Hz)
- Frontend updates: 1Hz default
- Memory: < 5MB for history
- Cleanup: Remove data older than 60 seconds

## Development Workflow

```bash
# Branch: wip/feature-name or fix/issue-description
# Commit: "Add ETA calculation" (imperative mood)
# Before commit: pytest && pre-commit run --all-files
```

## Files to Ignore (Don't Commit)

`.development/`, `venv/`, `__pycache__/`, `.pytest_cache/`, `.coverage/`, `.idea/`, `.vscode/`

## Key References

- Issue #469: https://github.com/OctoPrint/OctoPrint/issues/469
- Plugin Docs: https://docs.octoprint.org/en/main/plugins/
- Mixins: https://docs.octoprint.org/en/main/plugins/mixins.html
- Contributing: https://github.com/OctoPrint/OctoPrint/blob/main/CONTRIBUTING.md
- Knockout.js: https://knockoutjs.com/documentation/introduction.html