# OctoPrint Temperature ETA Plugin

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/Ajimaru/OctoPrint-TempETA/releases)
[![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![OctoPrint](https://img.shields.io/badge/OctoPrint-1.4.0%2B-blue.svg)](https://octoprint.org)

**Implements [OctoPrint Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469)**: Show estimated time remaining for printer heating.

Display real-time countdown/ETA when your 3D printer's bed, hotend, or chamber is heating up. No more guessing how long until your print starts!

## Features

- ⏱️ **Real-time ETA countdown** for bed and hotend heating
- 🌡️ **Smart calculation algorithms**: Linear (default) and exponential models
- 📊 **Flexible display**: Show ETA in navbar, sidebar, or both
- 🎛️ **Configurable thresholds**: Start countdown when X°C below target
- 🌍 **Internationalization**: English and German included, easily extensible
- 🚀 **Lightweight**: Minimal performance impact (~2Hz monitoring)
- 🔧 **Per-heater configuration**: Enable/disable for tool0, bed, chamber
- 📱 **Responsive design**: Works on desktop and mobile

## Installation

### Via Plugin Manager (Recommended)

1. Open OctoPrint web interface
2. Navigate to **Settings** → **Plugin Manager**
3. Click **Get More...**
4. Search for "Temperature ETA" or use this URL:
   ```
   https://github.com/yourusername/OctoPrint-TempETA/archive/main.zip
   ```
5. Click **Install**
6. Restart OctoPrint

### Manual Installation

```bash
pip install https://github.com/yourusername/OctoPrint-TempETA/archive/main.zip
```

## Configuration

After installation, configure the plugin in **Settings** → **Temperature ETA**:

### Basic Settings

- **Enable Plugin**: Toggle ETA calculation on/off
- **Start Threshold**: Begin countdown when temperature is X°C below target (default: 10°C)
- **Calculation Algorithm**:
  - **Linear** (default): Assumes constant heating rate, simple and fast
  - **Exponential**: Accounts for thermal asymptotic behavior, more accurate
- **Display Location**: Show ETA in navbar, sidebar, or both

### Heater Configuration

Enable/disable and customize display names for:

- **Tool 0** (Hotend): Default enabled as "Hotend"
- **Bed**: Default enabled as "Bed"
- **Chamber**: Default disabled

### Advanced Settings

- **Update Interval**: Frontend refresh rate (default: 1 second)
- **History Size**: Number of temperature readings to keep (default: 100)

## How It Works

1. **Temperature Monitoring**: Plugin registers for temperature callbacks (~2Hz frequency)
2. **Rate Calculation**: Analyzes temperature history to determine heating rate (°C/second)
3. **ETA Estimation**: Uses selected algorithm (linear/exponential) to predict time to target
4. **Display Update**: Sends countdown to frontend via WebSocket (1Hz default)
5. **Smart Thresholds**: Only shows ETA when heating and within configured threshold

### Algorithms

**Linear Algorithm** (Default)

- Assumes constant heating rate based on recent measurements
- Fast and simple
- Best for: Initial heating phase, stable environments

**Exponential Algorithm** (Advanced)

- Models thermal asymptotic behavior (approaching ambient temperature)
- More accurate for extended heating
- Best for: High-temperature targets, variable environments

## Development

This plugin follows the [OctoPrint Contributing Guidelines](https://github.com/OctoPrint/OctoPrint/blob/main/CONTRIBUTING.md).

### Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/OctoPrint-TempETA.git
cd OctoPrint-TempETA
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[develop]"
pre-commit install

# Test and check
pytest
pre-commit run --all-files
```

### Key Files

- `octoprint_temp_eta/__init__.py` - Main plugin logic
- `octoprint_temp_eta/static/js/temp_eta.js` - Frontend ViewModel
- `octoprint_temp_eta/templates/*.jinja2` - UI templates
- `.github/copilot-instructions.md` - AI coding guidelines
- `tests/` - Unit and integration tests

**See [.github/copilot-instructions.md](.github/copilot-instructions.md) for detailed development guidelines.**

## FAQ

**Q: Why does the ETA jump around?**  
A: Temperature changes aren't perfectly linear. The plugin uses recent data to calculate rate. Longer threshold values provide more stable estimates.

**Q: Can I use this with multiple hotends?**  
A: Currently supports tool0. Multi-tool support is planned for future releases.

**Q: Does this work with chamber heaters?**  
A: Yes! Enable chamber in settings if your printer has a chamber heater.

**Q: Will this slow down my prints?**  
A: No. The plugin uses efficient algorithms and runs in a separate thread. Impact is negligible.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b wip/my-feature`
3. Follow coding standards (see `.github/copilot-instructions.md`)
4. Write tests for new features
5. Submit a pull request

## License

AGPLv3 - See [LICENSE](LICENSE) for details.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/OctoPrint-TempETA/issues)
- 💬 **Discussion**: [OctoPrint Community Forum](https://community.octoprint.org/)
- 📧 **Email**: your.email@example.com

## Credits

- **Original Request**: [Issue #469](https://github.com/OctoPrint/OctoPrint/issues/469) by [@CptanPanic](https://github.com/CptanPanic) (2014)
- **Development**: Built following [OctoPrint Plugin Guidelines](https://docs.octoprint.org/en/main/plugins/index.html)
- **Contributors**: See [AUTHORS.md](AUTHORS.md)

---

**Like this plugin?** ⭐ Star the repo and share it with the OctoPrint community!
