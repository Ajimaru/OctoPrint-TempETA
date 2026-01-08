/*
 * View model for OctoPrint Temperature ETA Plugin
 *
 * Implements Issue #469: Temperature countdown/ETA display
 * Author: Your Name
 * License: AGPLv3
 */
$(function() {
    function TempETAViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];

        // TODO: Implement your plugin's view model here.
        
        self.onBeforeBinding = function() {
            // Called before the view model is bound to the DOM
        };
        
        self.onAfterBinding = function() {
            // Called after the view model is bound to the DOM
        };
    }

    // This is how our plugin registers itself with the application
    OCTOPRINT_VIEWMODELS.push({
        construct: TempETAViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_plugin_temp_eta", "#navbar_plugin_temp_eta", "#settings_plugin_temp_eta"]
    });
});
