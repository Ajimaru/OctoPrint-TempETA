
## `TempETAViewModel`

Knockout view model used by the plugin frontend. This is the primary JavaScript
API surface users of the OctoPrint view model system will interact with.

### Constructor

`new TempETAViewModel(parameters)`

- parameters: Array — OctoPrint-injected view models in the usual order
	(settingsViewModel, printerState, printerProfiles, loginState, ...)

### Description

`TempETAViewModel` wires the plugin settings and the OctoPrint UI together,
providing methods for binding the settings dialog, handling reset/restore
actions, and publishing simple API commands. The view model is registered
with OctoPrint and is the recommended entry point for UI integrations.

### Public methods (selection)

- `bind` / `applyBindings` — Bind the view model to the settings dialog (implicit)
- `publish reset_profile_history` — Triggers the plugin API command to clear persisted history
- `publish reset_settings_defaults` — Restores plugin settings to defaults

For further implementation details, see the source file:
[octoprint_temp_eta/static/js/temp_eta.js](octoprint_temp_eta/static/js/temp_eta.js#L1-L200)
