/*
 * View model for OctoPrint Temperature ETA Plugin
 *
 * Implements Issue #469: Temperature countdown/ETA display
 * Author: AjimaruGDR
 * License: AGPLv3
 */
$(function () {
  function _attrOr($el, name, fallback) {
    var v = $el && $el.length ? $el.attr(name) : null;
    if (v === undefined || v === null || v === "") {
      return fallback;
    }
    return v;
  }

  function _notify(type, title, text) {
    if (window.PNotify) {
      new PNotify({ title: title, text: text, type: type });
    } else {
      window.alert(title + "\n" + text);
    }
  }

  function _confirmAction(title, text, onYes, onNo) {
    try {
      if (typeof window.showConfirmationDialog === "function") {
        // OctoPrint UI helper (if available)
        window.showConfirmationDialog({
          title: title,
          message: text,
          onproceed: function () {
            onYes();
          },
          oncancel: function () {
            if (typeof onNo === "function") {
              onNo();
            }
          },
        });
        return;
      }
    } catch (e) {
      // Fall back to window.confirm
    }

    var ok = window.confirm(title + "\n\n" + text);
    if (ok) {
      onYes();
    } else if (typeof onNo === "function") {
      onNo();
    }
  }

  // Settings button handler. We keep this as a delegated event handler so it
  // works regardless of how the settings template is bound.
  $(document).on("click", "#temp_eta_reset_profile_history", function (e) {
    e.preventDefault();

    var $btn = $(this);

    var notifyTitle = _attrOr($btn, "data-notify-title", "TempETA");
    var confirmTitle = _attrOr($btn, "data-confirm-title", notifyTitle);
    var confirmText = _attrOr($btn, "data-confirm-text", "Are you sure?");
    var successTitle = _attrOr($btn, "data-success-title", notifyTitle);
    var successGeneric = _attrOr($btn, "data-success-text-generic", "Done.");
    var successWithCount = _attrOr(
      $btn,
      "data-success-text-with-count",
      "Deleted ({count}).",
    );
    var successNone = _attrOr(
      $btn,
      "data-success-text-none",
      "Nothing to delete.",
    );
    var errorTitle = _attrOr($btn, "data-error-title", notifyTitle);
    var errorText = _attrOr($btn, "data-error-text", "Failed.");
    var errorNoApi = _attrOr(
      $btn,
      "data-error-no-api",
      "OctoPrint API not available.",
    );

    _confirmAction(confirmTitle, confirmText, function () {
      $btn.prop("disabled", true);

      if (!window.OctoPrint || !OctoPrint.simpleApiCommand) {
        _notify("error", errorTitle, errorNoApi);
        $btn.prop("disabled", false);
        return;
      }

      OctoPrint.simpleApiCommand("temp_eta", "reset_profile_history", {})
        .done(function (resp) {
          if (resp && resp.success) {
            var deletedFiles =
              typeof resp.deleted_files === "number"
                ? resp.deleted_files
                : null;
            if (deletedFiles === null) {
              _notify("success", successTitle, successGeneric);
            } else if (deletedFiles > 0) {
              _notify(
                "success",
                successTitle,
                successWithCount.replace("{count}", String(deletedFiles)),
              );
            } else {
              _notify("success", successTitle, successNone);
            }
          } else {
            _notify("error", errorTitle, errorText);
          }
        })
        .fail(function () {
          _notify("error", errorTitle, errorText);
        })
        .always(function () {
          $btn.prop("disabled", false);
        });
    });
  });

  $(document).on("click", "#temp_eta_restore_defaults", function (e) {
    e.preventDefault();

    var $btn = $(this);
    var notifyTitle = _attrOr($btn, "data-notify-title", "TempETA");
    var confirmTitle = _attrOr($btn, "data-confirm-title", notifyTitle);
    var confirmText = _attrOr($btn, "data-confirm-text", "Are you sure?");
    var successTitle = _attrOr($btn, "data-success-title", notifyTitle);
    var successText = _attrOr($btn, "data-success-text", "Done.");
    var errorTitle = _attrOr($btn, "data-error-title", notifyTitle);
    var errorText = _attrOr($btn, "data-error-text", "Failed.");
    var errorNoApi = _attrOr(
      $btn,
      "data-error-no-api",
      "OctoPrint API not available.",
    );

    _confirmAction(confirmTitle, confirmText, function () {
      $btn.prop("disabled", true);

      if (!window.OctoPrint || !OctoPrint.simpleApiCommand) {
        _notify("error", errorTitle, errorNoApi);
        $btn.prop("disabled", false);
        return;
      }

      OctoPrint.simpleApiCommand("temp_eta", "reset_settings_defaults", {})
        .done(function (resp) {
          if (resp && resp.success) {
            // Message may be provided by backend, but we prefer i18n text from template.
            _notify("success", successTitle, successText);
          } else {
            _notify("error", errorTitle, errorText);
          }
        })
        .fail(function () {
          _notify("error", errorTitle, errorText);
        })
        .always(function () {
          $btn.prop("disabled", false);
        });
    });
  });

  function TempETAViewModel(parameters) {
    var self = this;

    function _gettext(msgid) {
      if (
        typeof window !== "undefined" &&
        typeof window.gettext === "function"
      ) {
        return window.gettext(msgid);
      }

      if (typeof gettext === "function") {
        return gettext(msgid);
      }

      return msgid;
    }

    self.settingsViewModel = parameters[0];
    self.loginState = parameters[3] || null;
    self.isAdmin = ko.pureComputed(function () {
      try {
        if (self.loginState && typeof self.loginState.isAdmin === "function") {
          return !!self.loginState.isAdmin();
        }
      } catch (e) {
        // ignore
      }
      return false;
    });
    self._resolveSettingsRoot = function () {
      // OctoPrint versions can differ in how the settings model is nested.
      // We want an object where `plugins.temp_eta.*` and `appearance.*` exist.
      var s = null;
      try {
        s = self.settingsViewModel && self.settingsViewModel.settings;
        if (typeof s === "function") {
          s = s();
        }
      } catch (e) {
        s = null;
      }

      if (s && s.plugins) {
        return s;
      }
      if (s && s.settings && s.settings.plugins) {
        return s.settings;
      }

      return {};
    };

    // Expose the actual settings data object as `settings` so the settings template
    // can use `settings.plugins.temp_eta.*` even when custom bindings are enabled.
    self.settings = self._resolveSettingsRoot();
    self.printerState = parameters[1];
    self.printerProfiles = parameters[2];

    self._bindSettingsIfNeeded = function () {
      // With custom_bindings=True the settings template is injected lazily when the
      // settings dialog opens. Bind it then, and guard against double-binding.
      self.settings = self._resolveSettingsRoot();
      var $root = $("#settings_plugin_temp_eta");
      if (!$root.length) {
        $root = $(".temp-eta-settings");
      }
      if (!$root.length) {
        return;
      }

      var rootEl = $root.get(0);
      if ($(rootEl).data("tempEtaKoBound")) {
        return;
      }

      try {
        ko.applyBindings(self, rootEl);
        $(rootEl).data("tempEtaKoBound", true);
      } catch (e) {
        // Ignore binding errors; OctoPrint may re-render parts of the dialog.
        // Keeping this quiet avoids spamming the log for transient timing issues.
      }
    };

    self._unbindSettingsIfBound = function () {
      var $root = $("#settings_plugin_temp_eta");
      if (!$root.length) {
        $root = $(".temp-eta-settings");
      }
      if (!$root.length) {
        return;
      }
      var rootEl = $root.get(0);
      if (!$(rootEl).data("tempEtaKoBound")) {
        return;
      }
      try {
        ko.cleanNode(rootEl);
      } catch (e) {}
      $(rootEl).removeData("tempEtaKoBound");
    };

    self._bindSettingsWithRetry = function () {
      // The settings content is injected lazily; retry a few times to catch it.
      var attempts = 0;
      var maxAttempts = 10;
      var delayMs = 50;

      var tick = function () {
        attempts += 1;
        self._bindSettingsIfNeeded();

        var $root = $("#settings_plugin_temp_eta");
        if (!$root.length) {
          $root = $(".temp-eta-settings");
        }
        if ($root.length && $root.data("tempEtaKoBound")) {
          return;
        }

        if (attempts < maxAttempts) {
          window.setTimeout(tick, delayMs);
        }
      };

      tick();
    };

    self._bindElementOnce = function (
      selector,
      dataFlag,
      maxAttempts,
      delayMs,
    ) {
      var attempts = 0;
      var maxA = typeof maxAttempts === "number" ? maxAttempts : 10;
      var delay = typeof delayMs === "number" ? delayMs : 100;

      var tick = function () {
        attempts += 1;

        var $root = $(selector);
        if ($root.length) {
          var el = $root.get(0);
          if (!$(el).data(dataFlag)) {
            try {
              ko.applyBindings(self, el);
              $(el).data(dataFlag, true);
            } catch (e) {}
          }
          if ($(el).data(dataFlag)) {
            return;
          }
        }

        if (attempts < maxA) {
          window.setTimeout(tick, delay);
        }
      };

      tick();
    };

    self._installSettingsDialogHooks = function () {
      if (self._settingsDialogHooksInstalled) {
        return;
      }
      self._settingsDialogHooksInstalled = true;

      // Bootstrap modal events differ between versions; listen to both.
      $(document).on("shown", "#settings_dialog", function () {
        self._bindSettingsWithRetry();
      });
      $(document).on("shown.bs.modal", "#settings_dialog", function () {
        self._bindSettingsWithRetry();
      });

      $(document).on("hidden", "#settings_dialog", function () {
        self._unbindSettingsIfBound();
      });
      $(document).on("hidden.bs.modal", "#settings_dialog", function () {
        self._unbindSettingsIfBound();
      });
    };

    self._ensureSidebarBound = function () {
      // Sidebar DOM can be injected after the initial viewmodel binding;
      // bind it lazily and only once.
      self._bindElementOnce(
        "#sidebar_plugin_temp_eta",
        "tempEtaKoBoundSidebar",
        10,
        200,
      );
    };

    self._throttledEnsureSidebarBound = (function () {
      var last = 0;
      return function () {
        var now = Date.now();
        if (now - last < 1000) {
          return;
        }
        last = now;
        self._ensureSidebarBound();
        self._applyComponentVisibility();
      };
    })();

    // Dynamic storage for all heaters
    // Maps heater name to {eta, actual, target} observables
    self.heaters = ko.observableArray([]);
    self.heaterData = {}; // Maps heater name to {eta, actual, target}

    self._isFrontendDebugEnabled = function () {
      var ps = self._pluginSettings();
      if (!ps || !ps.debug_logging) {
        return false;
      }
      try {
        return typeof ps.debug_logging === "function"
          ? !!ps.debug_logging()
          : !!ps.debug_logging;
      } catch (e) {
        return false;
      }
    };

    self._debugLog = (function () {
      var lastByKey = {};
      return function (key, message, payload, minIntervalMs) {
        if (!self._isFrontendDebugEnabled()) {
          return;
        }

        var now = Date.now();
        var last = lastByKey[key] || 0;
        var interval =
          typeof minIntervalMs === "number" ? minIntervalMs : 30000;
        if (now - last < interval) {
          return;
        }
        lastByKey[key] = now;

        try {
          if (payload !== undefined) {
            console.debug(message, payload);
          } else {
            console.debug(message);
          }
        } catch (e) {}
      };
    })();

    function readKoBool(value, defaultValue) {
      try {
        if (typeof value === "function") {
          return !!value();
        }
        if (value === undefined || value === null) {
          return !!defaultValue;
        }
        if (value === true || value === false) {
          return value;
        }
        if (typeof value === "string") {
          var v = value.toLowerCase();
          if (v === "true" || v === "1") return true;
          if (v === "false" || v === "0") return false;
        }
        if (typeof value === "number") {
          return value === 1;
        }
      } catch (e) {}
      return !!defaultValue;
    }

    self._pluginSettings = function () {
      try {
        return (
          self.settings &&
          self.settings.plugins &&
          self.settings.plugins.temp_eta
        );
      } catch (e) {
        return null;
      }
    };

    self.isComponentEnabled = function (component) {
      var ps = self._pluginSettings();
      if (!ps) {
        return true;
      }

      var pluginEnabled = readKoBool(ps.enabled, true);
      if (!pluginEnabled) {
        return false;
      }

      if (component === "sidebar") {
        return readKoBool(ps.show_in_sidebar, true);
      }
      if (component === "navbar") {
        return readKoBool(ps.show_in_navbar, true);
      }
      if (component === "tab") {
        return readKoBool(ps.show_in_tab, true);
      }

      return true;
    };

    /**
     * Format seconds to MM:SS format
     * @param {number} seconds - Seconds to format
     * @returns {string} Formatted time string
     */
    self.formatETA = function (seconds) {
      if (!seconds || seconds <= 0) {
        return "--:--";
      }
      var mins = Math.floor(seconds / 60);
      var secs = Math.floor(seconds % 60);
      return mins + ":" + (secs < 10 ? "0" : "") + secs;
    };

    /**
     * Format temperature with one decimal place
     * @param {number} temp - Temperature value
     * @returns {string} Formatted temperature
     */
    self.formatTemp = function (temp) {
      if (!temp && temp !== 0) {
        return "--";
      }
      return Math.round(temp * 10) / 10;
    };

    self._getTempDisplayMode = function () {
      var ps = self._pluginSettings();
      if (!ps || !ps.temp_display) {
        return "octoprint";
      }
      try {
        if (typeof ps.temp_display === "function") {
          return ps.temp_display() || "octoprint";
        }
        return ps.temp_display || "octoprint";
      } catch (e) {
        return "octoprint";
      }
    };

    self._getShowFahrenheitAlso = function () {
      try {
        return (
          self.settings &&
          self.settings.appearance &&
          self.settings.appearance.showFahrenheitAlso &&
          typeof self.settings.appearance.showFahrenheitAlso === "function" &&
          !!self.settings.appearance.showFahrenheitAlso()
        );
      } catch (e) {
        return false;
      }
    };

    self.formatTempDisplay = function (temp) {
      // Prefer OctoPrint's helper if available to keep formatting consistent.
      var mode = self._getTempDisplayMode();
      var showF = false;
      if (mode === "cf") {
        showF = true;
      } else if (mode === "octoprint") {
        showF = self._getShowFahrenheitAlso();
      } else {
        showF = false;
      }

      if (typeof window.formatTemperature === "function") {
        // returnUnicode=true to avoid HTML entities in text bindings
        return window.formatTemperature(temp, showF, undefined, true);
      }

      // Fallback if helper isn't present for some reason.
      if (temp === undefined || temp === null || isNaN(temp)) {
        return "--";
      }
      var c = Math.round(temp * 10) / 10;
      if (!showF) {
        return c + "°C";
      }
      var f = Math.round(((temp * 9) / 5 + 32) * 10) / 10;
      return c + "°C (" + f + "°F)";
    };

    self._cToF = function (celsius) {
      return (celsius * 9.0) / 5.0 + 32.0;
    };

    self._fToC = function (fahrenheit) {
      return ((fahrenheit - 32.0) * 5.0) / 9.0;
    };

    self._effectiveThresholdUnit = function () {
      var ps = self._pluginSettings();
      if (!ps || !ps.threshold_unit) {
        return "c";
      }

      var raw =
        typeof ps.threshold_unit === "function"
          ? ps.threshold_unit()
          : ps.threshold_unit;
      if (raw === "octoprint") {
        var displayMode = self._getTempDisplayMode();
        if (displayMode === "cf") {
          return "f";
        }
        if (displayMode === "octoprint" && self._getShowFahrenheitAlso()) {
          return "f";
        }
        return "c";
      }
      return raw || "c";
    };

    self.thresholdUnitLabel = ko.pureComputed(function () {
      return self._effectiveThresholdUnit() === "f" ? "(°F)" : "(°C)";
    });

    self.thresholdStartDisplay = ko.pureComputed({
      read: function () {
        var ps = self._pluginSettings();
        if (!ps || !ps.threshold_start) {
          return "";
        }

        var thresholdC = parseFloat(
          typeof ps.threshold_start === "function"
            ? ps.threshold_start()
            : ps.threshold_start,
        );
        if (!isFinite(thresholdC)) {
          return "";
        }

        if (self._effectiveThresholdUnit() === "f") {
          return self._cToF(thresholdC).toFixed(1);
        }
        return thresholdC.toFixed(1);
      },
      write: function (value) {
        var ps = self._pluginSettings();
        if (
          !ps ||
          !ps.threshold_start ||
          typeof ps.threshold_start !== "function"
        ) {
          return;
        }

        var numeric = parseFloat(value);
        if (!isFinite(numeric)) {
          return;
        }

        var thresholdC =
          self._effectiveThresholdUnit() === "f"
            ? self._fToC(numeric)
            : numeric;
        ps.threshold_start(parseFloat(thresholdC.toFixed(3)));
      },
    });

    /**
     * Handle plugin messages from backend
     * @param {string} plugin - Plugin identifier
     * @param {object} data - Message data
     */
    self.onDataUpdaterPluginMessage = function (plugin, data) {
      if (plugin !== "temp_eta") {
        return;
      }

      if (data.type === "settings_reset") {
        try {
          if (
            self.settingsViewModel &&
            typeof self.settingsViewModel.requestData === "function"
          ) {
            self.settingsViewModel.requestData();
          }
        } catch (e) {
          // Ignore
        }
        // Ensure bindings are active if the dialog is open.
        self._bindSettingsIfNeeded();
        return;
      }

      if (data.type === "eta_update") {
        var heater = data.heater;
        var eta = data.eta;

        // Dynamically register heaters as they appear
        if (!self.heaterData[heater]) {
          self.heaterData[heater] = {
            name: heater,
            eta: ko.observable(null),
            actual: ko.observable(null),
            target: ko.observable(null),
          };
          self.heaters.push(self.heaterData[heater]);
          self._debugLog(
            "register_" + heater,
            "[TempETA] Registered new heater",
            heater,
            60000,
          );
        }

        // Update heater data
        self.heaterData[heater].eta(eta);
        self.heaterData[heater].actual(data.actual);
        self.heaterData[heater].target(data.target);

        // Ensure sidebar becomes visible even if it was injected late.
        self._throttledEnsureSidebarBound();
      }
    };

    /**
     * Check if ETA should be shown
     * @param {number} eta - ETA value in seconds
     * @returns {boolean} True if ETA is valid and should be shown
     */
    self.isETAVisible = function (eta) {
      return eta !== null && eta !== undefined && eta >= 1;
    };

    function toBoolFlag(value) {
      if (value === true || value === false) return value;
      if (typeof value === "string") {
        return value.toLowerCase() === "true" || value === "1";
      }
      if (typeof value === "number") {
        return value === 1;
      }
      return false;
    }

    /**
     * Check if heater is part of the active printer profile
     * @param {string} heaterName
     * @returns {boolean}
     */
    self.isHeaterSupported = function (heaterName) {
      var profile = null;

      // Prefer printerProfilesViewModel (authoritative for current profile)
      if (self.printerProfiles && self.printerProfiles.currentProfileData) {
        profile = self.printerProfiles.currentProfileData();
      }

      // Fallback to printerStateViewModel if needed
      if (
        !profile &&
        self.printerState &&
        typeof self.printerState.printerProfile === "function"
      ) {
        profile = self.printerState.printerProfile();
      } else if (
        !profile &&
        self.printerState &&
        typeof self.printerState.currentPrinterProfileData === "function"
      ) {
        profile = self.printerState.currentPrinterProfileData();
      }

      if (!profile) {
        return true; // no profile info available, do not hide
      }

      var rawCount = profile.extruder && profile.extruder.count;
      var extruderCount = parseInt(rawCount, 10);
      if (isNaN(extruderCount) || extruderCount <= 0) {
        extruderCount = 1;
      }
      var hasBed =
        profile.heatedBed === undefined ? true : toBoolFlag(profile.heatedBed);
      var hasChamber = toBoolFlag(profile.heatedChamber);

      if (heaterName === "bed") {
        return hasBed;
      }

      if (heaterName === "chamber") {
        return hasChamber;
      }

      if (heaterName && heaterName.indexOf("tool") === 0) {
        var idx = parseInt(heaterName.replace("tool", ""), 10);
        if (isNaN(idx)) {
          return true;
        }
        return idx < extruderCount;
      }

      return true;
    };

    /**
     * Computed: CSS class for ETA display based on time
     */
    self.getETAClass = function (heater) {
      if (!heater || !heater.eta) return "hidden";

      var eta = heater.eta();
      if (!self.isETAVisible(eta)) {
        return "hidden";
      }
      if (eta < 60) {
        return "eta-warning";
      } else if (eta < 300) {
        return "eta-info";
      }
      return "eta-normal";
    };

    /**
     * Get display name for heater (friendly name)
     */
    self.getHeaterLabel = function (heaterName) {
      var labels = {
        bed: _gettext("Bed"),
        chamber: _gettext("Chamber"),
      };
      if (labels[heaterName]) {
        return labels[heaterName];
      }
      // Default for tool0, tool1, tool2, etc
      return heaterName.charAt(0).toUpperCase() + heaterName.slice(1);
    };

    self.getNotHeatingText = function () {
      return _gettext("Not heating");
    };

    /**
     * Sort heaters in logical order: tools first, then bed, then chamber
     */
    self.sortHeaters = function (heaters) {
      return heaters.slice().sort(function (a, b) {
        var nameA = a.name;
        var nameB = b.name;

        var orderA = 999;
        var orderB = 999;

        // Tools: tool0=0, tool1=1, tool2=2, etc
        if (nameA.indexOf("tool") === 0) {
          orderA = parseInt(nameA.replace("tool", ""), 10);
        } else if (nameA === "bed") {
          orderA = 1000;
        } else if (nameA === "chamber") {
          orderA = 1001;
        }

        if (nameB.indexOf("tool") === 0) {
          orderB = parseInt(nameB.replace("tool", ""), 10);
        } else if (nameB === "bed") {
          orderB = 1000;
        } else if (nameB === "chamber") {
          orderB = 1001;
        }

        return orderA - orderB;
      });
    };

    /**
     * Get icon class for heater type
     */
    self.getHeaterIcon = function (heaterName) {
      if (heaterName === "bed") {
        return "fa-bed";
      } else if (heaterName === "chamber") {
        return "fa-cube";
      } else {
        return "fa-fire"; // tools/hotends
      }
    };

    // Show only heaters with actual data from backend
    self.displayHeaters = ko.computed(function () {
      var heaters = self.heaters().filter(function (h) {
        return (
          h.actual() !== null ||
          h.target() !== null ||
          self.isETAVisible(h.eta())
        );
      });
      // Sort in logical order: tools, bed, chamber
      return self.sortHeaters(heaters);
    });

    // Visible heaters (ETA >= 1s)
    self.visibleHeaters = ko.computed(function () {
      return self.displayHeaters().filter(function (h) {
        return self.isETAVisible(h.eta());
      });
    });

    // Navbar visibility (used by template binding)
    self.showETA = ko.pureComputed(function () {
      return (
        self.isComponentEnabled("navbar") && self.visibleHeaters().length > 0
      );
    });

    self._applyComponentVisibility = function () {
      // Sidebar: hide whole box wrapper if disabled or no ETA to show.
      var showSidebar =
        self.isComponentEnabled("sidebar") && self.displayHeaters().length > 0;
      $("#sidebar_plugin_temp_eta_wrapper").toggle(!!showSidebar);

      // Tab: hide nav entry and content wrapper if disabled.
      var showTab = self.isComponentEnabled("tab");
      $("#tab_plugin_temp_eta_link").toggle(!!showTab);

      // Backwards compatible fallback (in case markup differs)
      var $tabAnchor = $("a[href='#tab_plugin_temp_eta']");
      if ($tabAnchor.length) {
        $tabAnchor.closest("li").toggle(!!showTab);
        $tabAnchor.toggle(!!showTab);
      }
    };

    self._setupVisibilitySubscriptions = function () {
      var ps = self._pluginSettings();
      if (!ps) {
        self._applyComponentVisibility();
        return;
      }

      ["enabled", "show_in_sidebar", "show_in_navbar", "show_in_tab"].forEach(
        function (key) {
          try {
            var obs = ps[key];
            if (obs && typeof obs.subscribe === "function") {
              obs.subscribe(self._applyComponentVisibility);
            }
          } catch (e) {}
        },
      );

      try {
        if (
          self.visibleHeaters &&
          typeof self.visibleHeaters.subscribe === "function"
        ) {
          self.visibleHeaters.subscribe(self._applyComponentVisibility);
        }
      } catch (e) {}

      try {
        if (
          self.displayHeaters &&
          typeof self.displayHeaters.subscribe === "function"
        ) {
          self.displayHeaters.subscribe(self._applyComponentVisibility);
        }
      } catch (e) {}

      self._applyComponentVisibility();
    };

    // Group heaters into columns of 2 (each column has max 2 rows)
    self.heaterColumns = ko.computed(function () {
      var visible = self.visibleHeaters();
      var columns = [];
      for (var i = 0; i < visible.length; i += 2) {
        columns.push(visible.slice(i, Math.min(i + 2, visible.length)));
      }
      return columns;
    });

    self.onBeforeBinding = function () {
      // Called before the view model is bound to the DOM
    };

    self.onAfterBinding = function () {
      // Called after the view model is bound to the DOM
      self._setupVisibilitySubscriptions();
      self._installSettingsDialogHooks();

      // Try binding the sidebar root even if it gets injected after startup.
      self._ensureSidebarBound();
    };

    self.onSettingsShown = function () {
      self._bindSettingsWithRetry();
    };

    self.onSettingsHidden = function () {
      self._unbindSettingsIfBound();
    };
  }

  // This is how our plugin registers itself with the application
  OCTOPRINT_VIEWMODELS.push({
    construct: TempETAViewModel,
    dependencies: [
      "settingsViewModel",
      "printerStateViewModel",
      "printerProfilesViewModel",
      "loginStateViewModel",
    ],
    elements: [
      "#tab_plugin_temp_eta",
      "#navbar_plugin_temp_eta",
      "#sidebar_plugin_temp_eta",
    ],
  });
});
