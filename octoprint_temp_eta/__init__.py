# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin


class TempETAPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
):
    """Main plugin implementation for Temperature ETA.
    
    Implements OctoPrint Issue #469: Show estimated time remaining
    for printer heating (bed, hotend, chamber).
    """

    def on_after_startup(self):
        """Called after OctoPrint startup, logs plugin initialization."""
        self._logger.info("Temperature ETA Plugin started")

    # SettingsPlugin mixin
    def get_settings_defaults(self):
        """Return the default settings for the plugin.

        Returns:
            dict: Dictionary containing default plugin settings.
        """
        return dict(
            enabled=True,
            threshold_start=10.0,
            algorithm="linear",
            update_interval=1.0,
            history_size=60,
        )

    # TemplatePlugin mixin
    def get_template_configs(self):
        """Configure which templates to use and how to bind them.

        Returns:
            list: List of template configuration dictionaries.
        """
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False),
            dict(type="tab", custom_bindings=False),
        ]

    # AssetPlugin mixin
    def get_assets(self):
        """Return static assets (JS, CSS, LESS) to be included.

        Returns:
            dict: Dictionary with asset types and their file paths.
        """
        return dict(
            js=["js/temp_eta.js"],
            css=["css/temp_eta.css"],
            less=["less/temp_eta.less"],
        )

    # Softwareupdate hook
    def get_update_information(self):
        """Provide update information for the Software Update plugin.

        Returns:
            dict: Update configuration for the plugin.
        """
        return dict(
            temp_eta=dict(
                displayName="Temperature ETA Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="yourusername",
                repo="OctoPrint-TempETA",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/yourusername/OctoPrint-TempETA/archive/{target_version}.zip",
            )
        )


__plugin_name__ = "Temperature ETA"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = TempETAPlugin()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
