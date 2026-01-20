---
layout: plugin

id: temp_eta
title: Temperature ETA
description: Show real-time ETA for your printer's bed, hotend, or chamber heating and cooling.
authors:
- Ajimaru
license: AGPLv3

date: 2026-01-15

homepage: https://github.com/Ajimaru/OctoPrint-TempETA
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

  python: ">=3.11,<4"

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

## How It Works

1. **Temperature Monitoring**: Plugin registers for temperature callbacks (~2Hz frequency)
2. **Rate Calculation**: Analyzes temperature history to determine heating rate (°C/second)
3. **ETA Estimation**: Uses selected algorithm (linear/exponential) to predict time to target
4. **Display Update**: Sends countdown to frontend via WebSocket (1Hz default)
5. **Smart Thresholds**: Only shows ETA when heating or cooling and within configured threshold

## Origin Story

This plugin implements a feature request from 2014 ([OctoPrint Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469))
by [@CptanPanic](https://github.com/CptanPanic) to show estimated time remaining for printer heating.

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
