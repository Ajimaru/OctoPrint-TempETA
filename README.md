<!-- markdownlint-disable MD041 MD033-->
<p align="center">
  <img src="octoprint_temp_eta/static/img/temp_eta.svg" alt="Temperature ETA Logo" width="96" />
</p>
<h1 align="center">OctoPrint Temperature ETA Plugin</h1>
<!-- markdownlint-enable MD041 MD033-->

[![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![OctoPrint](https://img.shields.io/badge/OctoPrint-1.12.0%2B-blue.svg)](https://octoprint.org)
[![Latest Release](https://img.shields.io/github/v/release/Ajimaru/OctoPrint-TempETA?sort=semver)](https://github.com/Ajimaru/OctoPrint-TempETA/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/Ajimaru/OctoPrint-TempETA/latest/total)](https://github.com/Ajimaru/OctoPrint-TempETA/releases/latest)
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

#### Heating ETA

<img src="assets/img/Temperature_ETA_heating.png" alt="Heating ETA" width="666" />

#### Cooling ETA

<img src="assets/img/Temperature_ETA_cooling.png" alt="Cooling ETA" width="666" />
<!-- markdownlint-enable MD033-->

## Features

- ⏱️ **Real-time ETA countdown** for bed, hotend and chamber heating
- 🌡️ **Smart calculation algorithms**: Linear (default) and exponential models
- 📊 **Flexible display**: Show ETA in navbar, sidebar, and/or a dedicated tab
- 📈 **Heating progress bars** (optional): Show progress to target in the sidebar and tab views
- 📉 **Historical temperature graphs**: A dedicated history view in the tab with a configurable time window (can be disabled)
- 🧊 **Cool-down ETA**: Optional ETA estimates when turning heaters off (target set to 0), with two modes: threshold-based and ambient-based
- 🎛️ **Configurable thresholds**: Start countdown when within a configurable delta to target
- 🎨 **Status colors**: Optional color bands for heating/cooling/idle states
- 🔔 **Sound alerts** (optional): Play a sound when target is reached or cool-down finishes
- 🖥️ **Browser toast notifications** (optional): Small top-right notifications for key events (default off)
- 🔁 **Reset history**: One-click reset deletes persisted history files for all printer profiles
- 🧰 **Multiple heaters**: Supports tools, bed and chamber (as reported by OctoPrint/printer)
- 🌍 **Internationalization**: English and German included, easily extensible
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

After installation, configure the plugin in **Settings** → **Temperature ETA**:

### Basic Settings

- **Enable Plugin**: Toggle ETA calculation on/off
- **Heating threshold**: Begin countdown when temperature is within this delta to target (default: 5.0°C)
- **Threshold unit**: Celsius / Fahrenheit / Follow temperature display (default: Follow temperature display)
- **Calculation Algorithm**:
  - **Linear** (default): Assumes constant heating rate, simple and fast
  - **Exponential**: Accounts for thermal asymptotic behavior, more accurate

### Display

- **Show in sidebar / navbar / tab**: Independently toggle UI placement
- **Tab view layout**: The Temperature ETA tab contains **Real-time Countdown** and (optionally) **Historical graph**
- **Show progress bars**: Toggle heating progress bars in the sidebar and tab views
- **Show historical graph**: Toggle the historical temperature graphs in the tab view (when disabled, the **Historical graph** subtab is hidden)
- **Historical graph window (seconds)**: Time window to display in the historical graphs
- **Temperature display**:
  - **Use OctoPrint appearance setting** (default)
  - **Celsius (°C)**
  - **Celsius + Fahrenheit (°C/°F)**

### Cool-down ETA

If enabled, the plugin can estimate an ETA while heaters are cooling down (target temperature is set to 0 / off). This is useful for quickly answering “how long until it reaches a safe temperature?”.

- **Enable cool-down ETA**: Turn cool-down ETA on/off
- **Mode**:
  - **Threshold (default)**: Uses a linear fit of recent temperature history to estimate time until a configurable cool-down target is reached
  - **Ambient**: Uses a Newton cooling model to estimate time until near ambient temperature (best-effort; depends on stable measurements)
- **Cool-down targets**: Configure the target temperature per heater (tool0/bed/chamber)
- **Hysteresis / fit window**: Controls when cool-down ETA appears and how much history is used

### Advanced Settings

- **Update Interval**: Frontend refresh rate (default: 1 second)
- **History Size**: Number of temperature readings to keep (default: 60)

### Alerts & Notifications

- **Status colors**: Customize the colors used for heating/cooling/idle indicators
- **Sound alerts** (optional): Enable per-event sounds and configure volume/rate limit
- **Browser toast notifications** (optional): Enable per-event toasts and configure timeout/rate limit

### Maintenance

- **Reset profile history**: Deletes all persisted ETA history JSON files for all printer profiles (stored in OctoPrint's plugin data folder).
- **Restore defaults**: Resets only this plugin's settings back to defaults (does not delete history files).

<!-- markdownlint-disable MD033 -->

#### Settings Screenshot

<img
  src="assets/img/Temperature_ETA_settings.png"
  alt="Temperature ETA settings"
  width="666"
/>

<!-- markdownlint-enable MD033 -->

### Settings Defaults

The following defaults apply to the user-editable plugin settings:

| Setting                  | Key                               | Default     |
| ------------------------ | --------------------------------- | ----------- |
| Enable Temperature ETA   | `enabled`                         | `true`      |
| Hide ETA while printing  | `suppress_while_printing`         | `false`     |
| Show in sidebar          | `show_in_sidebar`                 | `true`      |
| Show in navbar           | `show_in_navbar`                  | `true`      |
| Show in tab              | `show_in_tab`                     | `true`      |
| Show progress bars       | `show_progress_bars`              | `true`      |
| Show historical graph    | `show_historical_graph`           | `true`      |
| Graph window (seconds)   | `historical_graph_window_seconds` | `180`       |
| Temperature display      | `temp_display`                    | `octoprint` |
| Heating threshold        | `threshold_start`                 | `5.0 °C`    |
| Threshold unit           | `threshold_unit`                  | `octoprint` |
| Algorithm                | `algorithm`                       | `linear`    |
| Update Interval          | `update_interval`                 | `1.0 s`     |
| History Size             | `history_size`                    | `60`        |
| Enable cool-down ETA     | `enable_cooldown_eta`             | `true`      |
| Cool-down mode           | `cooldown_mode`                   | `threshold` |
| Enable debug logging     | `debug_logging`                   | `false`     |
| Color mode               | `color_mode`                      | `bands`     |
| Heating color            | `color_heating`                   | `#5cb85c`   |
| Cooling color            | `color_cooling`                   | `#337ab7`   |
| Idle color               | `color_idle`                      | `#777777`   |
| Enable sound alerts      | `sound_enabled`                   | `false`     |
| Sound: target reached    | `sound_target_reached`            | `false`     |
| Sound: cool-down done    | `sound_cooldown_finished`         | `false`     |
| Sound volume             | `sound_volume`                    | `0.5`       |
| Sound min interval       | `sound_min_interval_s`            | `10.0 s`    |
| Enable toast alerts      | `notification_enabled`            | `false`     |
| Toast: target reached    | `notification_target_reached`     | `false`     |
| Toast: cool-down done    | `notification_cooldown_finished`  | `false`     |
| Toast timeout            | `notification_timeout_s`          | `6.0 s`     |
| Toast min interval       | `notification_min_interval_s`     | `10.0 s`    |

## How It Works

1. **Temperature Monitoring**: Plugin registers for temperature callbacks (~2Hz frequency)
2. **Rate Calculation**: Analyzes temperature history to determine heating rate (°C/second)
3. **ETA Estimation**: Uses selected algorithm (linear/exponential) to predict time to target
4. **Display Update**: Sends countdown to frontend via WebSocket (1Hz default)
5. **Smart Thresholds**: Only shows ETA when heating and within configured threshold

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
5. For local development scripts (setup, restart helper, post-commit build hook), see [.development/README.md](.development/README.md).
6. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
7. Please follow our [Code of Conduct](CODE_OF_CONDUCT.md).
   Note: `main` is protected on GitHub, so changes go through PRs.

## License

AGPLv3 - See [LICENSE](LICENSE) for details.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Ajimaru/OctoPrint-TempETA/issues)
- 💬 **Discussion**: [OctoPrint Community Forum](https://community.octoprint.org/)

For logs and troubleshooting, enable "debug logging" in the plugin settings.

## Credits

- **Original Request**: [Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469) by [@CptanPanic](https://github.com/CptanPanic) (2014)
- **Development**: Built following [OctoPrint Plugin Guidelines](https://docs.octoprint.org/en/latest/plugins/index.html)
- **Contributors**: See [AUTHORS.md](AUTHORS.md)

---

**Like this plugin?** ⭐ Star the repo and share it with the OctoPrint community!
