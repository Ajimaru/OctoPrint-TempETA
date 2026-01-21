# Architecture Overview

OctoPrint-TempETA is designed as a lightweight, efficient OctoPrint plugin that monitors temperature changes and calculates estimated time to target temperature.

## System Components

The plugin consists of three main components:

### 1. Backend (Python)

- **Plugin Core** (`__init__.py`): Main plugin implementation using OctoPrint's plugin framework
- **Calculator** (`calculator.py`): Temperature ETA calculation algorithms
- **MQTT Client** (`mqtt_client.py`): Optional MQTT integration for external monitoring

### 2. Frontend (JavaScript)

- **View Model** (`temp_eta.js`): Knockout.js-based UI component
- Displays ETA in the temperature graph and sidebar
- Handles user interactions and settings

### 3. Communication Layer

- **Plugin Events**: OctoPrint's event system for temperature updates
- **MQTT Messages**: Optional external integration
- **WebSocket**: Real-time updates to the frontend

## Design Principles

### Thread Safety

Temperature callbacks occur on separate threads (~2Hz). All shared data structures use thread locks to prevent race conditions.

```python
self._lock = threading.RLock()

def _on_temp_callback(self, data):
    with self._lock:
        # Safe data access
        self._update_history(data)
```

### Performance

- **Callback Processing**: < 10ms per invocation
- **History Management**: Rolling window (60 seconds max)
- **Memory Usage**: < 5MB for all history
- **Frontend Updates**: Configurable rate (default 1Hz)

### Modularity

Each component is independent:

- Calculator can run standalone for testing
- MQTT client is optional
- Frontend can be customized without backend changes

## Plugin Lifecycle

```mermaid
graph TD
    A[OctoPrint Start] --> B[Plugin Initialize]
    B --> C[Load Settings]
    C --> D[Start Temperature Monitoring]
    D --> E{Temperature Changed?}
    E -->|Yes| F[Calculate ETA]
    E -->|No| E
    F --> G[Update UI]
    G --> H{MQTT Enabled?}
    H -->|Yes| I[Publish MQTT]
    H -->|No| E
    I --> E
```

## Data Flow

See [Data Flow](data-flow.md) for detailed information on how data moves through the system.

## Key Algorithms

The plugin uses two ETA calculation methods:

### Linear Algorithm (Default)

Simple and fast, assumes constant heating/cooling rate:

```
rate = ΔT / Δt
ETA = (target - current) / rate
```

### Exponential Algorithm (Advanced)

Models thermal dynamics more accurately:

```
T(t) = T_final - (T_final - T_0) * e^(-t/tau)
```

See [Algorithms](algorithms.md) for implementation details.

## OctoPrint Integration

The plugin implements several OctoPrint mixins:

- **StartupPlugin**: Initialization and cleanup
- **TemplatePlugin**: UI integration
- **SettingsPlugin**: Configuration management
- **AssetPlugin**: Static file serving
- **EventHandlerPlugin**: Temperature monitoring
- **SimpleApiPlugin**: REST API endpoints

See [OctoPrint Integration](octoprint-integration.md) for details.

## Configuration

Settings are stored in OctoPrint's configuration system:

```yaml
plugins:
  temp_eta:
    enabled: true
    algorithm: linear
    update_interval: 1.0
    min_rate: 0.1
    # ... more settings
```

See [Settings](settings.md) for all configuration options.

## Internationalization

The plugin supports multiple languages using Flask-Babel:

- English (default)
- German

Translation workflow:

1. Extract messages: `pybabel extract`
2. Update catalogs: `pybabel update`
3. Compile: `pybabel compile`

See [Internationalization](../frontend/i18n.md) for details.

## Extension Points

Developers can extend the plugin through:

1. **Custom Algorithms**: Implement new calculation methods
2. **MQTT Topics**: Subscribe to published data
3. **Settings Overlays**: Add custom configuration
4. **UI Themes**: Customize appearance via CSS/LESS

## Dependencies

### Runtime

- Python 3.11+
- OctoPrint 1.10.2+
- paho-mqtt 1.6.0+ (optional)

### Development

- pytest 7+
- pre-commit 3+
- black 24+
- isort 5+
- flake8 7+

### Documentation

- mkdocs
- mkdocs-material
- mkdocstrings
- mkdocstrings-python
- pymdown-extensions
- jsdoc (Node.js)
- jsdoc-to-markdown (Node.js)

## Security Considerations

- **No external API calls**: All processing is local
- **Input validation**: All settings are validated
- **Thread safety**: Proper locking for concurrent access
- **MQTT authentication**: Supports username/password and TLS
- **Template autoescape**: Enabled to prevent XSS

## Performance Monitoring

The plugin tracks its own performance:

- Callback execution time
- Memory usage
- ETA calculation time
- History buffer size

Enable debug logging to see performance metrics:

```
Settings → Logging → octoprint.plugins.temp_eta → DEBUG
```

## Next Steps

- [Data Flow](data-flow.md) - How data moves through the system
- [Algorithms](algorithms.md) - ETA calculation methods
- [Settings](settings.md) - Configuration reference
- [OctoPrint Integration](octoprint-integration.md) - Plugin implementation details
