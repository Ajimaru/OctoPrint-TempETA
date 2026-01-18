/**
 * Non-runtime JSDoc-only file for TempETA frontend.
 *
 * This file contains typedefs and high-level documentation used solely for
 * generating JavaScript API docs. It is intentionally separated from the
 * runtime `temp_eta.js` to avoid modifying code that executes in OctoPrint.
 *
 * Do NOT import this file at runtime; it exists only for documentation tools.
 */

/**
 * @typedef {Object} Heater
 * @property {string} name - heater id (e.g. 'tool0', 'bed')
 * @property {Function|number|null} actual - current temperature observable or number
 * @property {Function|number|null} target - target temperature observable or number
 * @property {Function|number|null} [cooldownTarget]
 * @property {Function|string|null} [etaKind]
 * @property {Array<HeaterHistoryEntry>} [_history]
 * @property {number} [_historyStart]
 */

/**
 * @typedef {Object} HeaterHistoryEntry
 * @property {number} t - epoch seconds of sample
 * @property {number} a - actual temp
 * @property {number|null} [tg] - recorded target
 */

/**
 * @typedef {Object} PluginSettings
 * @property {string} [color_mode]
 * @property {boolean} [show_in_sidebar]
 * @property {boolean} [show_in_navbar]
 * @property {boolean} [show_in_tab]
 * @property {number} [historical_graph_window_seconds]
 * @property {boolean} [debug_logging]
 */

/**
 * @typedef {Object} SoundConfig
 * @property {boolean} enabled
 * @property {number} volume
 * @property {Array<string>} files
 */

/**
 * @typedef {Object} PluginMessage
 * @property {string} type
 * @property {string} [heater]
 * @property {number} [eta]
 * @property {string} [eta_kind]
 * @property {number|null} [cooldown_target]
 * @property {number|null} [actual]
 * @property {number|null} [target]
 */

/**
 * High-level documented surface of the TempETA view model.
 *
 * @class TempETAViewModel
 * @description Knockout view model for the Temperature ETA plugin.
 * The runtime implementation lives in `temp_eta.js`; this file provides
 * non-invasive JSDoc typedefs and an overview for documentation generation.
 */
function TempETAViewModel() {}

/**
 * Called when the settings dialog is shown.
 * @param {HTMLElement} dialog - The settings dialog element.
 * @returns {void}
 */
TempETAViewModel.prototype.onSettingsShown = function (dialog) {};

/**
 * Called when the settings dialog is hidden.
 * @returns {void}
 */
TempETAViewModel.prototype.onSettingsHidden = function () {};

/**
 * Handle incoming plugin messages delivered by OctoPrint's data updater.
 * @param {string} plugin
 * @param {PluginMessage} msg - The incoming plugin message payload.
 * @returns {void}
 */
TempETAViewModel.prototype.onDataUpdaterPluginMessage = function (plugin, msg) {};

/**
 * Return a user-facing label for a heater id.
 * @param {string} heaterId
 * @returns {string}
 */
TempETAViewModel.prototype.getHeaterLabel = function (heaterId) {};

/**
 * Whether the ETA should be visible for a given heater.
 * @param {number|null|undefined} eta
 * @returns {boolean}
 */
TempETAViewModel.prototype.isETAVisible = function (eta) {};

/**
 * Compute a progress percentage (0-100) for the heater towards its target.
 * @param {Heater} heater
 * @returns {number}
 */
TempETAViewModel.prototype.getProgressPercent = function (heater) {};
