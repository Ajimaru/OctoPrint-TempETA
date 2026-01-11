/*
 * View model for OctoPrint Temperature ETA Plugin
 *
 * Implements Issue #469: Temperature countdown/ETA display
 * Author: Ajimaru
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

  function _toast(type, title, text, delayMs, extraClass) {
    if (window.PNotify) {
      var delay = typeof delayMs === "number" && isFinite(delayMs) ? delayMs : 6000;
      delay = Math.max(1000, Math.min(60000, delay));
      var extra = typeof extraClass === "string" ? extraClass : "";
      if (extra && extra.charAt(0) !== " ") {
        extra = " " + extra;
      }
      new PNotify({
        title: title,
        text: text,
        type: type,
        icon: false,
        hide: true,
        delay: delay,
        addclass: "temp-eta-toast" + extra,
        buttons: { closer: true, sticker: false },
        history: { history: false },
      });
    } else {
      _notify(type, title, text);
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

    // Extended settings: sound alerts
    self.soundBlocked = ko.observable(false);
    self._audioContext = null;
    self._soundLastPlayedByKey = {};

    self._getColorMode = function () {
      var ps = self._pluginSettings();
      if (!ps || !ps.color_mode) {
        return "bands";
      }
      try {
        var mode =
          typeof ps.color_mode === "function" ? ps.color_mode() : ps.color_mode;
        return mode === "status" ? "status" : "bands";
      } catch (e) {
        return "bands";
      }
    };

    self._readKoString = function (value, defaultValue) {
      try {
        if (typeof value === "function") {
          value = value();
        }
      } catch (e) {
        value = null;
      }
      if (typeof value === "string" && value.length) {
        return value;
      }
      return defaultValue;
    };

    self._applyStatusColorVariables = function () {
      var ps = self._pluginSettings();
      if (!ps) {
        return;
      }

      try {
        var heating = self._readKoString(ps.color_heating, "#5cb85c");
        var cooling = self._readKoString(ps.color_cooling, "#337ab7");
        var idle = self._readKoString(ps.color_idle, "#777777");
        var root = document && document.documentElement;
        if (!root || !root.style) {
          return;
        }

        root.style.setProperty("--temp-eta-color-heating", heating);
        root.style.setProperty("--temp-eta-color-cooling", cooling);
        root.style.setProperty("--temp-eta-color-idle", idle);
      } catch (e) {
        // ignore
      }
    };

    self._setupExtendedSettingsSubscriptions = function () {
      var ps = self._pluginSettings();
      if (!ps) {
        self._applyStatusColorVariables();
        return;
      }

      [
        "color_mode",
        "color_heating",
        "color_cooling",
        "color_idle",
      ].forEach(function (key) {
        try {
          var obs = ps[key];
          if (obs && typeof obs.subscribe === "function") {
            obs.subscribe(self._applyStatusColorVariables);
          }
        } catch (e) {}
      });

      self._applyStatusColorVariables();
    };

    self._i18nAttrOr = function (attrName, fallback) {
      try {
        return _attrOr($("#temp_eta_i18n"), attrName, fallback);
      } catch (e) {
        return fallback;
      }
    };

    self._isSoundEnabled = function () {
      var ps = self._pluginSettings();
      if (!ps) {
        return false;
      }
      if (!readKoBool(ps.enabled, true)) {
        return false;
      }
      return readKoBool(ps.sound_enabled, false);
    };

    self._isNotificationEnabled = function () {
      var ps = self._pluginSettings();
      if (!ps) {
        return false;
      }
      if (!readKoBool(ps.enabled, true)) {
        return false;
      }
      return readKoBool(ps.notification_enabled, false);
    };

    self._isNotificationEventEnabled = function (eventKey) {
      var ps = self._pluginSettings();
      if (!ps) {
        return false;
      }
      if (eventKey === "target_reached") {
        return readKoBool(ps.notification_target_reached, false);
      }
      if (eventKey === "cooldown_finished") {
        return readKoBool(ps.notification_cooldown_finished, false);
      }
      return false;
    };

    self._getNotificationTimeoutMs = function () {
      var ps = self._pluginSettings();
      var s = 6.0;
      if (ps) {
        s = readKoNumber(ps.notification_timeout_s, 6.0);
      }
      if (!isFinite(s) || s <= 0) {
        s = 6.0;
      }
      return Math.max(1000, Math.min(60000, s * 1000.0));
    };

    self._getNotificationMinIntervalMs = function () {
      var ps = self._pluginSettings();
      var s = 10.0;
      if (ps) {
        s = readKoNumber(ps.notification_min_interval_s, 10.0);
      }
      if (!isFinite(s) || s < 0) {
        s = 10.0;
      }
      return s * 1000.0;
    };

    self._notifyEvent = function (heaterName, eventKey, displayTargetC) {
      if (!self._isNotificationEnabled()) {
        return;
      }
      if (!self._isNotificationEventEnabled(eventKey)) {
        return;
      }

      var nowMs = Date.now();
      var k = String(heaterName) + ":" + String(eventKey);
      var last = self._notificationLastShownByKey[k] || 0;
      var minIntervalMs = self._getNotificationMinIntervalMs();
      if (nowMs - last < minIntervalMs) {
        return;
      }
      self._notificationLastShownByKey[k] = nowMs;

      var pluginTitle = self._i18nAttrOr(
        "data-notify-plugin-title",
        "Temperature ETA",
      );
      var heaterLabel = self.getHeaterLabel(heaterName);
      var targetText = self.formatTempDisplay(displayTargetC);

      var type = "info";
      var title = pluginTitle;
      var tpl = "";
      var toastClass = "temp-eta-toast-generic";

      if (eventKey === "target_reached") {
        type = "success";
        toastClass = "temp-eta-toast-target";
        title = self._i18nAttrOr(
          "data-notify-target-reached-title",
          "Target reached",
        );
        tpl = self._i18nAttrOr(
          "data-notify-target-reached-text",
          "{heater}: reached {target}",
        );
      } else if (eventKey === "cooldown_finished") {
        type = "info";
        toastClass = "temp-eta-toast-cooldown";
        title = self._i18nAttrOr(
          "data-notify-cooldown-finished-title",
          "Cooldown finished",
        );
        tpl = self._i18nAttrOr(
          "data-notify-cooldown-finished-text",
          "{heater}: cooled down to {target}",
        );
      }

      var text = String(tpl)
        .replace("{heater}", String(heaterLabel))
        .replace("{target}", String(targetText));

      _toast(type, title, text, self._getNotificationTimeoutMs(), toastClass);
    };

    self._isSoundEventEnabled = function (eventKey) {
      var ps = self._pluginSettings();
      if (!ps) {
        return false;
      }
      if (eventKey === "target_reached") {
        return readKoBool(ps.sound_target_reached, false);
      }
      if (eventKey === "cooldown_finished") {
        return readKoBool(ps.sound_cooldown_finished, false);
      }
      return false;
    };

    self._getSoundVolume = function () {
      var ps = self._pluginSettings();
      var v = 0.5;
      if (ps) {
        v = readKoNumber(ps.sound_volume, 0.5);
      }
      if (!isFinite(v)) {
        v = 0.5;
      }
      return Math.max(0, Math.min(1, v));
    };

    self._getSoundMinIntervalMs = function () {
      var ps = self._pluginSettings();
      var s = 10.0;
      if (ps) {
        s = readKoNumber(ps.sound_min_interval_s, 10.0);
      }
      if (!isFinite(s) || s < 0) {
        s = 10.0;
      }
      return s * 1000.0;
    };

    self._ensureAudioContext = function () {
      if (self._audioContext) {
        return self._audioContext;
      }
      var Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) {
        return null;
      }
      try {
        self._audioContext = new Ctx();
        return self._audioContext;
      } catch (e) {
        return null;
      }
    };

    self._getStaticSoundUrl = function (fileName) {
      // Prefer OctoPrint's helper if available; fall back to a relative URL.
      // Static files are served from /plugin/<identifier>/static/...
      try {
        if (window.OctoPrint && typeof OctoPrint.getBlueprintUrl === "function") {
          var base = OctoPrint.getBlueprintUrl("temp_eta");
          if (base && base.charAt(base.length - 1) !== "/") {
            base += "/";
          }
          return base + "static/sounds/" + encodeURIComponent(fileName);
        }
      } catch (e) {
        // ignore
      }

      return "/plugin/temp_eta/static/sounds/" + encodeURIComponent(fileName);
    };

    self._playSoundFile = function (fileName) {
      // HTMLAudio playback. This may be blocked by autoplay policies.
      try {
        var url = self._getStaticSoundUrl(fileName);
        var a = new Audio(url);
        a.volume = self._getSoundVolume();
        var p = a.play();
        if (p && typeof p.catch === "function") {
          p.catch(function () {
            self.soundBlocked(true);
            // Fallback to WebAudio beep (still may require interaction).
            self._playBeep({});
          });
        }
      } catch (e) {
        self._playBeep({});
      }
    };

    self._playBeep = function (opts) {
      var options = opts || {};
      var force = !!options.force;
      var volume =
        typeof options.volume === "number" ? options.volume : self._getSoundVolume();

      if (!force && !self._isSoundEnabled()) {
        return;
      }

      var ctx = self._ensureAudioContext();
      if (!ctx) {
        return;
      }

      var resumePromise = null;
      try {
        if (ctx.state === "suspended" && typeof ctx.resume === "function") {
          resumePromise = ctx.resume();
        }
      } catch (e) {
        resumePromise = null;
      }

      var doBeep = function () {
        try {
          if (ctx.state === "suspended") {
            self.soundBlocked(true);
            return;
          }

          self.soundBlocked(false);

          var now = ctx.currentTime;
          var osc = ctx.createOscillator();
          var gain = ctx.createGain();
          osc.type = "sine";
          osc.frequency.value = 880;

          var v = Math.max(0, Math.min(1, volume));
          gain.gain.setValueAtTime(0.0001, now);
          gain.gain.exponentialRampToValueAtTime(
            Math.max(0.0002, v),
            now + 0.02,
          );
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.14);

          osc.connect(gain);
          gain.connect(ctx.destination);

          osc.start(now);
          osc.stop(now + 0.15);
        } catch (e) {
          // ignore
        }
      };

      if (resumePromise && typeof resumePromise.then === "function") {
        resumePromise
          .then(function () {
            doBeep();
          })
          .catch(function () {
            self.soundBlocked(true);
          });
      } else {
        doBeep();
      }
    };

    self._playSoundEvent = function (heaterName, eventKey) {
      var nowMs = Date.now();
      var k = String(heaterName) + ":" + String(eventKey);
      var last = self._soundLastPlayedByKey[k] || 0;
      var minIntervalMs = self._getSoundMinIntervalMs();
      if (nowMs - last < minIntervalMs) {
        return;
      }
      self._soundLastPlayedByKey[k] = nowMs;

      if (eventKey === "target_reached") {
        self._playSoundFile("heating_done.wav");
        return;
      }
      if (eventKey === "cooldown_finished") {
        self._playSoundFile("cooling_done.wav");
        return;
      }

      self._playBeep({});
    };

    self.testSound = function () {
      // The test button should work regardless of master enable state to help
      // browsers unlock audio playback on user interaction.
      try {
        self.soundBlocked(false);
      } catch (e) {}

      // Try the file-based sound first; it will fall back to WebAudio.
      self._playSoundFile("heating_done.wav");
    };

    self._notificationLastShownByKey = {};

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

    function readKoNumber(value, defaultValue) {
      try {
        var v = value;
        if (typeof v === "function") {
          v = v();
        }
        if (v === undefined || v === null || v === "") {
          return defaultValue;
        }
        var n = parseFloat(v);
        if (!isFinite(n)) {
          return defaultValue;
        }
        return n;
      } catch (e) {}
      return defaultValue;
    }

    self._pluginSettings = function () {
      try {
        // IMPORTANT: prefer a fresh settings root (OctoPrint may replace the
        // settings object after save/reload). However, some OctoPrint setups
        // momentarily expose an empty settings structure while reloading.
        // For UI features like the historical graph, fall back to the last
        // known settings object if it still looks valid.
        var root = self._resolveSettingsRoot();
        var ps = root && root.plugins && root.plugins.temp_eta;
        var source = "fresh";

        if (
          !ps &&
          self.settings &&
          self.settings.plugins &&
          self.settings.plugins.temp_eta
        ) {
          ps = self.settings.plugins.temp_eta;
          source = "fallback";
        }

        if (ps && root && root.plugins) {
          self.settings = root;
        }

        // Debug once in a while to diagnose cases where the settings root is
        // temporarily missing and would disable features like the historical graph.
        // This logs to the browser console only (controlled by debug_logging).
        try {
          var dbg = {
            source: source,
            hasFreshPlugins: !!(root && root.plugins),
            hasFallbackPlugins: !!(self.settings && self.settings.plugins),
            show_historical_graph: ps
              ? readKoBool(ps.show_historical_graph, null)
              : null,
          };
          self._debugLog(
            "settings_graph",
            "[TempETA] Settings snapshot",
            dbg,
            60000,
          );
        } catch (e) {}

        return ps;
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

    self.isProgressBarsEnabled = function () {
      var ps = self._pluginSettings();
      if (!ps) {
        return true;
      }

      var pluginEnabled = readKoBool(ps.enabled, true);
      if (!pluginEnabled) {
        return false;
      }

      return readKoBool(ps.show_progress_bars, true);
    };

    self.isHistoricalGraphEnabled = function () {
      var ps = self._pluginSettings();
      if (!ps) {
        return false;
      }

      var pluginEnabled = readKoBool(ps.enabled, true);
      if (!pluginEnabled) {
        return false;
      }

      return readKoBool(ps.show_historical_graph, false);
    };

    self.getHistoricalGraphWindowSeconds = function () {
      var ps = self._pluginSettings();
      var seconds = 180;
      if (ps) {
        seconds = readKoNumber(ps.historical_graph_window_seconds, 180);
      }

      // Clamp to a reasonable range to prevent runaway memory usage.
      if (!isFinite(seconds)) {
        seconds = 180;
      }
      seconds = Math.max(30, Math.min(1800, seconds));
      return seconds;
    };

    self.isHistoricalGraphVisible = function (heater) {
      if (!self.isHistoricalGraphEnabled()) {
        return false;
      }

      if (!heater || !heater.actual || !heater.target) {
        return false;
      }

      var actual = parseFloat(heater.actual());
      var target = parseFloat(heater.target());
      if (!isFinite(actual) || !isFinite(target)) {
        return false;
      }

      // Only show if we have at least a couple of points recorded.
      if (!heater._history || heater._history.length < 2) {
        return false;
      }

      return true;
    };

    self._recordHeaterHistory = function (heaterObj, tsSec, actualC, targetC) {
      if (!heaterObj) {
        return;
      }

      if (!heaterObj._history) {
        heaterObj._history = [];
      }

      // Only record when the feature is enabled.
      if (!self.isHistoricalGraphEnabled()) {
        heaterObj._history = [];
        return;
      }

      if (!isFinite(tsSec) || !isFinite(actualC) || !isFinite(targetC)) {
        return;
      }

      heaterObj._history.push({ t: tsSec, a: actualC, tg: targetC });

      // Prune to configured window (keep a small margin).
      var windowSec = self.getHistoricalGraphWindowSeconds();
      var cutoff = tsSec - windowSec - 5;
      while (heaterObj._history.length && heaterObj._history[0].t < cutoff) {
        heaterObj._history.shift();
      }

      // Hard cap as a safety net (shouldn't be hit in normal operation).
      if (heaterObj._history.length > 5000) {
        heaterObj._history = heaterObj._history.slice(-5000);
      }
    };

    self._formatAxisTime = function (seconds) {
      // Format seconds as M:SS (no i18n needed for numeric axis labels).
      if (!isFinite(seconds) || seconds < 0) {
        seconds = 0;
      }
      var s = Math.round(seconds);
      var m = Math.floor(s / 60);
      var r = s % 60;
      return m + ":" + (r < 10 ? "0" : "") + r;
    };

    self._formatAxisTemp = function (tempC) {
      // Keep labels compact; whole degrees read better at small font sizes.
      if (!isFinite(tempC)) {
        return "";
      }

      var unit = self._effectiveThresholdUnit() === "f" ? "°F" : "°C";
      var value = tempC;
      if (unit === "°F") {
        value = self._cToF(tempC);
      }

      return String(Math.round(value)) + unit;
    };

    self._isHeaterHeatingNow = function (etaValue, actualC, targetC) {
      // "Idle" in the UI should cover: no active target or already at/above target.
      // Use a small epsilon to avoid flicker around the target.
      var eps = 0.3;
      if (!isFinite(actualC) || !isFinite(targetC) || targetC <= 0) {
        return false;
      }
      if (self.isETAVisible(etaValue)) {
        return true;
      }
      return targetC - actualC > eps;
    };

    self._renderHistoricalGraph = function (heaterObj) {
      if (!heaterObj) {
        return;
      }

      // Throttle per heater to ~1Hz.
      var nowMs = Date.now();
      if (
        heaterObj._lastGraphRenderMs &&
        nowMs - heaterObj._lastGraphRenderMs < 900
      ) {
        return;
      }
      heaterObj._lastGraphRenderMs = nowMs;

      if (!self.isHistoricalGraphVisible(heaterObj)) {
        return;
      }

      var poly = document.getElementById(
        "temp_eta_graph_actual_" + heaterObj.name,
      );
      var targetLine = document.getElementById(
        "temp_eta_graph_target_" + heaterObj.name,
      );
      if (!poly || !targetLine) {
        return;
      }

      var hist = heaterObj._history || [];
      if (hist.length < 2) {
        poly.setAttribute("points", "");
        return;
      }

      // ViewBox: 0..100 (x), 0..40 (y)
      var vbW = 100;
      var vbH = 40;
      var plotLeft = 12;
      var plotRight = 99;
      var plotTop = 2;
      var plotBottom = 30;
      var plotW = plotRight - plotLeft;
      var plotH = plotBottom - plotTop;

      var windowSec = self.getHistoricalGraphWindowSeconds();
      var nowSec = hist[hist.length - 1].t;
      var minT = nowSec - windowSec;

      // Determine min/max for scaling.
      var minTemp = Infinity;
      var maxTemp = -Infinity;
      for (var i = 0; i < hist.length; i++) {
        var p = hist[i];
        if (p.t < minT) continue;
        if (p.a < minTemp) minTemp = p.a;
        if (p.a > maxTemp) maxTemp = p.a;
        if (isFinite(p.tg) && p.tg > 0) {
          if (p.tg < minTemp) minTemp = p.tg;
          if (p.tg > maxTemp) maxTemp = p.tg;
        }
      }

      if (!isFinite(minTemp) || !isFinite(maxTemp)) {
        poly.setAttribute("points", "");
        return;
      }

      if (Math.abs(maxTemp - minTemp) < 0.5) {
        maxTemp = minTemp + 0.5;
      }

      // Add small padding.
      var pad = Math.max(1.0, (maxTemp - minTemp) * 0.05);
      minTemp -= pad;
      maxTemp += pad;

      function yForTemp(tempC) {
        var yNorm = (tempC - minTemp) / (maxTemp - minTemp);
        var y = plotBottom - yNorm * plotH;
        if (!isFinite(y)) {
          return plotBottom;
        }
        return Math.max(plotTop, Math.min(plotBottom, y));
      }

      function xForTime(ts) {
        var x = plotLeft + ((ts - minT) / windowSec) * plotW;
        if (!isFinite(x)) {
          return plotLeft;
        }
        return Math.max(plotLeft, Math.min(plotRight, x));
      }

      var points = [];
      for (var j = 0; j < hist.length; j++) {
        var h = hist[j];
        if (h.t < minT) continue;

        var x = xForTime(h.t);
        var y = yForTemp(h.a);
        points.push(x.toFixed(2) + "," + y.toFixed(2));
      }

      poly.setAttribute("points", points.join(" "));

      // Target line uses current target.
      var currentTarget = parseFloat(heaterObj.target());
      if (isFinite(currentTarget) && currentTarget > 0) {
        var yT = yForTemp(currentTarget);
        targetLine.setAttribute("x1", plotLeft);
        targetLine.setAttribute("x2", plotRight);
        targetLine.setAttribute("y1", yT.toFixed(2));
        targetLine.setAttribute("y2", yT.toFixed(2));
        targetLine.style.display = "";
      } else {
        targetLine.style.display = "none";
      }

      // Axes labels + Y ticks.
      var yMin = minTemp;
      var yMax = maxTemp;
      var yMid = (yMin + yMax) / 2.0;

      var unitX = document.getElementById(
        "temp_eta_graph_unit_x_" + heaterObj.name,
      );
      if (unitX) {
        unitX.textContent = "mm:ss";
      }

      var tickYMax = document.getElementById(
        "temp_eta_graph_tick_ymax_" + heaterObj.name,
      );
      var tickYMid = document.getElementById(
        "temp_eta_graph_tick_ymid_" + heaterObj.name,
      );
      var tickYMin = document.getElementById(
        "temp_eta_graph_tick_ymin_" + heaterObj.name,
      );

      var labelYMax = document.getElementById(
        "temp_eta_graph_label_ymax_" + heaterObj.name,
      );
      var labelYMid = document.getElementById(
        "temp_eta_graph_label_ymid_" + heaterObj.name,
      );
      var labelYMin = document.getElementById(
        "temp_eta_graph_label_ymin_" + heaterObj.name,
      );

      if (
        tickYMax &&
        tickYMid &&
        tickYMin &&
        labelYMax &&
        labelYMid &&
        labelYMin
      ) {
        var yTickMaxPos = yForTemp(yMax);
        var yTickMidPos = yForTemp(yMid);
        var yTickMinPos = yForTemp(yMin);

        tickYMax.setAttribute("y1", yTickMaxPos.toFixed(2));
        tickYMax.setAttribute("y2", yTickMaxPos.toFixed(2));
        tickYMid.setAttribute("y1", yTickMidPos.toFixed(2));
        tickYMid.setAttribute("y2", yTickMidPos.toFixed(2));
        tickYMin.setAttribute("y1", yTickMinPos.toFixed(2));
        tickYMin.setAttribute("y2", yTickMinPos.toFixed(2));

        labelYMax.textContent = self._formatAxisTemp(yMax);
        labelYMid.textContent = self._formatAxisTemp(yMid);
        labelYMin.textContent = self._formatAxisTemp(yMin);

        labelYMax.setAttribute("y", yTickMaxPos.toFixed(2));
        labelYMid.setAttribute("y", yTickMidPos.toFixed(2));
        labelYMin.setAttribute("y", yTickMinPos.toFixed(2));
      }

      // X labels are relative time within the window.
      var labelXLeft = document.getElementById(
        "temp_eta_graph_label_xleft_" + heaterObj.name,
      );
      var labelXMid = document.getElementById(
        "temp_eta_graph_label_xmid_" + heaterObj.name,
      );
      var labelXRight = document.getElementById(
        "temp_eta_graph_label_xright_" + heaterObj.name,
      );
      if (labelXLeft && labelXMid && labelXRight) {
        labelXLeft.textContent = "-" + self._formatAxisTime(windowSec);
        labelXMid.textContent = "-" + self._formatAxisTime(windowSec / 2.0);
        labelXRight.textContent = "0:00";
      }
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
        var etaKind = data.eta_kind || null;
        var cooldownTarget =
          data.cooldown_target !== undefined && data.cooldown_target !== null
            ? parseFloat(data.cooldown_target)
            : null;

        // Dynamically register heaters as they appear
        if (!self.heaterData[heater]) {
          self.heaterData[heater] = {
            name: heater,
            eta: ko.observable(null),
            etaKind: ko.observable(null),
            actual: ko.observable(null),
            target: ko.observable(null),
            cooldownTarget: ko.observable(null),
            startTemp: ko.observable(null),
            startTarget: ko.observable(null),
            _history: [],
            _lastGraphRenderMs: 0,
            _targetReachedNotifiedFor: null,
            _targetReachedNotifiedForNotification: null,
          };
          self.heaters.push(self.heaterData[heater]);
          self._debugLog(
            "register_" + heater,
            "[TempETA] Registered new heater",
            heater,
            60000,
          );
        }

        // Capture previous state for sound/event transitions.
        var heaterObj = self.heaterData[heater];
        var prevEta = heaterObj.eta();
        var prevEtaKind = heaterObj.etaKind();
        var prevActual = heaterObj.actual ? parseFloat(heaterObj.actual()) : NaN;
        var prevTarget = heaterObj.target ? parseFloat(heaterObj.target()) : NaN;

        // Update heater data
        heaterObj.eta(eta);
        heaterObj.etaKind(etaKind);
        heaterObj.actual(data.actual);
        heaterObj.target(data.target);
        heaterObj.cooldownTarget(
          cooldownTarget !== null && isFinite(cooldownTarget)
            ? cooldownTarget
            : null,
        );

        // Track start temperature for progress bars.
        // We reset this when a new target is set (or the target changes), so
        // progress represents the fraction from startTemp -> target.
        var actualNow = parseFloat(data.actual);
        var targetNow = parseFloat(data.target);
        var prevStartTarget = parseFloat(heaterObj.startTarget());

        var heatingNow = self._isHeaterHeatingNow(eta, actualNow, targetNow);
        if (!heatingNow) {
          // Reset when the heater returns to "Idle" (e.g. reached target).
          heaterObj.startTemp(null);
          heaterObj.startTarget(null);
        } else {
          var needsReset =
            !isFinite(prevStartTarget) ||
            Math.abs(prevStartTarget - targetNow) > 1e-6 ||
            heaterObj.startTemp() === null ||
            heaterObj.startTemp() === undefined;

          if (needsReset) {
            heaterObj.startTemp(actualNow);
            heaterObj.startTarget(targetNow);
          }
        }

        // Sound alert transitions.
        try {
          var prevHeating = self._isHeaterHeatingNow(
            prevEta,
            prevActual,
            prevTarget,
          );

          // Reset target-reached marker if the target changes significantly.
          if (
            isFinite(prevTarget) &&
            isFinite(targetNow) &&
            Math.abs(prevTarget - targetNow) > 0.2
          ) {
            heaterObj._targetReachedNotifiedFor = null;
            heaterObj._targetReachedNotifiedForNotification = null;
          }

          if (
            self._isSoundEnabled() &&
            self._isSoundEventEnabled("target_reached") &&
            prevHeating &&
            !heatingNow &&
            isFinite(targetNow) &&
            targetNow > 0
          ) {
            var notifiedFor = heaterObj._targetReachedNotifiedFor;
            if (
              !isFinite(notifiedFor) ||
              notifiedFor === null ||
              Math.abs(notifiedFor - targetNow) > 0.1
            ) {
              heaterObj._targetReachedNotifiedFor = targetNow;
              self._playSoundEvent(heater, "target_reached");
            }
          }

          if (
            self._isNotificationEnabled() &&
            self._isNotificationEventEnabled("target_reached") &&
            prevHeating &&
            !heatingNow &&
            isFinite(targetNow) &&
            targetNow > 0
          ) {
            var notifiedForN = heaterObj._targetReachedNotifiedForNotification;
            if (
              !isFinite(notifiedForN) ||
              notifiedForN === null ||
              Math.abs(notifiedForN - targetNow) > 0.1
            ) {
              heaterObj._targetReachedNotifiedForNotification = targetNow;
              self._notifyEvent(heater, "target_reached", targetNow);
            }
          }

          var prevCooling = prevEtaKind === "cooling";
          var nowCooling = etaKind === "cooling";
          if (
            self._isSoundEnabled() &&
            self._isSoundEventEnabled("cooldown_finished") &&
            prevCooling &&
            !nowCooling
          ) {
            self._playSoundEvent(heater, "cooldown_finished");
          }

          if (
            self._isNotificationEnabled() &&
            self._isNotificationEventEnabled("cooldown_finished") &&
            prevCooling &&
            !nowCooling
          ) {
            // Prefer the explicit cooldown target if provided, otherwise fall back
            // to the current "effective" target.
            var t = cooldownTarget;
            if (!isFinite(t) || t === null) {
              t = targetNow;
            }
            self._notifyEvent(heater, "cooldown_finished", t);
          }
        } catch (e) {
          // ignore
        }

        // Record and render history graph (tab view).
        self._recordHeaterHistory(
          heaterObj,
          Date.now() / 1000.0,
          actualNow,
          targetNow,
        );
        self._renderHistoricalGraph(heaterObj);

        // Ensure sidebar becomes visible even if it was injected late.
        self._throttledEnsureSidebarBound();
      }
    };

    self._effectiveDisplayTargetC = function (heater) {
      if (!heater) {
        return NaN;
      }

      try {
        var kind = heater.etaKind ? heater.etaKind() : null;
        if (kind === "cooling") {
          var ct = heater.cooldownTarget
            ? parseFloat(heater.cooldownTarget())
            : NaN;
          if (isFinite(ct) && ct > -100) {
            return ct;
          }
        }
      } catch (e) {
        // ignore
      }

      return heater.target ? parseFloat(heater.target()) : NaN;
    };

    self.formatTempPair = function (heater) {
      if (!heater) {
        return "";
      }
      var actual = heater.actual ? parseFloat(heater.actual()) : NaN;
      var effTarget = self._effectiveDisplayTargetC(heater);

      if (!isFinite(actual)) {
        return "";
      }

      if (!isFinite(effTarget) || effTarget <= 0) {
        // When no target is set and we don't have a cooldown target, show only the actual.
        return self.formatTempDisplay(actual);
      }

      return (
        self.formatTempDisplay(actual) + "/" + self.formatTempDisplay(effTarget)
      );
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

      if (heater.etaKind && heater.etaKind() === "cooling") {
        return "eta-cooling";
      }

      if (self._getColorMode() === "status") {
        return "eta-heating";
      }
      if (eta < 60) {
        return "eta-warning";
      } else if (eta < 300) {
        return "eta-info";
      }
      return "eta-normal";
    };

    /**
     * Progress helpers (percent to target).
     *
     * We intentionally compute this client-side from actual/target to keep the
     * backend payload small and robust across profiles/heaters.
     */
    self.isProgressVisible = function (heater) {
      if (!self.isProgressBarsEnabled()) {
        return false;
      }

      if (!heater || !heater.actual || !heater.target) {
        return false;
      }

      var actual = parseFloat(heater.actual());
      var target = parseFloat(heater.target());

      if (!isFinite(actual) || !isFinite(target) || target <= 0) {
        return false;
      }

      return true;
    };

    self.isTabProgressVisible = function (heater) {
      if (!self.isProgressVisible(heater)) {
        return false;
      }

      // Tab view should reset/hide progress when the heater is back to "Idle".
      var eta = heater && heater.eta ? heater.eta() : null;
      var actual = heater && heater.actual ? parseFloat(heater.actual()) : NaN;
      var target = heater && heater.target ? parseFloat(heater.target()) : NaN;
      return self._isHeaterHeatingNow(eta, actual, target);
    };

    self.getProgressPercent = function (heater) {
      if (!self.isProgressVisible(heater)) {
        return 0;
      }

      var actual = parseFloat(heater.actual());
      var target = parseFloat(heater.target());

      // Preferred: progress from startTemp -> target.
      var start = null;
      if (heater.startTemp && heater.startTarget) {
        var st = parseFloat(heater.startTemp());
        var tt = parseFloat(heater.startTarget());
        if (isFinite(st) && isFinite(tt) && tt > 0) {
          start = st;
          target = tt;
        }
      }

      if (!isFinite(actual) || !isFinite(target) || target <= 0) {
        return 0;
      }

      // If start is unknown, fall back to actual/target.
      var pct = 0;
      if (start === null || start === undefined || !isFinite(start)) {
        pct = (actual / target) * 100.0;
      } else {
        var denom = target - start;
        if (!isFinite(denom) || denom <= 0.001) {
          pct = (actual / target) * 100.0;
        } else {
          pct = ((actual - start) / denom) * 100.0;
        }
      }

      if (!isFinite(pct)) {
        pct = 0;
      }
      pct = Math.max(0, Math.min(100, pct));
      return pct;
    };

    self.getProgressBarClass = function (heater) {
      if (self._getColorMode() === "status") {
        if (heater && heater.etaKind && heater.etaKind() === "cooling") {
          return "eta-cooling";
        }
        var eta = heater && heater.eta ? heater.eta() : null;
        var actual = heater && heater.actual ? parseFloat(heater.actual()) : NaN;
        var target = heater && heater.target ? parseFloat(heater.target()) : NaN;
        return self._isHeaterHeatingNow(eta, actual, target)
          ? "eta-heating"
          : "eta-idle";
      }

      // Reuse the ETA coloring bands. When ETA is hidden, use a neutral style.
      var c = self.getETAClass(heater);
      if (!c || c === "hidden") {
        return "eta-normal";
      }
      return c;
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
      return _gettext("Idle");
    };

    self.getHeaterIdleText = function (heater) {
      if (heater && heater.etaKind && heater.etaKind() === "cooling") {
        return _gettext("Cooling");
      }
      return _gettext("Idle");
    };

    self.getHeaterIdleClass = function (heater) {
      if (heater && heater.etaKind && heater.etaKind() === "cooling") {
        return "eta-cooling";
      }
      return "eta-idle";
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

      // Extended settings (colors + sound)
      self._setupExtendedSettingsSubscriptions();

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
