# OctoPrint-TempETA Developer Documentation

Welcome to the OctoPrint Temperature ETA Plugin developer documentation.

## Overview

OctoPrint-TempETA is an OctoPrint plugin that displays real-time estimated time of arrival (ETA) for printer heating and cooling operations. This addresses the longstanding [Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469) from the OctoPrint project.

## Key Features

- **Real-time ETA calculation** for bed, hotend, and chamber temperature changes
- **Linear and exponential algorithms** for accurate predictions
- **MQTT integration** for external monitoring
- **Internationalization support** (English and German)
- **Configurable settings** for customization
- **Modern UI** with Knockout.js integration

## Quick Links

- [Getting Started](getting-started.md) - Installation and basic setup
- [Architecture Overview](architecture/overview.md) - System design and components
- [Python API](api/python.md) - Backend API reference
- [JavaScript API](api/javascript.md) - Frontend API reference
- [Contributing Guide](development/contributing.md) - How to contribute

## Technology Stack

- **Backend**: Python 3.11+ with OctoPrint plugin framework
- **Frontend**: JavaScript with Knockout.js
- **Communication**: MQTT (optional)
- **Build**: setuptools, pytest
- **Documentation**: MkDocs Material

## Project Information

- **Repository**: [Ajimaru/OctoPrint-TempETA](https://github.com/Ajimaru/OctoPrint-TempETA)
- **License**: AGPLv3
- **OctoPrint Version**: 1.12.0+
- **Python Version**: 3.11+

## For Users

If you're looking for end-user documentation on how to install and use the plugin, please refer to the [README.md](https://github.com/Ajimaru/OctoPrint-TempETA/blob/main/README.md) in the repository.

This documentation is intended for developers who want to:

- Understand the plugin architecture
- Contribute code or features
- Extend the plugin
- Debug issues
- Create integrations
