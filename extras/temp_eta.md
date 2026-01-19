---
layout: plugin

id: temp_eta
title: Temperature ETA
description: Display real-time countdown/ETA when your 3D printer's bed, hotend, or chamber is heating up or cooling down. No more guessing how long until your print starts or is ready for maintenance!
authors:
- Ajimaru
license: AGPLv3

date: 2026-01-15

homepage: https://ajimaru.github.io/OctoPrint-TempETA
source: https://github.com/Ajimaru/OctoPrint-TempETA
archive: https://github.com/Ajimaru/OctoPrint-TempETA/archive/{target_version}.zip

tags:
- temperature
- eta
- heating
- cooling
- countdown
- monitoring
- ui

screenshots:
- url: /assets/img/plugins/temp_eta/Temperature_ETA_heating.png
  alt: Heating ETA display showing countdown
  caption: Real-time heating ETA countdown
- url: /assets/img/plugins/temp_eta/Temperature_ETA_cooling.png
  alt: Cooling ETA display
  caption: Cool-down ETA estimation
- url: /assets/img/plugins/temp_eta/Temperature_ETA_settings.png
  alt: Plugin settings interface
  caption: Comprehensive settings panel

featuredimage: /assets/img/plugins/temp_eta/Temperature_ETA_heating.png

compatibility:
  octoprint:
  - 1.10.2

  python: ">=3.07,<4"

---

## Temperature ETA Plugin for OctoPrint

Display real-time countdown/ETA when your 3D printer's bed, hotend, or chamber is heating up or cooling down.
No more guessing how long until your print starts or is ready for maintenance!

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

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

```url
https://github.com/Ajimaru/OctoPrint-TempETA/archive/main.zip
```

## Configuration

After installation, configure the plugin in **Settings** → **Temperature ETA**:

### General

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

### Heating ETA

- **Enable heating ETA**: Controls whether heating ETAs are shown/calculated
- **Heating threshold** + **Threshold unit**: Start ETA when within a configured delta to the target
- **Calculation algorithm**: Linear (default) or exponential

### Cool-down ETA

- **Enable cool-down ETA**: Turn cool-down ETA on/off
- **Mode**:
  - **Threshold target (default)**: Estimate time until a fixed, per-heater target is reached
  - **Ambient-based target**: Estimate time until near ambient temperature (best-effort)
- **Cool-down targets**: Configure per-heater targets (tool0/bed/chamber) for threshold mode
- **Ambient temperature** (optional): Provide a fixed ambient value for ambient mode
- **Hysteresis / fit window**: Controls when cool-down ETA disappears and how much recent data is used

### MQTT

- **Enable MQTT**: Master switch for MQTT integration (publishes ETA data to external broker)
- **Broker Host**: MQTT broker hostname or IP address
- **Broker Port**: MQTT broker port (default: 1883)
- **Username/Password**: Optional authentication credentials
- **Use TLS/SSL**: Enable encrypted connection
- **Base Topic**: Root MQTT topic for publishing messages (default: `octoprint/temp_eta`)
- **QoS**: MQTT Quality of Service level
- **Retain Messages**: Enable MQTT retain flag
- **Publish Interval**: Minimum seconds between MQTT publishes

## How It Works

1. **Temperature Monitoring**: Plugin registers for temperature callbacks (~2Hz frequency)
2. **Rate Calculation**: Analyzes temperature history to determine heating rate (°C/second)
3. **ETA Estimation**: Uses selected algorithm (linear/exponential) to predict time to target
4. **Display Update**: Sends countdown to frontend via WebSocket (1Hz default)
5. **Smart Thresholds**: Only shows ETA when heating or cooling and within configured threshold

## MQTT Integration

When MQTT is enabled, the plugin publishes temperature ETA updates and state changes to your MQTT broker.
This allows integration with home automation systems like Home Assistant, Node-RED, or any MQTT-compatible platform.

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

## Origin Story

This plugin implements a feature request from 2014 ([OctoPrint Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469))
by [@CptanPanic](https://github.com/CptanPanic) to show estimated time remaining for printer heating.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Ajimaru/OctoPrint-TempETA/issues)
- 💬 **Discussion**: [OctoPrint Community Forum](https://community.octoprint.org/)
- 📖 **Documentation**: [Full Documentation](https://ajimaru.github.io/OctoPrint-TempETA/)

## Privacy & Data

This plugin optionally connects to external services only when explicitly enabled:

- **MQTT Integration** (optional, disabled by default): When enabled, publishes temperature data to your configured MQTT broker. No data is sent to any third-party service without your explicit configuration.

The plugin does not:

- Collect or transmit any personal information
- Connect to any external services by default
- Require internet connectivity to function
- Track usage or analytics

All temperature history data is stored locally in OctoPrint's plugin data folder.

---

**Like this plugin?** ⭐ Star the repo and share it with the OctoPrint community!
