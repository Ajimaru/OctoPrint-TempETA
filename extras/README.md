# Plugin Registration Files

This directory contains the registration file for the OctoPrint Plugin Repository.

## File: temp_eta.md

This is the plugin registration file required to list the Temperature ETA plugin on [plugins.octoprint.org](https://plugins.octoprint.org).

### Registration Process

To register this plugin on the OctoPrint Plugin Repository:

1. **Fork the Plugin Repository**
   - Go to https://github.com/OctoPrint/plugins.octoprint.org
   - Click "Fork" to create your own copy

2. **Add Your Plugin File**
   - Copy `extras/temp_eta.md` from this repository
   - Place it in the `_plugins` directory of your forked repository
   - The filename should remain `temp_eta.md`

3. **Provide Screenshots**
   - The plugin repository will host screenshots at `/assets/img/plugins/temp_eta/`
   - You'll need to provide the following screenshots from `assets/img/`:
     - `Temperature_ETA_heating.png`
     - `Temperature_ETA_cooling.png`
     - `Temperature_ETA_settings.png`
   - These should be included in your pull request to the plugin repository

4. **Create a Pull Request**
   - Commit your changes to your fork
   - Create a Pull Request to the main OctoPrint plugins repository
   - Use a clear PR title like: "Add Temperature ETA plugin"
   - In the PR description, reference this repository and confirm you meet the requirements

5. **Wait for Review**
   - The OctoPrint team will review your submission
   - They may request changes or clarifications
   - Once approved, your plugin will appear on plugins.octoprint.org

### Requirements Checklist

Before submitting, ensure:

- ✅ Plugin is actively maintained
- ✅ Code follows OctoPrint plugin guidelines
- ✅ No unauthorized system modifications on install
- ✅ Privacy policy included (for MQTT feature)
- ✅ All external connections use HTTPS (MQTT is user-configured)
- ✅ Clear documentation and installation instructions
- ✅ Plugin is properly packaged and distributable via pip

### Registration File Contents

The `temp_eta.md` file contains:

- **Metadata**: Plugin ID, title, description, authors, license
- **Links**: Homepage, source repository, archive URL
- **Compatibility**: OctoPrint and Python version requirements
- **Tags**: Keywords for plugin discovery
- **Screenshots**: References to plugin UI images
- **Documentation**: Features, installation, configuration, and usage
- **Privacy Statement**: Data handling for MQTT integration

### Updating the Registration

If you need to update the plugin listing after registration:

1. Update `extras/temp_eta.md` in this repository
2. Submit a PR to the plugins.octoprint.org repository with the updated file
3. Changes will appear after the PR is merged and the site is rebuilt

### References

- [OctoPrint Plugin Registration Guide](https://plugins.octoprint.org/help/registering/)
- [OctoPrint Plugin Development Docs](https://docs.octoprint.org/en/main/plugins/)
- [Plugin Repository GitHub](https://github.com/OctoPrint/plugins.octoprint.org)

### Maintenance Commitment

By registering this plugin, you commit to:

- Keep the plugin updated with OctoPrint API changes
- Fix bugs and security issues promptly
- Handle user bug reports and feature requests
- Maintain compatibility with supported Python and OctoPrint versions
- Communicate clearly if you can no longer maintain the plugin

### Questions?

If you have questions about the registration process:

- Review the [registration guidelines](https://plugins.octoprint.org/help/registering/)
- Check the [OctoPrint Community Forum](https://community.octoprint.org/)
- Look at existing plugin registrations in the [plugins repository](https://github.com/OctoPrint/plugins.octoprint.org/tree/gh-pages/_plugins)
