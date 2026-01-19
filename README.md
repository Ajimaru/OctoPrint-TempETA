<!-- markdownlint-disable MD041 MD033-->
<p align="center">
  <img src="octoprint_temp_eta/static/img/temp_eta.svg" alt="Temperature ETA Logo" width="96" />
</p>
<h1 align="center">OctoPrint Temperature ETA Plugin</h1>
<!-- markdownlint-enable MD041 MD033-->

[![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![OctoPrint](https://img.shields.io/badge/OctoPrint-1.10.2%2B-blue.svg)](https://octoprint.org)
[![Latest Release](https://img.shields.io/github/v/release/Ajimaru/OctoPrint-TempETA?sort=semver)](https://github.com/Ajimaru/OctoPrint-TempETA/releases/latest)
[![Issues](https://img.shields.io/github/issues/Ajimaru/OctoPrint-TempETA)](https://github.com/Ajimaru/OctoPrint-TempETA/issues)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![Coverage](https://codecov.io/gh/Ajimaru/OctoPrint-TempETA/graph/badge.svg?branch=main)](https://codecov.io/gh/Ajimaru/OctoPrint-TempETA)
[![CI](https://github.com/Ajimaru/OctoPrint-TempETA/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Ajimaru/OctoPrint-TempETA/actions/workflows/ci.yml?query=branch%3Amain)
[![i18n](https://github.com/Ajimaru/OctoPrint-TempETA/actions/workflows/i18n.yml/badge.svg?branch=main)](https://github.com/Ajimaru/OctoPrint-TempETA/actions/workflows/i18n.yml?query=branch%3Amain)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Ajimaru/OctoPrint-TempETA/pulls)

### Heat Up and Cool Down with Confidence

<!-- markdownlint-disable MD033-->
<strong>
  Display real-time countdown/ETA when your 3D printer's bed, hotend, or chamber is heating up or cooling down.<br />
  No more guessing how long until your print starts or is ready for maintenance!
</strong>

#### Heating

<img src="assets/img/Temperature_ETA_heating.png" alt="Heating ETA" width="666" />

#### Cooling

<img src="assets/img/Temperature_ETA_cooling.png" alt="Cooling ETA" width="666" />
<!-- markdownlint-enable MD033-->

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Installation](#installation)
  - [Via Plugin Manager (Recommended)](#via-plugin-manager-recommended)
  - [Manual Installation](#manual-installation)
- [Configuration](#configuration)
  - [General](#general)
  - [Heating ETA](#heating-eta)
  - [Cool-down ETA](#cool-down-eta)
  - [MQTT](#mqtt)
  - [Maintenance](#maintenance)
  - [Help](#help)
  - [Settings Defaults](#settings-defaults)
- [How It Works](#how-it-works)
- [MQTT Message Format](#mqtt-message-format)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Credits](#credits)

## Features

- ⏱️ **Real-time ETA countdown** for bed, hotend and chamber heating or cooling
- 🌡️ **Smart calculation algorithms**: Linear (default) and exponential models
- 📊 **Flexible display**: Show ETA in navbar, sidebar, and/or a dedicated tab
- 📈 **Progress bars**: Show progress to target in the sidebar and tab views
- 📉 **Historical temperature graphs**: A dedicated history view in the tab with a configurable time window
- ⏳ **Heating ETA**: Estimates time remaining until target temperature is reached
- 🧊 **Cool-down ETA**: Estimates time remaining until cool-down target is reached (target set to 0), with two modes: threshold-based and ambient-based
- 🎛️ **Configurable thresholds**: Start countdown when within a configurable delta to target
- 🎨 **Status colors**: Optional color bands for heating/cooling/idle states
- 🔔 **Sound alerts**: Play a sound when target is reached or cool-down finishes
- 🖥️ **Browser toast notifications**: Small top-right notifications for key events (default off)
- 📡 **MQTT integration**: Publish ETA data and state changes to an MQTT broker for home automation
- 🔁 **Reset history**: One-click reset deletes persisted history files for all printer profiles
- 🧰 **Multiple heaters**: Supports tools, bed and chamber (as reported by OctoPrint/printer)
- 🌍 **Internationalization**: English and German included, easily extensible
- 🧮 **Supports °C and °F** based on OctoPrint settings
- ⚙️ **Highly configurable**: Many settings to tailor behavior and display to your needs
- 🚀 **Lightweight**: Minimal performance impact (~2Hz monitoring)

## Installation

### Via Plugin Manager (Recommended)

1. Open OctoPrint web interface
2. Navigate to **Settings** → **Plugin Manager**
3. Click **Get More...**
4. Click **Install from URL** and enter:
   `https://github.com/Ajimaru/OctoPrint-TempETA/releases/latest/download/octoprint_tempeta-latest.zip`
5. Click **Install**
6. Restart OctoPrint

### Manual Installation

```bash
pip install https://github.com/Ajimaru/OctoPrint-TempETA/releases/latest/download/octoprint_tempeta-latest.zip
```

The `releases/latest` URL always points to the newest stable release.

## Configuration

Configure the plugin in **Settings** → **Temperature ETA**:

<!-- markdownlint-disable MD033 -->

<img
  src="assets/img/Temperature_ETA_settings.png"
  alt="Temperature ETA settings"
  width="666"
/>

<!-- markdownlint-enable MD033 -->

The settings UI is organized into multiple tabs:

### General
<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>General Settings</strong> (click to expand)</summary>

- **Enable Temperature ETA**: Master switch for the plugin
- **Hide ETA while printing**: Optionally suppress ETA during active print jobs
- **Show in sidebar / navbar / tab**: Independently enable the UI placements
- **Show progress bars**: Show progress bars in sidebar and tab
- **Show historical graph** + **Historical graph window (seconds)**: Configure the history graph in the tab
- **Temperature display**: Use OctoPrint's preference or override it
- **Status colors**: Configure time-based bands or fixed status colors (heating/cooling/idle)
- **Update & Logging**:
  - **Update interval** + **Temperature history size**: Control refresh rate and retained samples
  - **Debug logging** (optional): Enables additional log output (may be noisy)
- **Sound alerts** (optional): Enable per-event sounds, volume, rate limit, and a test button
- **Browser notifications** (optional): Enable per-event toasts, timeout, and rate limit

Note: Numeric settings inputs are validated (min/max/range) and saving is blocked until invalid values are fixed.

</details>
<!-- markdownlint-enable MD033 -->

### Heating ETA
<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>Heating ETA Settings</strong> (click to expand)</summary>

- **Enable heating ETA**: Controls whether heating ETAs are shown/calculated
- **Heating threshold** + **Threshold unit**: Start ETA when within a configured delta to the target
- **Calculation algorithm**: Linear (default) or exponential

</details>
<!-- markdownlint-enable MD033 -->

### Cool-down ETA
<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>Cool-down ETA Settings</strong> (click to expand)</summary>

- **Enable cool-down ETA**: Turn cool-down ETA on/off
- **Mode**:
  - **Threshold target (default)**: Estimate time until a fixed, per-heater target is reached
  - **Ambient-based target**: Estimate time until near ambient temperature (best-effort)
- **Cool-down targets**: Configure per-heater targets (tool0/bed/chamber) for threshold mode
- **Ambient temperature** (optional): Provide a fixed ambient value for ambient mode
- **Hysteresis / fit window**: Controls when cool-down ETA disappears and how much recent data is used

</details>
<!-- markdownlint-enable MD033 -->

### MQTT
<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>MQTT Settings</strong> (click to expand)</summary>

- **Enable MQTT**: Master switch for MQTT integration (publishes ETA data to external broker)
- **Broker Host**: MQTT broker hostname or IP address (e.g., `localhost`, `192.168.1.100`)
- **Broker Port**: MQTT broker port (default: `1883`, TLS typically uses `8883`)
- **Username/Password**: Optional authentication credentials for the MQTT broker
- **Use TLS/SSL**: Enable encrypted connection to the broker
- **Skip TLS certificate verification**: For self-signed certificates (not recommended for production)
- **Base Topic**: Root MQTT topic for publishing messages (default: `octoprint/temp_eta`)
  - ETA updates are published to: `{base_topic}/{heater}/eta`
  - State changes are published to: `{base_topic}/{heater}/state_change`
- **QoS**: MQTT Quality of Service level (0=At most once, 1=At least once, 2=Exactly once)
- **Retain Messages**: Enable MQTT retain flag (new subscribers receive the last message)
- **Publish Interval**: Minimum seconds between MQTT publishes (default: `1.0`)

</details>
<!-- markdownlint-enable MD033 -->

### Maintenance
<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>Maintenance Actions</strong> (click to expand)</summary>

- **Reset profile history**: Deletes all persisted ETA history JSON files for all printer profiles (stored in OctoPrint's plugin data folder)
- **Restore defaults**: Resets only this plugin's settings back to defaults (does not delete history files)

</details>
<!-- markdownlint-enable MD033 -->

### Help
<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>How is ETA calculated?</strong> (click to expand)</summary>

**ETA Logic Overview**
The plugin estimates how long it will take for each heater (bed, hotend, chamber) to reach its target temperature (heating) or cool down to a set value (cooling). It does this by analyzing recent temperature history and applying a calculation algorithm.

**Algorithms Used**

- **Linear ETA (default):**
  Calculates the rate of temperature change (°C/s) using the last 10 seconds of data. ETA is the remaining temperature difference divided by this rate.
  This method is fast and stable for most printers.

- **Exponential ETA (advanced):**
  Models heating/cooling as an exponential curve, which can be more accurate for some hardware.
  This option can be enabled in the settings.

**Key Points**

- ETA is only shown when the heater is actively heating/cooling and within a configurable threshold of the target.
- The plugin automatically handles multiple heaters and adapts to target changes.
- All calculations are optimized for performance and run in a background thread.

</details>
<!-- markdownlint-enable MD033 -->

### Settings Defaults
<!-- markdownlint-disable MD033 MD040 -->
<details>
<summary><strong>Default Plugin Settings</strong> (click to expand)</summary>

The following defaults apply to the user-editable plugin settings:

<table>
<thead>
<tr>
<th>Setting</th>
<th>Key</th>
<th>Default</th>
</tr>
</thead>
<tbody>
<tr><td>Enable Temperature ETA</td><td><code>enabled</code></td><td><code>true</code></td></tr>
<tr><td>Enable heating ETA</td><td><code>enable_heating_eta</code></td><td><code>true</code></td></tr>
<tr><td>Hide ETA while printing</td><td><code>suppress_while_printing</code></td><td><code>false</code></td></tr>
<tr><td>Show in sidebar</td><td><code>show_in_sidebar</code></td><td><code>true</code></td></tr>
<tr><td>Show in navbar</td><td><code>show_in_navbar</code></td><td><code>true</code></td></tr>
<tr><td>Show in tab</td><td><code>show_in_tab</code></td><td><code>true</code></td></tr>
<tr><td>Show progress bars</td><td><code>show_progress_bars</code></td><td><code>true</code></td></tr>
<tr><td>Show historical graph</td><td><code>show_historical_graph</code></td><td><code>true</code></td></tr>
<tr><td>Graph window (seconds)</td><td><code>historical_graph_window_seconds</code></td><td><code>180</code></td></tr>
<tr><td>Temperature display</td><td><code>temp_display</code></td><td><code>octoprint</code></td></tr>
<tr><td>Heating threshold</td><td><code>threshold_start</code></td><td><code>5.0 °C</code></td></tr>
<tr><td>Threshold unit</td><td><code>threshold_unit</code></td><td><code>octoprint</code></td></tr>
<tr><td>Algorithm</td><td><code>algorithm</code></td><td><code>linear</code></td></tr>
<tr><td>Update Interval</td><td><code>update_interval</code></td><td><code>1.0 s</code></td></tr>
<tr><td>History Size</td><td><code>history_size</code></td><td><code>60</code></td></tr>
<tr><td>Enable cool-down ETA</td><td><code>enable_cooldown_eta</code></td><td><code>true</code></td></tr>
<tr><td>Cool-down mode</td><td><code>cooldown_mode</code></td><td><code>threshold</code></td></tr>
<tr><td>Enable debug logging</td><td><code>debug_logging</code></td><td><code>false</code></td></tr>
<tr><td>Color mode</td><td><code>color_mode</code></td><td><code>bands</code></td></tr>
<tr><td>Heating color</td><td><code>color_heating</code></td><td><code>#5cb85c</code></td></tr>
<tr><td>Cooling color</td><td><code>color_cooling</code></td><td><code>#337ab7</code></td></tr>
<tr><td>Idle color</td><td><code>color_idle</code></td><td><code>#777777</code></td></tr>
<tr><td>Enable sound alerts</td><td><code>sound_enabled</code></td><td><code>false</code></td></tr>
<tr><td>Sound: target reached</td><td><code>sound_target_reached</code></td><td><code>false</code></td></tr>
<tr><td>Sound: cool-down done</td><td><code>sound_cooldown_finished</code></td><td><code>false</code></td></tr>
<tr><td>Sound volume</td><td><code>sound_volume</code></td><td><code>0.5</code></td></tr>
<tr><td>Sound min interval</td><td><code>sound_min_interval_s</code></td><td><code>10.0 s</code></td></tr>
<tr><td>Enable notifications</td><td><code>notification_enabled</code></td><td><code>false</code></td></tr>
<tr><td>Notify: target reached</td><td><code>notification_target_reached</code></td><td><code>false</code></td></tr>
<tr><td>Notify: cool-down done</td><td><code>notification_cooldown_finished</code></td><td><code>false</code></td></tr>
<tr><td>Notification timeout</td><td><code>notification_timeout_s</code></td><td><code>6.0 s</code></td></tr>
<tr><td>Notification min interval</td><td><code>notification_min_interval_s</code></td><td><code>10.0 s</code></td></tr>
<tr><td>Enable MQTT</td><td><code>mqtt_enabled</code></td><td><code>false</code></td></tr>
<tr><td>MQTT broker host</td><td><code>mqtt_broker_host</code></td><td><code>""</code></td></tr>
<tr><td>MQTT broker port</td><td><code>mqtt_broker_port</code></td><td><code>1883</code></td></tr>
<tr><td>MQTT username</td><td><code>mqtt_username</code></td><td><code>""</code></td></tr>
<tr><td>MQTT password</td><td><code>mqtt_password</code></td><td><code>""</code></td></tr>
<tr><td>MQTT use TLS</td><td><code>mqtt_use_tls</code></td><td><code>false</code></td></tr>
<tr><td>MQTT TLS insecure</td><td><code>mqtt_tls_insecure</code></td><td><code>false</code></td></tr>
<tr><td>MQTT base topic</td><td><code>mqtt_base_topic</code></td><td><code>octoprint/temp_eta</code></td></tr>
<tr><td>MQTT QoS</td><td><code>mqtt_qos</code></td><td><code>0</code></td></tr>
<tr><td>MQTT retain</td><td><code>mqtt_retain</code></td><td><code>false</code></td></tr>
<tr><td>MQTT publish interval</td><td><code>mqtt_publish_interval</code></td><td><code>1.0 s</code></td></tr>
</tbody>
</table>

</details>
<!-- markdownlint-enable MD033 MD040 -->

## How It Works

1. **Temperature Monitoring**: Plugin registers for temperature callbacks (~2Hz frequency)
2. **Rate Calculation**: Analyzes temperature history to determine heating rate (°C/second)
3. **ETA Estimation**: Uses selected algorithm (linear/exponential) to predict time to target
4. **Display Update**: Sends countdown to frontend via WebSocket (1Hz default)
5. **Smart Thresholds**: Only shows ETA when heating or cooling and within configured threshold

## MQTT Message Format
<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>MQTT Message Format Details</strong> (click to expand)</summary>

**ETA Updates** (`{base_topic}/{heater}/eta`):

```json
{
  "heater": "bed",
  "eta_seconds": 120.5,
  "eta_kind": "heating",
  "target": 60.0,
  "actual": 40.2,
  "cooldown_target": null,
  "timestamp": 1234567890.123,
  "state": "heating"
}
```

**State Changes** (`{base_topic}/{heater}/state_change`):

```json
{
  "heater": "bed",
  "state": "at_target",
  "previous_state": "heating",
  "timestamp": 1234567890.456,
  "actual": 60.0,
  "target": 60.0
}
```

</details>
<!-- markdownlint-enable MD033 -->

## FAQ

**Q: Why does the ETA jump around?**
A: Temperature changes aren't perfectly linear. The plugin uses recent data to calculate rate. Longer threshold values provide more stable estimates.

**Q: Can I use this with multiple hotends?**
A: Yes. The UI registers heaters dynamically as OctoPrint reports them (e.g. tool0, tool1, ...).

**Q: Does this work with chamber heaters?**
A: Yes! Enable chamber in settings if your printer has a chamber heater.

**Q: Will this slow down my prints?**
A: No. The plugin uses efficient algorithms and runs in a separate thread. Impact is negligible.

**Q: Can I hide the ETA during an active print?**
A: Yes. If you enable "Hide ETA while printing", the plugin will only show ETA when no print job is active. If the option is disabled (default), ETA is shown whenever the target temperature is at least the configured heating threshold above the current temperature.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b wip/my-feature`
3. Write tests for new features
4. Submit a pull request
5. For local development scripts (setup, restart helper, post-commit build hook, performance monitor), see [.development/README.md](.development/README.md).
6. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
7. Please follow our [Code of Conduct](CODE_OF_CONDUCT.md).

Note: `main` is protected on GitHub, so changes go through PRs.

## License

AGPLv3 - See [LICENSE](LICENSE) for details.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Ajimaru/OctoPrint-TempETA/issues)
- 💬 **Discussion**: [Github Discussions](https://github.com/Ajimaru/OctoPrint-TempETA/discussions)

Note: For logs and troubleshooting, enable "debug logging" in the plugin settings.

## Credits

- **Original Request**: [Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469) by [@CptanPanic](https://github.com/CptanPanic) (2014)
- **Development**: Built following [OctoPrint Plugin Guidelines](https://docs.octoprint.org/en/main/plugins/index.html)
- **Contributors**: See [AUTHORS.md](AUTHORS.md)

---

**Like this plugin?** ⭐ Star the repo and share it with the OctoPrint community!
