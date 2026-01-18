## Classes

<dl>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd></dd>
<dt><a href="#PluginMessage">PluginMessage</a> : <code>Object</code></dt>
<dd><p>TempETAViewModel</p></dd>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd></dd>
<dt><a href="#PluginMessage">PluginMessage</a> : <code>Object</code></dt>
<dd><p>TempETAViewModel</p></dd>
</dl>

## Functions

<dl>
<dt><a href="#resetProfileHistoryHandler">resetProfileHistoryHandler(e)</a></dt>
<dd><p>Handler for the &quot;Reset Profile History&quot; settings button.
Delegated click handler so it works regardless of template binding timing.</p></dd>
<dt><a href="#restoreDefaultsHandler">restoreDefaultsHandler(e)</a></dt>
<dd><p>Handler for the &quot;Restore Defaults&quot; settings button.
Invokes OctoPrint's <code>simpleApiCommand</code> to instruct the plugin to reset
settings to their defaults.</p></dd>
<dt><a href="#calculateETA">calculateETA(history, target)</a> ⇒ <code>number</code></dt>
<dd><p>calculateETA (placeholder documentation)</p>
<p>ETA calculation is primarily performed on the backend for accuracy and
consistency. If a client-side implementation exists in the future, it
should accept a <code>history</code> array of [HeaterHistoryEntry](#HeaterHistoryEntry) and a numeric <code>target</code>.</p></dd>
<dt><a href="#resetProfileHistoryHandler">resetProfileHistoryHandler(e)</a></dt>
<dd><p>Handler for the &quot;Reset Profile History&quot; settings button.
Delegated click handler so it works regardless of template binding timing.</p></dd>
<dt><a href="#restoreDefaultsHandler">restoreDefaultsHandler(e)</a></dt>
<dd><p>Handler for the &quot;Restore Defaults&quot; settings button.
Invokes OctoPrint's <code>simpleApiCommand</code> to instruct the plugin to reset
settings to their defaults.</p></dd>
<dt><a href="#calculateETA">calculateETA(history, target)</a> ⇒ <code>number</code></dt>
<dd><p>calculateETA (placeholder documentation)</p>
<p>ETA calculation is primarily performed on the backend for accuracy and
consistency. If a client-side implementation exists in the future, it
should accept a <code>history</code> array of [HeaterHistoryEntry](#HeaterHistoryEntry) and a numeric <code>target</code>.</p></dd>
</dl>

## Typedefs

<dl>
<dt><a href="#Heater">Heater</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#HeaterHistoryEntry">HeaterHistoryEntry</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#PluginSettings">PluginSettings</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#SoundConfig">SoundConfig</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#PluginMessage">PluginMessage</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#Heater">Heater</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#HeaterHistoryEntry">HeaterHistoryEntry</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#PluginSettings">PluginSettings</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#SoundConfig">SoundConfig</a> : <code>Object</code></dt>
<dd></dd>
<dt><a href="#PluginMessage">PluginMessage</a> : <code>Object</code></dt>
<dd></dd>
</dl>

<a name="TempETAViewModel"></a>

## TempETAViewModel
**Kind**: global class

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [._resolveSettingsRoot()](#TempETAViewModel+_resolveSettingsRoot) ⇒ <code>Object</code>
    * [._getSettingsDialogRoot()](#TempETAViewModel+_getSettingsDialogRoot) ⇒ <code>jQuery</code> \| <code>null</code>
    * [._bindSettingsIfNeeded()](#TempETAViewModel+_bindSettingsIfNeeded) ⇒ <code>void</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._formatValidationMessage(template, [params])](#TempETAViewModel+_formatValidationMessage) ⇒ <code>string</code>
    * [._clearValidationForInput(inputEl)](#TempETAViewModel+_clearValidationForInput) ⇒ <code>void</code>
    * [._setValidationForInput(inputEl, message)](#TempETAViewModel+_setValidationForInput) ⇒ <code>void</code>
    * [._isEmptyValue(v)](#TempETAViewModel+_isEmptyValue) ⇒ <code>boolean</code>
    * [._parseFiniteNumber(v)](#TempETAViewModel+_parseFiniteNumber) ⇒ <code>number</code> \| <code>null</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._installSettingsValidationHandlers(rootEl)](#TempETAViewModel+_installSettingsValidationHandlers) ⇒ <code>void</code>
    * [._validateAllSettingsNumbers()](#TempETAViewModel+_validateAllSettingsNumbers) ⇒ <code>boolean</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._unbindSettingsIfBound()](#TempETAViewModel+_unbindSettingsIfBound) ⇒ <code>void</code>
    * [._bindSettingsWithRetry()](#TempETAViewModel+_bindSettingsWithRetry) ⇒ <code>void</code>
    * [._bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs])](#TempETAViewModel+_bindElementOnce) ⇒ <code>void</code>
    * [._installSettingsDialogHooks()](#TempETAViewModel+_installSettingsDialogHooks) ⇒ <code>void</code>
    * [._ensureSidebarBound()](#TempETAViewModel+_ensureSidebarBound) ⇒ <code>void</code>
    * [._throttledEnsureSidebarBound()](#TempETAViewModel+_throttledEnsureSidebarBound) ⇒ <code>void</code>
    * [._isFrontendDebugEnabled()](#TempETAViewModel+_isFrontendDebugEnabled) ⇒ <code>boolean</code>
    * [._debugLog(key, message, [payload], [minIntervalMs])](#TempETAViewModel+_debugLog) ⇒ <code>void</code>
    * [._getColorMode()](#TempETAViewModel+_getColorMode) ⇒ <code>string</code>
    * [._readKoString(value, defaultValue)](#TempETAViewModel+_readKoString) ⇒ <code>string</code>
    * [._applyStatusColorVariables()](#TempETAViewModel+_applyStatusColorVariables) ⇒ <code>void</code>
    * [._setupExtendedSettingsSubscriptions()](#TempETAViewModel+_setupExtendedSettingsSubscriptions) ⇒ <code>void</code>
    * [._i18nAttrOr(attrName, fallback)](#TempETAViewModel+_i18nAttrOr) ⇒ <code>string</code>
    * [._isSoundEnabled()](#TempETAViewModel+_isSoundEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEnabled()](#TempETAViewModel+_isNotificationEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEventEnabled(eventKey)](#TempETAViewModel+_isNotificationEventEnabled) ⇒ <code>boolean</code>
    * [._getNotificationTimeoutMs()](#TempETAViewModel+_getNotificationTimeoutMs) ⇒ <code>number</code>
    * [._getNotificationMinIntervalMs()](#TempETAViewModel+_getNotificationMinIntervalMs) ⇒ <code>number</code>
    * [._notifyEvent(heaterName, eventKey, displayTargetC)](#TempETAViewModel+_notifyEvent) ⇒ <code>void</code>
    * [._isSoundEventEnabled(eventKey)](#TempETAViewModel+_isSoundEventEnabled) ⇒ <code>boolean</code>
    * [._getSoundVolume()](#TempETAViewModel+_getSoundVolume) ⇒ <code>number</code>
    * [._getSoundMinIntervalMs()](#TempETAViewModel+_getSoundMinIntervalMs) ⇒ <code>number</code>
    * [._ensureAudioContext()](#TempETAViewModel+_ensureAudioContext) ⇒ <code>AudioContext</code> \| <code>null</code>
    * [._getStaticSoundUrl(fileName)](#TempETAViewModel+_getStaticSoundUrl) ⇒ <code>string</code>
    * [._playSoundFile(fileName)](#TempETAViewModel+_playSoundFile) ⇒ <code>void</code>
    * [._playBeep([opts])](#TempETAViewModel+_playBeep) ⇒ <code>void</code>
    * [._playSoundEvent(heaterName, eventKey)](#TempETAViewModel+_playSoundEvent) ⇒ <code>void</code>
    * [.testSound()](#TempETAViewModel+testSound) ⇒ <code>void</code>
    * [._pluginSettings()](#TempETAViewModel+_pluginSettings) ⇒ <code>Object</code> \| <code>null</code>
    * [.isComponentEnabled(component)](#TempETAViewModel+isComponentEnabled) ⇒ <code>boolean</code>
    * [.isProgressBarsEnabled()](#TempETAViewModel+isProgressBarsEnabled) ⇒ <code>boolean</code>
    * [.isHistoricalGraphEnabled()](#TempETAViewModel+isHistoricalGraphEnabled) ⇒ <code>boolean</code>
    * [.getHistoricalGraphWindowSeconds()](#TempETAViewModel+getHistoricalGraphWindowSeconds) ⇒ <code>number</code>
    * [.isHistoricalGraphVisible(heater)](#TempETAViewModel+isHistoricalGraphVisible) ⇒ <code>boolean</code>
    * [._recordHeaterHistory(heaterObj, tsSec, actualC, targetC)](#TempETAViewModel+_recordHeaterHistory) ⇒ <code>void</code>
    * [._resetHistoricalGraphState([info])](#TempETAViewModel+_resetHistoricalGraphState) ⇒ <code>void</code>
    * [._getGraphElements(heaterName)](#TempETAViewModel+_getGraphElements) ⇒ <code>Object</code> \| <code>null</code>
    * [._formatAxisTime(seconds)](#TempETAViewModel+_formatAxisTime) ⇒ <code>string</code>
    * [._formatAxisTemp(tempC)](#TempETAViewModel+_formatAxisTemp) ⇒ <code>string</code>
    * [._isHeaterHeatingNow(etaValue, actualC, targetC)](#TempETAViewModel+_isHeaterHeatingNow) ⇒ <code>boolean</code>
    * [._renderHistoricalGraph(heaterObj)](#TempETAViewModel+_renderHistoricalGraph) ⇒ <code>void</code>
    * [.formatTempDisplay(temp)](#TempETAViewModel+formatTempDisplay) ⇒ <code>string</code>
    * [._cToF(celsius)](#TempETAViewModel+_cToF) ⇒ <code>number</code>
    * [._fToC(fahrenheit)](#TempETAViewModel+_fToC) ⇒ <code>number</code>
    * [._cDeltaToF(deltaC)](#TempETAViewModel+_cDeltaToF) ⇒ <code>number</code>
    * [._fDeltaToC(deltaF)](#TempETAViewModel+_fDeltaToC) ⇒ <code>number</code>
    * [._effectiveThresholdUnit()](#TempETAViewModel+_effectiveThresholdUnit) ⇒ <code>string</code>
    * [.onSettingsBeforeSave()](#TempETAViewModel+onSettingsBeforeSave) ⇒ <code>boolean</code>
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [._effectiveDisplayTargetC(heater)](#TempETAViewModel+_effectiveDisplayTargetC) ⇒ <code>number</code>
    * [.formatTempPair(heater)](#TempETAViewModel+formatTempPair) ⇒ <code>string</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getETAClass(heater)](#TempETAViewModel+getETAClass) ⇒ <code>string</code>
    * [.isProgressVisible(heater)](#TempETAViewModel+isProgressVisible) ⇒ <code>boolean</code>
    * [.isTabProgressVisible(heater)](#TempETAViewModel+isTabProgressVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel+getProgressPercent) ⇒ <code>number</code>
    * [.getProgressBarClass(heater)](#TempETAViewModel+getProgressBarClass) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterIdleClass(heater)](#TempETAViewModel+getHeaterIdleClass) ⇒ <code>string</code>
    * [.sortHeaters(heaters)](#TempETAViewModel+sortHeaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
    * [.getHeaterIcon(heaterName)](#TempETAViewModel+getHeaterIcon) ⇒ <code>string</code>
    * [._resolveSettingsRoot()](#TempETAViewModel+_resolveSettingsRoot) ⇒ <code>Object</code>
    * [._getSettingsDialogRoot()](#TempETAViewModel+_getSettingsDialogRoot) ⇒ <code>jQuery</code> \| <code>null</code>
    * [._bindSettingsIfNeeded()](#TempETAViewModel+_bindSettingsIfNeeded) ⇒ <code>void</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._formatValidationMessage(template, [params])](#TempETAViewModel+_formatValidationMessage) ⇒ <code>string</code>
    * [._clearValidationForInput(inputEl)](#TempETAViewModel+_clearValidationForInput) ⇒ <code>void</code>
    * [._setValidationForInput(inputEl, message)](#TempETAViewModel+_setValidationForInput) ⇒ <code>void</code>
    * [._isEmptyValue(v)](#TempETAViewModel+_isEmptyValue) ⇒ <code>boolean</code>
    * [._parseFiniteNumber(v)](#TempETAViewModel+_parseFiniteNumber) ⇒ <code>number</code> \| <code>null</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._installSettingsValidationHandlers(rootEl)](#TempETAViewModel+_installSettingsValidationHandlers) ⇒ <code>void</code>
    * [._validateAllSettingsNumbers()](#TempETAViewModel+_validateAllSettingsNumbers) ⇒ <code>boolean</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._unbindSettingsIfBound()](#TempETAViewModel+_unbindSettingsIfBound) ⇒ <code>void</code>
    * [._bindSettingsWithRetry()](#TempETAViewModel+_bindSettingsWithRetry) ⇒ <code>void</code>
    * [._bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs])](#TempETAViewModel+_bindElementOnce) ⇒ <code>void</code>
    * [._installSettingsDialogHooks()](#TempETAViewModel+_installSettingsDialogHooks) ⇒ <code>void</code>
    * [._ensureSidebarBound()](#TempETAViewModel+_ensureSidebarBound) ⇒ <code>void</code>
    * [._throttledEnsureSidebarBound()](#TempETAViewModel+_throttledEnsureSidebarBound) ⇒ <code>void</code>
    * [._isFrontendDebugEnabled()](#TempETAViewModel+_isFrontendDebugEnabled) ⇒ <code>boolean</code>
    * [._debugLog(key, message, [payload], [minIntervalMs])](#TempETAViewModel+_debugLog) ⇒ <code>void</code>
    * [._getColorMode()](#TempETAViewModel+_getColorMode) ⇒ <code>string</code>
    * [._readKoString(value, defaultValue)](#TempETAViewModel+_readKoString) ⇒ <code>string</code>
    * [._applyStatusColorVariables()](#TempETAViewModel+_applyStatusColorVariables) ⇒ <code>void</code>
    * [._setupExtendedSettingsSubscriptions()](#TempETAViewModel+_setupExtendedSettingsSubscriptions) ⇒ <code>void</code>
    * [._i18nAttrOr(attrName, fallback)](#TempETAViewModel+_i18nAttrOr) ⇒ <code>string</code>
    * [._isSoundEnabled()](#TempETAViewModel+_isSoundEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEnabled()](#TempETAViewModel+_isNotificationEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEventEnabled(eventKey)](#TempETAViewModel+_isNotificationEventEnabled) ⇒ <code>boolean</code>
    * [._getNotificationTimeoutMs()](#TempETAViewModel+_getNotificationTimeoutMs) ⇒ <code>number</code>
    * [._getNotificationMinIntervalMs()](#TempETAViewModel+_getNotificationMinIntervalMs) ⇒ <code>number</code>
    * [._notifyEvent(heaterName, eventKey, displayTargetC)](#TempETAViewModel+_notifyEvent) ⇒ <code>void</code>
    * [._isSoundEventEnabled(eventKey)](#TempETAViewModel+_isSoundEventEnabled) ⇒ <code>boolean</code>
    * [._getSoundVolume()](#TempETAViewModel+_getSoundVolume) ⇒ <code>number</code>
    * [._getSoundMinIntervalMs()](#TempETAViewModel+_getSoundMinIntervalMs) ⇒ <code>number</code>
    * [._ensureAudioContext()](#TempETAViewModel+_ensureAudioContext) ⇒ <code>AudioContext</code> \| <code>null</code>
    * [._getStaticSoundUrl(fileName)](#TempETAViewModel+_getStaticSoundUrl) ⇒ <code>string</code>
    * [._playSoundFile(fileName)](#TempETAViewModel+_playSoundFile) ⇒ <code>void</code>
    * [._playBeep([opts])](#TempETAViewModel+_playBeep) ⇒ <code>void</code>
    * [._playSoundEvent(heaterName, eventKey)](#TempETAViewModel+_playSoundEvent) ⇒ <code>void</code>
    * [.testSound()](#TempETAViewModel+testSound) ⇒ <code>void</code>
    * [._pluginSettings()](#TempETAViewModel+_pluginSettings) ⇒ <code>Object</code> \| <code>null</code>
    * [.isComponentEnabled(component)](#TempETAViewModel+isComponentEnabled) ⇒ <code>boolean</code>
    * [.isProgressBarsEnabled()](#TempETAViewModel+isProgressBarsEnabled) ⇒ <code>boolean</code>
    * [.isHistoricalGraphEnabled()](#TempETAViewModel+isHistoricalGraphEnabled) ⇒ <code>boolean</code>
    * [.getHistoricalGraphWindowSeconds()](#TempETAViewModel+getHistoricalGraphWindowSeconds) ⇒ <code>number</code>
    * [.isHistoricalGraphVisible(heater)](#TempETAViewModel+isHistoricalGraphVisible) ⇒ <code>boolean</code>
    * [._recordHeaterHistory(heaterObj, tsSec, actualC, targetC)](#TempETAViewModel+_recordHeaterHistory) ⇒ <code>void</code>
    * [._resetHistoricalGraphState([info])](#TempETAViewModel+_resetHistoricalGraphState) ⇒ <code>void</code>
    * [._getGraphElements(heaterName)](#TempETAViewModel+_getGraphElements) ⇒ <code>Object</code> \| <code>null</code>
    * [._formatAxisTime(seconds)](#TempETAViewModel+_formatAxisTime) ⇒ <code>string</code>
    * [._formatAxisTemp(tempC)](#TempETAViewModel+_formatAxisTemp) ⇒ <code>string</code>
    * [._isHeaterHeatingNow(etaValue, actualC, targetC)](#TempETAViewModel+_isHeaterHeatingNow) ⇒ <code>boolean</code>
    * [._renderHistoricalGraph(heaterObj)](#TempETAViewModel+_renderHistoricalGraph) ⇒ <code>void</code>
    * [.formatTempDisplay(temp)](#TempETAViewModel+formatTempDisplay) ⇒ <code>string</code>
    * [._cToF(celsius)](#TempETAViewModel+_cToF) ⇒ <code>number</code>
    * [._fToC(fahrenheit)](#TempETAViewModel+_fToC) ⇒ <code>number</code>
    * [._cDeltaToF(deltaC)](#TempETAViewModel+_cDeltaToF) ⇒ <code>number</code>
    * [._fDeltaToC(deltaF)](#TempETAViewModel+_fDeltaToC) ⇒ <code>number</code>
    * [._effectiveThresholdUnit()](#TempETAViewModel+_effectiveThresholdUnit) ⇒ <code>string</code>
    * [.onSettingsBeforeSave()](#TempETAViewModel+onSettingsBeforeSave) ⇒ <code>boolean</code>
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [._effectiveDisplayTargetC(heater)](#TempETAViewModel+_effectiveDisplayTargetC) ⇒ <code>number</code>
    * [.formatTempPair(heater)](#TempETAViewModel+formatTempPair) ⇒ <code>string</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getETAClass(heater)](#TempETAViewModel+getETAClass) ⇒ <code>string</code>
    * [.isProgressVisible(heater)](#TempETAViewModel+isProgressVisible) ⇒ <code>boolean</code>
    * [.isTabProgressVisible(heater)](#TempETAViewModel+isTabProgressVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel+getProgressPercent) ⇒ <code>number</code>
    * [.getProgressBarClass(heater)](#TempETAViewModel+getProgressBarClass) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterIdleClass(heater)](#TempETAViewModel+getHeaterIdleClass) ⇒ <code>string</code>
    * [.sortHeaters(heaters)](#TempETAViewModel+sortHeaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
    * [.getHeaterIcon(heaterName)](#TempETAViewModel+getHeaterIcon) ⇒ <code>string</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="TempETAViewModel+_resolveSettingsRoot"></a>

### tempETAViewModel.\_resolveSettingsRoot() ⇒ <code>Object</code>
<p>Resolve the settings root object across OctoPrint versions.
Returns an object that contains <code>plugins</code> and (optionally) <code>appearance</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>settings root (may be an empty object)</p>
<a name="TempETAViewModel+_getSettingsDialogRoot"></a>

### tempETAViewModel.\_getSettingsDialogRoot() ⇒ <code>jQuery</code> \| <code>null</code>
<p>Get the root element of the plugin settings dialog.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>jQuery</code> \| <code>null</code> - <p>jQuery element or null</p>
<a name="TempETAViewModel+_bindSettingsIfNeeded"></a>

### tempETAViewModel.\_bindSettingsIfNeeded() ⇒ <code>void</code>
<p>Bind the view model to the settings dialog if it hasn't been bound yet.
This supports OctoPrint instances that inject the settings template lazily.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>messages</p>
<a name="TempETAViewModel+_formatValidationMessage"></a>

### tempETAViewModel.\_formatValidationMessage(template, [params]) ⇒ <code>string</code>
<p>Replace named placeholders in a template string like &quot;{min}&quot;.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| template | <code>string</code> | <p>template string with {keys}</p> |
| [params] | <code>Object.&lt;string, \*&gt;</code> | <p>mapping of key-&gt;value</p> |

<a name="TempETAViewModel+_clearValidationForInput"></a>

### tempETAViewModel.\_clearValidationForInput(inputEl) ⇒ <code>void</code>
<p>Clear inline validation UI for an input element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |

<a name="TempETAViewModel+_setValidationForInput"></a>

### tempETAViewModel.\_setValidationForInput(inputEl, message) ⇒ <code>void</code>
<p>Mark an input as invalid and show an inline message.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |
| message | <code>string</code> | <p>validation message to display</p> |

<a name="TempETAViewModel+_isEmptyValue"></a>

### tempETAViewModel.\_isEmptyValue(v) ⇒ <code>boolean</code>
<p>Return whether a value is considered empty for settings inputs.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_parseFiniteNumber"></a>

### tempETAViewModel.\_parseFiniteNumber(v) ⇒ <code>number</code> \| <code>null</code>
<p>Parse a value into a finite number or return null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a numeric input element using <code>min</code>/<code>max</code> attributes and
custom <code>data-allow-empty</code>. Adds inline error message when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true when valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>the input element to validate</p> |

<a name="TempETAViewModel+_installSettingsValidationHandlers"></a>

### tempETAViewModel.\_installSettingsValidationHandlers(rootEl) ⇒ <code>void</code>
<p>Install validation handlers for numeric inputs inside the settings dialog.
This attaches delegated input/change/blur handlers for <code>input[type=&quot;number&quot;]</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| rootEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>Root element of the settings dialog</p> |

<a name="TempETAViewModel+_validateAllSettingsNumbers"></a>

### tempETAViewModel.\_validateAllSettingsNumbers() ⇒ <code>boolean</code>
<p>Validate all numeric settings inputs in the settings dialog.
Blocks save when invalid inputs are found.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if all numeric inputs are valid</p>
<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a single numeric input element according to <code>min</code>/<code>max</code> attributes
and custom data-* attributes used by the settings template. Adds inline
validation messages when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> | <p>The input element to validate</p> |

<a name="TempETAViewModel+_unbindSettingsIfBound"></a>

### tempETAViewModel.\_unbindSettingsIfBound() ⇒ <code>void</code>
<p>Unbind the settings dialog if it was previously bound to this viewmodel.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindSettingsWithRetry"></a>

### tempETAViewModel.\_bindSettingsWithRetry() ⇒ <code>void</code>
<p>Attempt to bind the settings dialog, retrying a small number of times
to handle lazy-injection of the template.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindElementOnce"></a>

### tempETAViewModel.\_bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs]) ⇒ <code>void</code>
<p>Bind a DOM element once, retrying until it appears in the DOM.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| selector | <code>string</code> | <p>DOM selector</p> |
| dataFlag | <code>string</code> | <p>data flag to mark binding</p> |
| [maxAttempts] | <code>number</code> | <p>maximum attempts</p> |
| [delayMs] | <code>number</code> | <p>delay between attempts in ms</p> |

<a name="TempETAViewModel+_installSettingsDialogHooks"></a>

### tempETAViewModel.\_installSettingsDialogHooks() ⇒ <code>void</code>
<p>Install hooks to bind/unbind settings dialog on show/hidden events.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureSidebarBound"></a>

### tempETAViewModel.\_ensureSidebarBound() ⇒ <code>void</code>
<p>Ensure the sidebar view is bound to this viewmodel (lazy binding).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_throttledEnsureSidebarBound"></a>

### tempETAViewModel.\_throttledEnsureSidebarBound() ⇒ <code>void</code>
<p>Throttled wrapper around <code>_ensureSidebarBound</code> to avoid excessive DOM
operations during rapid updates.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isFrontendDebugEnabled"></a>

### tempETAViewModel.\_isFrontendDebugEnabled() ⇒ <code>boolean</code>
<p>Check whether frontend debug logging is enabled via plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_debugLog"></a>

### tempETAViewModel.\_debugLog(key, message, [payload], [minIntervalMs]) ⇒ <code>void</code>
<p>Throttled frontend debug logger. Usage: <code>self._debugLog(key, message, payload, minIntervalMs)</code></p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| key | <code>string</code> | <p>unique key to throttle messages</p> |
| message | <code>string</code> | <p>message to log</p> |
| [payload] | <code>any</code> | <p>optional payload to log</p> |
| [minIntervalMs] | <code>number</code> | <p>minimum interval between logs for this key</p> |

<a name="TempETAViewModel+_getColorMode"></a>

### tempETAViewModel.\_getColorMode() ⇒ <code>string</code>
<p>Return the configured color mode for ETA display ('bands' or 'status').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_readKoString"></a>

### tempETAViewModel.\_readKoString(value, defaultValue) ⇒ <code>string</code>
<p>Read a Knockout observable or plain value as string, with fallback.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| value | <code>any</code> | <p>observable or value</p> |
| defaultValue | <code>string</code> | <p>fallback value</p> |

<a name="TempETAViewModel+_applyStatusColorVariables"></a>

### tempETAViewModel.\_applyStatusColorVariables() ⇒ <code>void</code>
<p>Apply CSS custom properties for status colors from plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_setupExtendedSettingsSubscriptions"></a>

### tempETAViewModel.\_setupExtendedSettingsSubscriptions() ⇒ <code>void</code>
<p>Subscribe to extended settings (colors etc.) and apply on changes.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_i18nAttrOr"></a>

### tempETAViewModel.\_i18nAttrOr(attrName, fallback) ⇒ <code>string</code>
<p>Read an i18n data-attribute from the hidden i18n element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| attrName | <code>string</code> | <p>attribute name</p> |
| fallback | <code>string</code> | <p>fallback string</p> |

<a name="TempETAViewModel+_isSoundEnabled"></a>

### tempETAViewModel.\_isSoundEnabled() ⇒ <code>boolean</code>
<p>Check whether sound alerts are enabled in the plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEnabled"></a>

### tempETAViewModel.\_isNotificationEnabled() ⇒ <code>boolean</code>
<p>Check whether toast notifications are enabled in plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEventEnabled"></a>

### tempETAViewModel.\_isNotificationEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific notification event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| eventKey | <code>string</code> | <p>event identifier (e.g. 'target_reached')</p> |

<a name="TempETAViewModel+_getNotificationTimeoutMs"></a>

### tempETAViewModel.\_getNotificationTimeoutMs() ⇒ <code>number</code>
<p>Get the configured toast timeout in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getNotificationMinIntervalMs"></a>

### tempETAViewModel.\_getNotificationMinIntervalMs() ⇒ <code>number</code>
<p>Get the minimum interval between notification toasts in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_notifyEvent"></a>

### tempETAViewModel.\_notifyEvent(heaterName, eventKey, displayTargetC) ⇒ <code>void</code>
<p>Show a toast notification for a heater event (target reached, cooldown finished).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier</p> |
| eventKey | <code>string</code> | <p>event key ('target_reached'|'cooldown_finished')</p> |
| displayTargetC | <code>number</code> | <p>temperature to display (°C)</p> |

<a name="TempETAViewModel+_isSoundEventEnabled"></a>

### tempETAViewModel.\_isSoundEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific sound event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+_getSoundVolume"></a>

### tempETAViewModel.\_getSoundVolume() ⇒ <code>number</code>
<p>Get configured sound playback volume (0.0 - 1.0).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getSoundMinIntervalMs"></a>

### tempETAViewModel.\_getSoundMinIntervalMs() ⇒ <code>number</code>
<p>Minimum interval between sound events in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureAudioContext"></a>

### tempETAViewModel.\_ensureAudioContext() ⇒ <code>AudioContext</code> \| <code>null</code>
<p>Ensure and return a WebAudio <code>AudioContext</code> if supported.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getStaticSoundUrl"></a>

### tempETAViewModel.\_getStaticSoundUrl(fileName) ⇒ <code>string</code>
<p>Return the URL for a plugin static sound file.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playSoundFile"></a>

### tempETAViewModel.\_playSoundFile(fileName) ⇒ <code>void</code>
<p>Play a static sound file via HTMLAudio (falls back to WebAudio beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playBeep"></a>

### tempETAViewModel.\_playBeep([opts]) ⇒ <code>void</code>
<p>Play a short WebAudio beep. Options: <code>{ force: true, volume: 0.5 }</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [opts] | <code>Object</code> |

<a name="TempETAViewModel+_playSoundEvent"></a>

### tempETAViewModel.\_playSoundEvent(heaterName, eventKey) ⇒ <code>void</code>
<p>Play the configured sound for an event (or fallback beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+testSound"></a>

### tempETAViewModel.testSound() ⇒ <code>void</code>
<p>Trigger the test sound (bound to settings button).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_pluginSettings"></a>

### tempETAViewModel.\_pluginSettings() ⇒ <code>Object</code> \| <code>null</code>
<p>Return the current plugin settings object (Knockout structure) or null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isComponentEnabled"></a>

### tempETAViewModel.isComponentEnabled(component) ⇒ <code>boolean</code>
<p>Return whether a UI component (sidebar/navbar/tab) is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| component | <code>string</code> | <p>one of 'sidebar','navbar','tab'</p> |

<a name="TempETAViewModel+isProgressBarsEnabled"></a>

### tempETAViewModel.isProgressBarsEnabled() ⇒ <code>boolean</code>
<p>Return whether progress bars are enabled in settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphEnabled"></a>

### tempETAViewModel.isHistoricalGraphEnabled() ⇒ <code>boolean</code>
<p>Return whether the historical graph feature is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+getHistoricalGraphWindowSeconds"></a>

### tempETAViewModel.getHistoricalGraphWindowSeconds() ⇒ <code>number</code>
<p>Get the historical graph window length in seconds (configured).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphVisible"></a>

### tempETAViewModel.isHistoricalGraphVisible(heater) ⇒ <code>boolean</code>
<p>Return whether the historical graph should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+_recordHeaterHistory"></a>

### tempETAViewModel.\_recordHeaterHistory(heaterObj, tsSec, actualC, targetC) ⇒ <code>void</code>
<p>Record a heater sample for the historical graph.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |  |
| tsSec | <code>number</code> | <p>timestamp (seconds)</p> |
| actualC | <code>number</code> | <p>actual temperature (°C)</p> |
| targetC | <code>number</code> | <p>target temperature (°C)</p> |

<a name="TempETAViewModel+_resetHistoricalGraphState"></a>

### tempETAViewModel.\_resetHistoricalGraphState([info]) ⇒ <code>void</code>
<p>Reset cached state used by the historical graph rendering.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [info] | <code>Object</code> |

<a name="TempETAViewModel+_getGraphElements"></a>

### tempETAViewModel.\_getGraphElements(heaterName) ⇒ <code>Object</code> \| <code>null</code>
<p>Retrieve cached SVG graph elements for a heater, or query DOM and cache them.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> \| <code>null</code> - <p>elements or null</p>

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+_formatAxisTime"></a>

### tempETAViewModel.\_formatAxisTime(seconds) ⇒ <code>string</code>
<p>Format seconds for axis labels (M:SS).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| seconds | <code>number</code> |

<a name="TempETAViewModel+_formatAxisTemp"></a>

### tempETAViewModel.\_formatAxisTemp(tempC) ⇒ <code>string</code>
<p>Format temperature for axis labels according to display unit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| tempC | <code>number</code> |

<a name="TempETAViewModel+_isHeaterHeatingNow"></a>

### tempETAViewModel.\_isHeaterHeatingNow(etaValue, actualC, targetC) ⇒ <code>boolean</code>
<p>Determine whether a heater is currently heating.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| etaValue | <code>number</code> \| <code>null</code> |
| actualC | <code>number</code> |
| targetC | <code>number</code> |

<a name="TempETAViewModel+_renderHistoricalGraph"></a>

### tempETAViewModel.\_renderHistoricalGraph(heaterObj) ⇒ <code>void</code>
<p>Render the historical graph for a heater into its SVG element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempDisplay"></a>

### tempETAViewModel.formatTempDisplay(temp) ⇒ <code>string</code>
<p>Format a temperature for display according to user settings.
Uses OctoPrint helper if available, otherwise falls back to simple formatting.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>formatted temperature (e.g. &quot;200°C&quot; or &quot;200°C (392°F)&quot;)</p>

| Param | Type | Description |
| --- | --- | --- |
| temp | <code>number</code> | <p>temperature in °C</p> |

<a name="TempETAViewModel+_cToF"></a>

### tempETAViewModel.\_cToF(celsius) ⇒ <code>number</code>
<p>Convert Celsius to Fahrenheit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| celsius | <code>number</code> |

<a name="TempETAViewModel+_fToC"></a>

### tempETAViewModel.\_fToC(fahrenheit) ⇒ <code>number</code>
<p>Convert Fahrenheit to Celsius.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fahrenheit | <code>number</code> |

<a name="TempETAViewModel+_cDeltaToF"></a>

### tempETAViewModel.\_cDeltaToF(deltaC) ⇒ <code>number</code>
<p>Convert a Celsius delta to Fahrenheit delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaC | <code>number</code> |

<a name="TempETAViewModel+_fDeltaToC"></a>

### tempETAViewModel.\_fDeltaToC(deltaF) ⇒ <code>number</code>
<p>Convert a Fahrenheit delta to Celsius delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaF | <code>number</code> |

<a name="TempETAViewModel+_effectiveThresholdUnit"></a>

### tempETAViewModel.\_effectiveThresholdUnit() ⇒ <code>string</code>
<p>Determine the effective unit for threshold display (&quot;c&quot; or &quot;f&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>&quot;c&quot; or &quot;f&quot;</p>
<a name="TempETAViewModel+onSettingsBeforeSave"></a>

### tempETAViewModel.onSettingsBeforeSave() ⇒ <code>boolean</code>
<p>Hook called before settings are saved. Return false to block save.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handler for messages from OctoPrint's data updater plugin.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (expected 'temp_eta')</p> |
| data | [<code>PluginMessage</code>](#PluginMessage) | <p>payload object</p> |

<a name="TempETAViewModel+_effectiveDisplayTargetC"></a>

### tempETAViewModel.\_effectiveDisplayTargetC(heater) ⇒ <code>number</code>
<p>Determine the effective display target (°C) for a heater, using cooldownTarget when cooling.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>number</code> - <p>target in °C or NaN</p>

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempPair"></a>

### tempETAViewModel.formatTempPair(heater) ⇒ <code>string</code>
<p>Format a pair of temperatures (actual/target) for display.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Return whether an ETA value should be shown.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eta | <code>number</code> \| <code>null</code> |

<a name="TempETAViewModel+getETAClass"></a>

### tempETAViewModel.getETAClass(heater) ⇒ <code>string</code>
<p>Return CSS class for ETA display based on heater state and ETA value.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isProgressVisible"></a>

### tempETAViewModel.isProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the progress bar should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isTabProgressVisible"></a>

### tempETAViewModel.isTabProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the tab progress indicator should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressPercent"></a>

### tempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute progress percent for a heater (0-100).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressBarClass"></a>

### tempETAViewModel.getProgressBarClass(heater) ⇒ <code>string</code>
<p>Return CSS class for progress bar based on ETA and color mode.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Human-readable label for a heater name (i18n-aware for known names).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Idle text for a heater (&quot;Idle&quot; or &quot;Cooling&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIdleClass"></a>

### tempETAViewModel.getHeaterIdleClass(heater) ⇒ <code>string</code>
<p>CSS class for idle/heating state.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+sortHeaters"></a>

### tempETAViewModel.sortHeaters(heaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
<p>Sort heaters into display order (tools, bed, chamber).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: [<code>Array.&lt;Heater&gt;</code>](#Heater) - <p>sorted heaters</p>

| Param | Type |
| --- | --- |
| heaters | [<code>Array.&lt;Heater&gt;</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIcon"></a>

### tempETAViewModel.getHeaterIcon(heaterName) ⇒ <code>string</code>
<p>Return a font-awesome icon class for a heater name.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+_resolveSettingsRoot"></a>

### tempETAViewModel.\_resolveSettingsRoot() ⇒ <code>Object</code>
<p>Resolve the settings root object across OctoPrint versions.
Returns an object that contains <code>plugins</code> and (optionally) <code>appearance</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>settings root (may be an empty object)</p>
<a name="TempETAViewModel+_getSettingsDialogRoot"></a>

### tempETAViewModel.\_getSettingsDialogRoot() ⇒ <code>jQuery</code> \| <code>null</code>
<p>Get the root element of the plugin settings dialog.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>jQuery</code> \| <code>null</code> - <p>jQuery element or null</p>
<a name="TempETAViewModel+_bindSettingsIfNeeded"></a>

### tempETAViewModel.\_bindSettingsIfNeeded() ⇒ <code>void</code>
<p>Bind the view model to the settings dialog if it hasn't been bound yet.
This supports OctoPrint instances that inject the settings template lazily.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>messages</p>
<a name="TempETAViewModel+_formatValidationMessage"></a>

### tempETAViewModel.\_formatValidationMessage(template, [params]) ⇒ <code>string</code>
<p>Replace named placeholders in a template string like &quot;{min}&quot;.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| template | <code>string</code> | <p>template string with {keys}</p> |
| [params] | <code>Object.&lt;string, \*&gt;</code> | <p>mapping of key-&gt;value</p> |

<a name="TempETAViewModel+_clearValidationForInput"></a>

### tempETAViewModel.\_clearValidationForInput(inputEl) ⇒ <code>void</code>
<p>Clear inline validation UI for an input element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |

<a name="TempETAViewModel+_setValidationForInput"></a>

### tempETAViewModel.\_setValidationForInput(inputEl, message) ⇒ <code>void</code>
<p>Mark an input as invalid and show an inline message.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |
| message | <code>string</code> | <p>validation message to display</p> |

<a name="TempETAViewModel+_isEmptyValue"></a>

### tempETAViewModel.\_isEmptyValue(v) ⇒ <code>boolean</code>
<p>Return whether a value is considered empty for settings inputs.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_parseFiniteNumber"></a>

### tempETAViewModel.\_parseFiniteNumber(v) ⇒ <code>number</code> \| <code>null</code>
<p>Parse a value into a finite number or return null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a numeric input element using <code>min</code>/<code>max</code> attributes and
custom <code>data-allow-empty</code>. Adds inline error message when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true when valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>the input element to validate</p> |

<a name="TempETAViewModel+_installSettingsValidationHandlers"></a>

### tempETAViewModel.\_installSettingsValidationHandlers(rootEl) ⇒ <code>void</code>
<p>Install validation handlers for numeric inputs inside the settings dialog.
This attaches delegated input/change/blur handlers for <code>input[type=&quot;number&quot;]</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| rootEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>Root element of the settings dialog</p> |

<a name="TempETAViewModel+_validateAllSettingsNumbers"></a>

### tempETAViewModel.\_validateAllSettingsNumbers() ⇒ <code>boolean</code>
<p>Validate all numeric settings inputs in the settings dialog.
Blocks save when invalid inputs are found.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if all numeric inputs are valid</p>
<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a single numeric input element according to <code>min</code>/<code>max</code> attributes
and custom data-* attributes used by the settings template. Adds inline
validation messages when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> | <p>The input element to validate</p> |

<a name="TempETAViewModel+_unbindSettingsIfBound"></a>

### tempETAViewModel.\_unbindSettingsIfBound() ⇒ <code>void</code>
<p>Unbind the settings dialog if it was previously bound to this viewmodel.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindSettingsWithRetry"></a>

### tempETAViewModel.\_bindSettingsWithRetry() ⇒ <code>void</code>
<p>Attempt to bind the settings dialog, retrying a small number of times
to handle lazy-injection of the template.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindElementOnce"></a>

### tempETAViewModel.\_bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs]) ⇒ <code>void</code>
<p>Bind a DOM element once, retrying until it appears in the DOM.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| selector | <code>string</code> | <p>DOM selector</p> |
| dataFlag | <code>string</code> | <p>data flag to mark binding</p> |
| [maxAttempts] | <code>number</code> | <p>maximum attempts</p> |
| [delayMs] | <code>number</code> | <p>delay between attempts in ms</p> |

<a name="TempETAViewModel+_installSettingsDialogHooks"></a>

### tempETAViewModel.\_installSettingsDialogHooks() ⇒ <code>void</code>
<p>Install hooks to bind/unbind settings dialog on show/hidden events.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureSidebarBound"></a>

### tempETAViewModel.\_ensureSidebarBound() ⇒ <code>void</code>
<p>Ensure the sidebar view is bound to this viewmodel (lazy binding).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_throttledEnsureSidebarBound"></a>

### tempETAViewModel.\_throttledEnsureSidebarBound() ⇒ <code>void</code>
<p>Throttled wrapper around <code>_ensureSidebarBound</code> to avoid excessive DOM
operations during rapid updates.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isFrontendDebugEnabled"></a>

### tempETAViewModel.\_isFrontendDebugEnabled() ⇒ <code>boolean</code>
<p>Check whether frontend debug logging is enabled via plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_debugLog"></a>

### tempETAViewModel.\_debugLog(key, message, [payload], [minIntervalMs]) ⇒ <code>void</code>
<p>Throttled frontend debug logger. Usage: <code>self._debugLog(key, message, payload, minIntervalMs)</code></p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| key | <code>string</code> | <p>unique key to throttle messages</p> |
| message | <code>string</code> | <p>message to log</p> |
| [payload] | <code>any</code> | <p>optional payload to log</p> |
| [minIntervalMs] | <code>number</code> | <p>minimum interval between logs for this key</p> |

<a name="TempETAViewModel+_getColorMode"></a>

### tempETAViewModel.\_getColorMode() ⇒ <code>string</code>
<p>Return the configured color mode for ETA display ('bands' or 'status').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_readKoString"></a>

### tempETAViewModel.\_readKoString(value, defaultValue) ⇒ <code>string</code>
<p>Read a Knockout observable or plain value as string, with fallback.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| value | <code>any</code> | <p>observable or value</p> |
| defaultValue | <code>string</code> | <p>fallback value</p> |

<a name="TempETAViewModel+_applyStatusColorVariables"></a>

### tempETAViewModel.\_applyStatusColorVariables() ⇒ <code>void</code>
<p>Apply CSS custom properties for status colors from plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_setupExtendedSettingsSubscriptions"></a>

### tempETAViewModel.\_setupExtendedSettingsSubscriptions() ⇒ <code>void</code>
<p>Subscribe to extended settings (colors etc.) and apply on changes.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_i18nAttrOr"></a>

### tempETAViewModel.\_i18nAttrOr(attrName, fallback) ⇒ <code>string</code>
<p>Read an i18n data-attribute from the hidden i18n element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| attrName | <code>string</code> | <p>attribute name</p> |
| fallback | <code>string</code> | <p>fallback string</p> |

<a name="TempETAViewModel+_isSoundEnabled"></a>

### tempETAViewModel.\_isSoundEnabled() ⇒ <code>boolean</code>
<p>Check whether sound alerts are enabled in the plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEnabled"></a>

### tempETAViewModel.\_isNotificationEnabled() ⇒ <code>boolean</code>
<p>Check whether toast notifications are enabled in plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEventEnabled"></a>

### tempETAViewModel.\_isNotificationEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific notification event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| eventKey | <code>string</code> | <p>event identifier (e.g. 'target_reached')</p> |

<a name="TempETAViewModel+_getNotificationTimeoutMs"></a>

### tempETAViewModel.\_getNotificationTimeoutMs() ⇒ <code>number</code>
<p>Get the configured toast timeout in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getNotificationMinIntervalMs"></a>

### tempETAViewModel.\_getNotificationMinIntervalMs() ⇒ <code>number</code>
<p>Get the minimum interval between notification toasts in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_notifyEvent"></a>

### tempETAViewModel.\_notifyEvent(heaterName, eventKey, displayTargetC) ⇒ <code>void</code>
<p>Show a toast notification for a heater event (target reached, cooldown finished).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier</p> |
| eventKey | <code>string</code> | <p>event key ('target_reached'|'cooldown_finished')</p> |
| displayTargetC | <code>number</code> | <p>temperature to display (°C)</p> |

<a name="TempETAViewModel+_isSoundEventEnabled"></a>

### tempETAViewModel.\_isSoundEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific sound event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+_getSoundVolume"></a>

### tempETAViewModel.\_getSoundVolume() ⇒ <code>number</code>
<p>Get configured sound playback volume (0.0 - 1.0).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getSoundMinIntervalMs"></a>

### tempETAViewModel.\_getSoundMinIntervalMs() ⇒ <code>number</code>
<p>Minimum interval between sound events in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureAudioContext"></a>

### tempETAViewModel.\_ensureAudioContext() ⇒ <code>AudioContext</code> \| <code>null</code>
<p>Ensure and return a WebAudio <code>AudioContext</code> if supported.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getStaticSoundUrl"></a>

### tempETAViewModel.\_getStaticSoundUrl(fileName) ⇒ <code>string</code>
<p>Return the URL for a plugin static sound file.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playSoundFile"></a>

### tempETAViewModel.\_playSoundFile(fileName) ⇒ <code>void</code>
<p>Play a static sound file via HTMLAudio (falls back to WebAudio beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playBeep"></a>

### tempETAViewModel.\_playBeep([opts]) ⇒ <code>void</code>
<p>Play a short WebAudio beep. Options: <code>{ force: true, volume: 0.5 }</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [opts] | <code>Object</code> |

<a name="TempETAViewModel+_playSoundEvent"></a>

### tempETAViewModel.\_playSoundEvent(heaterName, eventKey) ⇒ <code>void</code>
<p>Play the configured sound for an event (or fallback beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+testSound"></a>

### tempETAViewModel.testSound() ⇒ <code>void</code>
<p>Trigger the test sound (bound to settings button).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_pluginSettings"></a>

### tempETAViewModel.\_pluginSettings() ⇒ <code>Object</code> \| <code>null</code>
<p>Return the current plugin settings object (Knockout structure) or null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isComponentEnabled"></a>

### tempETAViewModel.isComponentEnabled(component) ⇒ <code>boolean</code>
<p>Return whether a UI component (sidebar/navbar/tab) is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| component | <code>string</code> | <p>one of 'sidebar','navbar','tab'</p> |

<a name="TempETAViewModel+isProgressBarsEnabled"></a>

### tempETAViewModel.isProgressBarsEnabled() ⇒ <code>boolean</code>
<p>Return whether progress bars are enabled in settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphEnabled"></a>

### tempETAViewModel.isHistoricalGraphEnabled() ⇒ <code>boolean</code>
<p>Return whether the historical graph feature is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+getHistoricalGraphWindowSeconds"></a>

### tempETAViewModel.getHistoricalGraphWindowSeconds() ⇒ <code>number</code>
<p>Get the historical graph window length in seconds (configured).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphVisible"></a>

### tempETAViewModel.isHistoricalGraphVisible(heater) ⇒ <code>boolean</code>
<p>Return whether the historical graph should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+_recordHeaterHistory"></a>

### tempETAViewModel.\_recordHeaterHistory(heaterObj, tsSec, actualC, targetC) ⇒ <code>void</code>
<p>Record a heater sample for the historical graph.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |  |
| tsSec | <code>number</code> | <p>timestamp (seconds)</p> |
| actualC | <code>number</code> | <p>actual temperature (°C)</p> |
| targetC | <code>number</code> | <p>target temperature (°C)</p> |

<a name="TempETAViewModel+_resetHistoricalGraphState"></a>

### tempETAViewModel.\_resetHistoricalGraphState([info]) ⇒ <code>void</code>
<p>Reset cached state used by the historical graph rendering.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [info] | <code>Object</code> |

<a name="TempETAViewModel+_getGraphElements"></a>

### tempETAViewModel.\_getGraphElements(heaterName) ⇒ <code>Object</code> \| <code>null</code>
<p>Retrieve cached SVG graph elements for a heater, or query DOM and cache them.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> \| <code>null</code> - <p>elements or null</p>

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+_formatAxisTime"></a>

### tempETAViewModel.\_formatAxisTime(seconds) ⇒ <code>string</code>
<p>Format seconds for axis labels (M:SS).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| seconds | <code>number</code> |

<a name="TempETAViewModel+_formatAxisTemp"></a>

### tempETAViewModel.\_formatAxisTemp(tempC) ⇒ <code>string</code>
<p>Format temperature for axis labels according to display unit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| tempC | <code>number</code> |

<a name="TempETAViewModel+_isHeaterHeatingNow"></a>

### tempETAViewModel.\_isHeaterHeatingNow(etaValue, actualC, targetC) ⇒ <code>boolean</code>
<p>Determine whether a heater is currently heating.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| etaValue | <code>number</code> \| <code>null</code> |
| actualC | <code>number</code> |
| targetC | <code>number</code> |

<a name="TempETAViewModel+_renderHistoricalGraph"></a>

### tempETAViewModel.\_renderHistoricalGraph(heaterObj) ⇒ <code>void</code>
<p>Render the historical graph for a heater into its SVG element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempDisplay"></a>

### tempETAViewModel.formatTempDisplay(temp) ⇒ <code>string</code>
<p>Format a temperature for display according to user settings.
Uses OctoPrint helper if available, otherwise falls back to simple formatting.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>formatted temperature (e.g. &quot;200°C&quot; or &quot;200°C (392°F)&quot;)</p>

| Param | Type | Description |
| --- | --- | --- |
| temp | <code>number</code> | <p>temperature in °C</p> |

<a name="TempETAViewModel+_cToF"></a>

### tempETAViewModel.\_cToF(celsius) ⇒ <code>number</code>
<p>Convert Celsius to Fahrenheit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| celsius | <code>number</code> |

<a name="TempETAViewModel+_fToC"></a>

### tempETAViewModel.\_fToC(fahrenheit) ⇒ <code>number</code>
<p>Convert Fahrenheit to Celsius.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fahrenheit | <code>number</code> |

<a name="TempETAViewModel+_cDeltaToF"></a>

### tempETAViewModel.\_cDeltaToF(deltaC) ⇒ <code>number</code>
<p>Convert a Celsius delta to Fahrenheit delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaC | <code>number</code> |

<a name="TempETAViewModel+_fDeltaToC"></a>

### tempETAViewModel.\_fDeltaToC(deltaF) ⇒ <code>number</code>
<p>Convert a Fahrenheit delta to Celsius delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaF | <code>number</code> |

<a name="TempETAViewModel+_effectiveThresholdUnit"></a>

### tempETAViewModel.\_effectiveThresholdUnit() ⇒ <code>string</code>
<p>Determine the effective unit for threshold display (&quot;c&quot; or &quot;f&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>&quot;c&quot; or &quot;f&quot;</p>
<a name="TempETAViewModel+onSettingsBeforeSave"></a>

### tempETAViewModel.onSettingsBeforeSave() ⇒ <code>boolean</code>
<p>Hook called before settings are saved. Return false to block save.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handler for messages from OctoPrint's data updater plugin.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (expected 'temp_eta')</p> |
| data | [<code>PluginMessage</code>](#PluginMessage) | <p>payload object</p> |

<a name="TempETAViewModel+_effectiveDisplayTargetC"></a>

### tempETAViewModel.\_effectiveDisplayTargetC(heater) ⇒ <code>number</code>
<p>Determine the effective display target (°C) for a heater, using cooldownTarget when cooling.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>number</code> - <p>target in °C or NaN</p>

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempPair"></a>

### tempETAViewModel.formatTempPair(heater) ⇒ <code>string</code>
<p>Format a pair of temperatures (actual/target) for display.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Return whether an ETA value should be shown.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eta | <code>number</code> \| <code>null</code> |

<a name="TempETAViewModel+getETAClass"></a>

### tempETAViewModel.getETAClass(heater) ⇒ <code>string</code>
<p>Return CSS class for ETA display based on heater state and ETA value.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isProgressVisible"></a>

### tempETAViewModel.isProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the progress bar should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isTabProgressVisible"></a>

### tempETAViewModel.isTabProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the tab progress indicator should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressPercent"></a>

### tempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute progress percent for a heater (0-100).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressBarClass"></a>

### tempETAViewModel.getProgressBarClass(heater) ⇒ <code>string</code>
<p>Return CSS class for progress bar based on ETA and color mode.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Human-readable label for a heater name (i18n-aware for known names).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Idle text for a heater (&quot;Idle&quot; or &quot;Cooling&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIdleClass"></a>

### tempETAViewModel.getHeaterIdleClass(heater) ⇒ <code>string</code>
<p>CSS class for idle/heating state.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+sortHeaters"></a>

### tempETAViewModel.sortHeaters(heaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
<p>Sort heaters into display order (tools, bed, chamber).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: [<code>Array.&lt;Heater&gt;</code>](#Heater) - <p>sorted heaters</p>

| Param | Type |
| --- | --- |
| heaters | [<code>Array.&lt;Heater&gt;</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIcon"></a>

### tempETAViewModel.getHeaterIcon(heaterName) ⇒ <code>string</code>
<p>Return a font-awesome icon class for a heater name.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="PluginMessage"></a>

## PluginMessage : <code>Object</code>
<p>TempETAViewModel</p>

**Kind**: global class
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| name | <code>string</code> | <p>heater id (e.g. 'tool0', 'bed')</p> |
| actual | <code>function</code> \| <code>ko.observable.&lt;(number\|null)&gt;</code> | <p>current temperature observable or number</p> |
| target | <code>function</code> \| <code>ko.observable.&lt;(number\|null)&gt;</code> | <p>target temperature observable or number</p> |
| [cooldownTarget] | <code>function</code> \| <code>ko.observable.&lt;(number\|null)&gt;</code> | <p>optional cooldown target observable or number</p> |
| [etaKind] | <code>function</code> \| <code>ko.observable.&lt;string&gt;</code> | <p>'heating'|'cooling' or similar observable</p> |
| [_history] | [<code>Array.&lt;HeaterHistoryEntry&gt;</code>](#HeaterHistoryEntry) | <p>internal history array of samples</p> |
| [_historyStart] | <code>number</code> | <p>index where retained history begins</p> |
| time | <code>number</code> | <p>epoch seconds (or ms depending on implementation) of sample</p> |
| temp | <code>number</code> | <p>temperature in °C</p> |
| [color_mode] | <code>string</code> |  |
| [progress_bars_enabled] | <code>boolean</code> |  |
| [historical_graph_window_seconds] | <code>number</code> |  |
| [debug_logging] | <code>boolean</code> |  |
| enabled | <code>boolean</code> |  |
| volume | <code>number</code> |  |
| files | <code>Array.&lt;string&gt;</code> |  |
| type | <code>string</code> | <p>message type (e.g. 'eta_update','history_reset','settings_reset')</p> |
| [heater] | <code>string</code> | <p>heater id for 'eta_update'</p> |
| [eta] | <code>number</code> |  |
| [eta_kind] | <code>string</code> |  |
| [cooldown_target] | <code>number</code> \| <code>null</code> |  |
| [actual] | <code>number</code> \| <code>null</code> |  |
| [target] | <code>number</code> \| <code>null</code> | <p>TempETAViewModel</p> <p>Main Knockout view model for the Temperature ETA plugin. The <code>parameters</code> array contains OctoPrint view models in the standard order the plugin expects (settings, printerState, printerProfiles, loginState, ...).</p> |


* [PluginMessage](#PluginMessage) : <code>Object</code>
    * [new PluginMessage(parameters)](#new_PluginMessage_new)
    * [new PluginMessage(parameters)](#new_PluginMessage_new)

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |

<a name="TempETAViewModel"></a>

## TempETAViewModel
**Kind**: global class

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [._resolveSettingsRoot()](#TempETAViewModel+_resolveSettingsRoot) ⇒ <code>Object</code>
    * [._getSettingsDialogRoot()](#TempETAViewModel+_getSettingsDialogRoot) ⇒ <code>jQuery</code> \| <code>null</code>
    * [._bindSettingsIfNeeded()](#TempETAViewModel+_bindSettingsIfNeeded) ⇒ <code>void</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._formatValidationMessage(template, [params])](#TempETAViewModel+_formatValidationMessage) ⇒ <code>string</code>
    * [._clearValidationForInput(inputEl)](#TempETAViewModel+_clearValidationForInput) ⇒ <code>void</code>
    * [._setValidationForInput(inputEl, message)](#TempETAViewModel+_setValidationForInput) ⇒ <code>void</code>
    * [._isEmptyValue(v)](#TempETAViewModel+_isEmptyValue) ⇒ <code>boolean</code>
    * [._parseFiniteNumber(v)](#TempETAViewModel+_parseFiniteNumber) ⇒ <code>number</code> \| <code>null</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._installSettingsValidationHandlers(rootEl)](#TempETAViewModel+_installSettingsValidationHandlers) ⇒ <code>void</code>
    * [._validateAllSettingsNumbers()](#TempETAViewModel+_validateAllSettingsNumbers) ⇒ <code>boolean</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._unbindSettingsIfBound()](#TempETAViewModel+_unbindSettingsIfBound) ⇒ <code>void</code>
    * [._bindSettingsWithRetry()](#TempETAViewModel+_bindSettingsWithRetry) ⇒ <code>void</code>
    * [._bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs])](#TempETAViewModel+_bindElementOnce) ⇒ <code>void</code>
    * [._installSettingsDialogHooks()](#TempETAViewModel+_installSettingsDialogHooks) ⇒ <code>void</code>
    * [._ensureSidebarBound()](#TempETAViewModel+_ensureSidebarBound) ⇒ <code>void</code>
    * [._throttledEnsureSidebarBound()](#TempETAViewModel+_throttledEnsureSidebarBound) ⇒ <code>void</code>
    * [._isFrontendDebugEnabled()](#TempETAViewModel+_isFrontendDebugEnabled) ⇒ <code>boolean</code>
    * [._debugLog(key, message, [payload], [minIntervalMs])](#TempETAViewModel+_debugLog) ⇒ <code>void</code>
    * [._getColorMode()](#TempETAViewModel+_getColorMode) ⇒ <code>string</code>
    * [._readKoString(value, defaultValue)](#TempETAViewModel+_readKoString) ⇒ <code>string</code>
    * [._applyStatusColorVariables()](#TempETAViewModel+_applyStatusColorVariables) ⇒ <code>void</code>
    * [._setupExtendedSettingsSubscriptions()](#TempETAViewModel+_setupExtendedSettingsSubscriptions) ⇒ <code>void</code>
    * [._i18nAttrOr(attrName, fallback)](#TempETAViewModel+_i18nAttrOr) ⇒ <code>string</code>
    * [._isSoundEnabled()](#TempETAViewModel+_isSoundEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEnabled()](#TempETAViewModel+_isNotificationEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEventEnabled(eventKey)](#TempETAViewModel+_isNotificationEventEnabled) ⇒ <code>boolean</code>
    * [._getNotificationTimeoutMs()](#TempETAViewModel+_getNotificationTimeoutMs) ⇒ <code>number</code>
    * [._getNotificationMinIntervalMs()](#TempETAViewModel+_getNotificationMinIntervalMs) ⇒ <code>number</code>
    * [._notifyEvent(heaterName, eventKey, displayTargetC)](#TempETAViewModel+_notifyEvent) ⇒ <code>void</code>
    * [._isSoundEventEnabled(eventKey)](#TempETAViewModel+_isSoundEventEnabled) ⇒ <code>boolean</code>
    * [._getSoundVolume()](#TempETAViewModel+_getSoundVolume) ⇒ <code>number</code>
    * [._getSoundMinIntervalMs()](#TempETAViewModel+_getSoundMinIntervalMs) ⇒ <code>number</code>
    * [._ensureAudioContext()](#TempETAViewModel+_ensureAudioContext) ⇒ <code>AudioContext</code> \| <code>null</code>
    * [._getStaticSoundUrl(fileName)](#TempETAViewModel+_getStaticSoundUrl) ⇒ <code>string</code>
    * [._playSoundFile(fileName)](#TempETAViewModel+_playSoundFile) ⇒ <code>void</code>
    * [._playBeep([opts])](#TempETAViewModel+_playBeep) ⇒ <code>void</code>
    * [._playSoundEvent(heaterName, eventKey)](#TempETAViewModel+_playSoundEvent) ⇒ <code>void</code>
    * [.testSound()](#TempETAViewModel+testSound) ⇒ <code>void</code>
    * [._pluginSettings()](#TempETAViewModel+_pluginSettings) ⇒ <code>Object</code> \| <code>null</code>
    * [.isComponentEnabled(component)](#TempETAViewModel+isComponentEnabled) ⇒ <code>boolean</code>
    * [.isProgressBarsEnabled()](#TempETAViewModel+isProgressBarsEnabled) ⇒ <code>boolean</code>
    * [.isHistoricalGraphEnabled()](#TempETAViewModel+isHistoricalGraphEnabled) ⇒ <code>boolean</code>
    * [.getHistoricalGraphWindowSeconds()](#TempETAViewModel+getHistoricalGraphWindowSeconds) ⇒ <code>number</code>
    * [.isHistoricalGraphVisible(heater)](#TempETAViewModel+isHistoricalGraphVisible) ⇒ <code>boolean</code>
    * [._recordHeaterHistory(heaterObj, tsSec, actualC, targetC)](#TempETAViewModel+_recordHeaterHistory) ⇒ <code>void</code>
    * [._resetHistoricalGraphState([info])](#TempETAViewModel+_resetHistoricalGraphState) ⇒ <code>void</code>
    * [._getGraphElements(heaterName)](#TempETAViewModel+_getGraphElements) ⇒ <code>Object</code> \| <code>null</code>
    * [._formatAxisTime(seconds)](#TempETAViewModel+_formatAxisTime) ⇒ <code>string</code>
    * [._formatAxisTemp(tempC)](#TempETAViewModel+_formatAxisTemp) ⇒ <code>string</code>
    * [._isHeaterHeatingNow(etaValue, actualC, targetC)](#TempETAViewModel+_isHeaterHeatingNow) ⇒ <code>boolean</code>
    * [._renderHistoricalGraph(heaterObj)](#TempETAViewModel+_renderHistoricalGraph) ⇒ <code>void</code>
    * [.formatTempDisplay(temp)](#TempETAViewModel+formatTempDisplay) ⇒ <code>string</code>
    * [._cToF(celsius)](#TempETAViewModel+_cToF) ⇒ <code>number</code>
    * [._fToC(fahrenheit)](#TempETAViewModel+_fToC) ⇒ <code>number</code>
    * [._cDeltaToF(deltaC)](#TempETAViewModel+_cDeltaToF) ⇒ <code>number</code>
    * [._fDeltaToC(deltaF)](#TempETAViewModel+_fDeltaToC) ⇒ <code>number</code>
    * [._effectiveThresholdUnit()](#TempETAViewModel+_effectiveThresholdUnit) ⇒ <code>string</code>
    * [.onSettingsBeforeSave()](#TempETAViewModel+onSettingsBeforeSave) ⇒ <code>boolean</code>
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [._effectiveDisplayTargetC(heater)](#TempETAViewModel+_effectiveDisplayTargetC) ⇒ <code>number</code>
    * [.formatTempPair(heater)](#TempETAViewModel+formatTempPair) ⇒ <code>string</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getETAClass(heater)](#TempETAViewModel+getETAClass) ⇒ <code>string</code>
    * [.isProgressVisible(heater)](#TempETAViewModel+isProgressVisible) ⇒ <code>boolean</code>
    * [.isTabProgressVisible(heater)](#TempETAViewModel+isTabProgressVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel+getProgressPercent) ⇒ <code>number</code>
    * [.getProgressBarClass(heater)](#TempETAViewModel+getProgressBarClass) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterIdleClass(heater)](#TempETAViewModel+getHeaterIdleClass) ⇒ <code>string</code>
    * [.sortHeaters(heaters)](#TempETAViewModel+sortHeaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
    * [.getHeaterIcon(heaterName)](#TempETAViewModel+getHeaterIcon) ⇒ <code>string</code>
    * [._resolveSettingsRoot()](#TempETAViewModel+_resolveSettingsRoot) ⇒ <code>Object</code>
    * [._getSettingsDialogRoot()](#TempETAViewModel+_getSettingsDialogRoot) ⇒ <code>jQuery</code> \| <code>null</code>
    * [._bindSettingsIfNeeded()](#TempETAViewModel+_bindSettingsIfNeeded) ⇒ <code>void</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._getValidationMessages()](#TempETAViewModel+_getValidationMessages) ⇒ <code>Object</code>
    * [._formatValidationMessage(template, [params])](#TempETAViewModel+_formatValidationMessage) ⇒ <code>string</code>
    * [._clearValidationForInput(inputEl)](#TempETAViewModel+_clearValidationForInput) ⇒ <code>void</code>
    * [._setValidationForInput(inputEl, message)](#TempETAViewModel+_setValidationForInput) ⇒ <code>void</code>
    * [._isEmptyValue(v)](#TempETAViewModel+_isEmptyValue) ⇒ <code>boolean</code>
    * [._parseFiniteNumber(v)](#TempETAViewModel+_parseFiniteNumber) ⇒ <code>number</code> \| <code>null</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._installSettingsValidationHandlers(rootEl)](#TempETAViewModel+_installSettingsValidationHandlers) ⇒ <code>void</code>
    * [._validateAllSettingsNumbers()](#TempETAViewModel+_validateAllSettingsNumbers) ⇒ <code>boolean</code>
    * [._validateNumberInput(inputEl)](#TempETAViewModel+_validateNumberInput) ⇒ <code>boolean</code>
    * [._unbindSettingsIfBound()](#TempETAViewModel+_unbindSettingsIfBound) ⇒ <code>void</code>
    * [._bindSettingsWithRetry()](#TempETAViewModel+_bindSettingsWithRetry) ⇒ <code>void</code>
    * [._bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs])](#TempETAViewModel+_bindElementOnce) ⇒ <code>void</code>
    * [._installSettingsDialogHooks()](#TempETAViewModel+_installSettingsDialogHooks) ⇒ <code>void</code>
    * [._ensureSidebarBound()](#TempETAViewModel+_ensureSidebarBound) ⇒ <code>void</code>
    * [._throttledEnsureSidebarBound()](#TempETAViewModel+_throttledEnsureSidebarBound) ⇒ <code>void</code>
    * [._isFrontendDebugEnabled()](#TempETAViewModel+_isFrontendDebugEnabled) ⇒ <code>boolean</code>
    * [._debugLog(key, message, [payload], [minIntervalMs])](#TempETAViewModel+_debugLog) ⇒ <code>void</code>
    * [._getColorMode()](#TempETAViewModel+_getColorMode) ⇒ <code>string</code>
    * [._readKoString(value, defaultValue)](#TempETAViewModel+_readKoString) ⇒ <code>string</code>
    * [._applyStatusColorVariables()](#TempETAViewModel+_applyStatusColorVariables) ⇒ <code>void</code>
    * [._setupExtendedSettingsSubscriptions()](#TempETAViewModel+_setupExtendedSettingsSubscriptions) ⇒ <code>void</code>
    * [._i18nAttrOr(attrName, fallback)](#TempETAViewModel+_i18nAttrOr) ⇒ <code>string</code>
    * [._isSoundEnabled()](#TempETAViewModel+_isSoundEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEnabled()](#TempETAViewModel+_isNotificationEnabled) ⇒ <code>boolean</code>
    * [._isNotificationEventEnabled(eventKey)](#TempETAViewModel+_isNotificationEventEnabled) ⇒ <code>boolean</code>
    * [._getNotificationTimeoutMs()](#TempETAViewModel+_getNotificationTimeoutMs) ⇒ <code>number</code>
    * [._getNotificationMinIntervalMs()](#TempETAViewModel+_getNotificationMinIntervalMs) ⇒ <code>number</code>
    * [._notifyEvent(heaterName, eventKey, displayTargetC)](#TempETAViewModel+_notifyEvent) ⇒ <code>void</code>
    * [._isSoundEventEnabled(eventKey)](#TempETAViewModel+_isSoundEventEnabled) ⇒ <code>boolean</code>
    * [._getSoundVolume()](#TempETAViewModel+_getSoundVolume) ⇒ <code>number</code>
    * [._getSoundMinIntervalMs()](#TempETAViewModel+_getSoundMinIntervalMs) ⇒ <code>number</code>
    * [._ensureAudioContext()](#TempETAViewModel+_ensureAudioContext) ⇒ <code>AudioContext</code> \| <code>null</code>
    * [._getStaticSoundUrl(fileName)](#TempETAViewModel+_getStaticSoundUrl) ⇒ <code>string</code>
    * [._playSoundFile(fileName)](#TempETAViewModel+_playSoundFile) ⇒ <code>void</code>
    * [._playBeep([opts])](#TempETAViewModel+_playBeep) ⇒ <code>void</code>
    * [._playSoundEvent(heaterName, eventKey)](#TempETAViewModel+_playSoundEvent) ⇒ <code>void</code>
    * [.testSound()](#TempETAViewModel+testSound) ⇒ <code>void</code>
    * [._pluginSettings()](#TempETAViewModel+_pluginSettings) ⇒ <code>Object</code> \| <code>null</code>
    * [.isComponentEnabled(component)](#TempETAViewModel+isComponentEnabled) ⇒ <code>boolean</code>
    * [.isProgressBarsEnabled()](#TempETAViewModel+isProgressBarsEnabled) ⇒ <code>boolean</code>
    * [.isHistoricalGraphEnabled()](#TempETAViewModel+isHistoricalGraphEnabled) ⇒ <code>boolean</code>
    * [.getHistoricalGraphWindowSeconds()](#TempETAViewModel+getHistoricalGraphWindowSeconds) ⇒ <code>number</code>
    * [.isHistoricalGraphVisible(heater)](#TempETAViewModel+isHistoricalGraphVisible) ⇒ <code>boolean</code>
    * [._recordHeaterHistory(heaterObj, tsSec, actualC, targetC)](#TempETAViewModel+_recordHeaterHistory) ⇒ <code>void</code>
    * [._resetHistoricalGraphState([info])](#TempETAViewModel+_resetHistoricalGraphState) ⇒ <code>void</code>
    * [._getGraphElements(heaterName)](#TempETAViewModel+_getGraphElements) ⇒ <code>Object</code> \| <code>null</code>
    * [._formatAxisTime(seconds)](#TempETAViewModel+_formatAxisTime) ⇒ <code>string</code>
    * [._formatAxisTemp(tempC)](#TempETAViewModel+_formatAxisTemp) ⇒ <code>string</code>
    * [._isHeaterHeatingNow(etaValue, actualC, targetC)](#TempETAViewModel+_isHeaterHeatingNow) ⇒ <code>boolean</code>
    * [._renderHistoricalGraph(heaterObj)](#TempETAViewModel+_renderHistoricalGraph) ⇒ <code>void</code>
    * [.formatTempDisplay(temp)](#TempETAViewModel+formatTempDisplay) ⇒ <code>string</code>
    * [._cToF(celsius)](#TempETAViewModel+_cToF) ⇒ <code>number</code>
    * [._fToC(fahrenheit)](#TempETAViewModel+_fToC) ⇒ <code>number</code>
    * [._cDeltaToF(deltaC)](#TempETAViewModel+_cDeltaToF) ⇒ <code>number</code>
    * [._fDeltaToC(deltaF)](#TempETAViewModel+_fDeltaToC) ⇒ <code>number</code>
    * [._effectiveThresholdUnit()](#TempETAViewModel+_effectiveThresholdUnit) ⇒ <code>string</code>
    * [.onSettingsBeforeSave()](#TempETAViewModel+onSettingsBeforeSave) ⇒ <code>boolean</code>
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [._effectiveDisplayTargetC(heater)](#TempETAViewModel+_effectiveDisplayTargetC) ⇒ <code>number</code>
    * [.formatTempPair(heater)](#TempETAViewModel+formatTempPair) ⇒ <code>string</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getETAClass(heater)](#TempETAViewModel+getETAClass) ⇒ <code>string</code>
    * [.isProgressVisible(heater)](#TempETAViewModel+isProgressVisible) ⇒ <code>boolean</code>
    * [.isTabProgressVisible(heater)](#TempETAViewModel+isTabProgressVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel+getProgressPercent) ⇒ <code>number</code>
    * [.getProgressBarClass(heater)](#TempETAViewModel+getProgressBarClass) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterIdleClass(heater)](#TempETAViewModel+getHeaterIdleClass) ⇒ <code>string</code>
    * [.sortHeaters(heaters)](#TempETAViewModel+sortHeaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
    * [.getHeaterIcon(heaterName)](#TempETAViewModel+getHeaterIcon) ⇒ <code>string</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="TempETAViewModel+_resolveSettingsRoot"></a>

### tempETAViewModel.\_resolveSettingsRoot() ⇒ <code>Object</code>
<p>Resolve the settings root object across OctoPrint versions.
Returns an object that contains <code>plugins</code> and (optionally) <code>appearance</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>settings root (may be an empty object)</p>
<a name="TempETAViewModel+_getSettingsDialogRoot"></a>

### tempETAViewModel.\_getSettingsDialogRoot() ⇒ <code>jQuery</code> \| <code>null</code>
<p>Get the root element of the plugin settings dialog.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>jQuery</code> \| <code>null</code> - <p>jQuery element or null</p>
<a name="TempETAViewModel+_bindSettingsIfNeeded"></a>

### tempETAViewModel.\_bindSettingsIfNeeded() ⇒ <code>void</code>
<p>Bind the view model to the settings dialog if it hasn't been bound yet.
This supports OctoPrint instances that inject the settings template lazily.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>messages</p>
<a name="TempETAViewModel+_formatValidationMessage"></a>

### tempETAViewModel.\_formatValidationMessage(template, [params]) ⇒ <code>string</code>
<p>Replace named placeholders in a template string like &quot;{min}&quot;.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| template | <code>string</code> | <p>template string with {keys}</p> |
| [params] | <code>Object.&lt;string, \*&gt;</code> | <p>mapping of key-&gt;value</p> |

<a name="TempETAViewModel+_clearValidationForInput"></a>

### tempETAViewModel.\_clearValidationForInput(inputEl) ⇒ <code>void</code>
<p>Clear inline validation UI for an input element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |

<a name="TempETAViewModel+_setValidationForInput"></a>

### tempETAViewModel.\_setValidationForInput(inputEl, message) ⇒ <code>void</code>
<p>Mark an input as invalid and show an inline message.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |
| message | <code>string</code> | <p>validation message to display</p> |

<a name="TempETAViewModel+_isEmptyValue"></a>

### tempETAViewModel.\_isEmptyValue(v) ⇒ <code>boolean</code>
<p>Return whether a value is considered empty for settings inputs.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_parseFiniteNumber"></a>

### tempETAViewModel.\_parseFiniteNumber(v) ⇒ <code>number</code> \| <code>null</code>
<p>Parse a value into a finite number or return null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a numeric input element using <code>min</code>/<code>max</code> attributes and
custom <code>data-allow-empty</code>. Adds inline error message when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true when valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>the input element to validate</p> |

<a name="TempETAViewModel+_installSettingsValidationHandlers"></a>

### tempETAViewModel.\_installSettingsValidationHandlers(rootEl) ⇒ <code>void</code>
<p>Install validation handlers for numeric inputs inside the settings dialog.
This attaches delegated input/change/blur handlers for <code>input[type=&quot;number&quot;]</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| rootEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>Root element of the settings dialog</p> |

<a name="TempETAViewModel+_validateAllSettingsNumbers"></a>

### tempETAViewModel.\_validateAllSettingsNumbers() ⇒ <code>boolean</code>
<p>Validate all numeric settings inputs in the settings dialog.
Blocks save when invalid inputs are found.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if all numeric inputs are valid</p>
<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a single numeric input element according to <code>min</code>/<code>max</code> attributes
and custom data-* attributes used by the settings template. Adds inline
validation messages when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> | <p>The input element to validate</p> |

<a name="TempETAViewModel+_unbindSettingsIfBound"></a>

### tempETAViewModel.\_unbindSettingsIfBound() ⇒ <code>void</code>
<p>Unbind the settings dialog if it was previously bound to this viewmodel.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindSettingsWithRetry"></a>

### tempETAViewModel.\_bindSettingsWithRetry() ⇒ <code>void</code>
<p>Attempt to bind the settings dialog, retrying a small number of times
to handle lazy-injection of the template.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindElementOnce"></a>

### tempETAViewModel.\_bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs]) ⇒ <code>void</code>
<p>Bind a DOM element once, retrying until it appears in the DOM.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| selector | <code>string</code> | <p>DOM selector</p> |
| dataFlag | <code>string</code> | <p>data flag to mark binding</p> |
| [maxAttempts] | <code>number</code> | <p>maximum attempts</p> |
| [delayMs] | <code>number</code> | <p>delay between attempts in ms</p> |

<a name="TempETAViewModel+_installSettingsDialogHooks"></a>

### tempETAViewModel.\_installSettingsDialogHooks() ⇒ <code>void</code>
<p>Install hooks to bind/unbind settings dialog on show/hidden events.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureSidebarBound"></a>

### tempETAViewModel.\_ensureSidebarBound() ⇒ <code>void</code>
<p>Ensure the sidebar view is bound to this viewmodel (lazy binding).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_throttledEnsureSidebarBound"></a>

### tempETAViewModel.\_throttledEnsureSidebarBound() ⇒ <code>void</code>
<p>Throttled wrapper around <code>_ensureSidebarBound</code> to avoid excessive DOM
operations during rapid updates.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isFrontendDebugEnabled"></a>

### tempETAViewModel.\_isFrontendDebugEnabled() ⇒ <code>boolean</code>
<p>Check whether frontend debug logging is enabled via plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_debugLog"></a>

### tempETAViewModel.\_debugLog(key, message, [payload], [minIntervalMs]) ⇒ <code>void</code>
<p>Throttled frontend debug logger. Usage: <code>self._debugLog(key, message, payload, minIntervalMs)</code></p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| key | <code>string</code> | <p>unique key to throttle messages</p> |
| message | <code>string</code> | <p>message to log</p> |
| [payload] | <code>any</code> | <p>optional payload to log</p> |
| [minIntervalMs] | <code>number</code> | <p>minimum interval between logs for this key</p> |

<a name="TempETAViewModel+_getColorMode"></a>

### tempETAViewModel.\_getColorMode() ⇒ <code>string</code>
<p>Return the configured color mode for ETA display ('bands' or 'status').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_readKoString"></a>

### tempETAViewModel.\_readKoString(value, defaultValue) ⇒ <code>string</code>
<p>Read a Knockout observable or plain value as string, with fallback.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| value | <code>any</code> | <p>observable or value</p> |
| defaultValue | <code>string</code> | <p>fallback value</p> |

<a name="TempETAViewModel+_applyStatusColorVariables"></a>

### tempETAViewModel.\_applyStatusColorVariables() ⇒ <code>void</code>
<p>Apply CSS custom properties for status colors from plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_setupExtendedSettingsSubscriptions"></a>

### tempETAViewModel.\_setupExtendedSettingsSubscriptions() ⇒ <code>void</code>
<p>Subscribe to extended settings (colors etc.) and apply on changes.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_i18nAttrOr"></a>

### tempETAViewModel.\_i18nAttrOr(attrName, fallback) ⇒ <code>string</code>
<p>Read an i18n data-attribute from the hidden i18n element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| attrName | <code>string</code> | <p>attribute name</p> |
| fallback | <code>string</code> | <p>fallback string</p> |

<a name="TempETAViewModel+_isSoundEnabled"></a>

### tempETAViewModel.\_isSoundEnabled() ⇒ <code>boolean</code>
<p>Check whether sound alerts are enabled in the plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEnabled"></a>

### tempETAViewModel.\_isNotificationEnabled() ⇒ <code>boolean</code>
<p>Check whether toast notifications are enabled in plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEventEnabled"></a>

### tempETAViewModel.\_isNotificationEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific notification event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| eventKey | <code>string</code> | <p>event identifier (e.g. 'target_reached')</p> |

<a name="TempETAViewModel+_getNotificationTimeoutMs"></a>

### tempETAViewModel.\_getNotificationTimeoutMs() ⇒ <code>number</code>
<p>Get the configured toast timeout in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getNotificationMinIntervalMs"></a>

### tempETAViewModel.\_getNotificationMinIntervalMs() ⇒ <code>number</code>
<p>Get the minimum interval between notification toasts in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_notifyEvent"></a>

### tempETAViewModel.\_notifyEvent(heaterName, eventKey, displayTargetC) ⇒ <code>void</code>
<p>Show a toast notification for a heater event (target reached, cooldown finished).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier</p> |
| eventKey | <code>string</code> | <p>event key ('target_reached'|'cooldown_finished')</p> |
| displayTargetC | <code>number</code> | <p>temperature to display (°C)</p> |

<a name="TempETAViewModel+_isSoundEventEnabled"></a>

### tempETAViewModel.\_isSoundEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific sound event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+_getSoundVolume"></a>

### tempETAViewModel.\_getSoundVolume() ⇒ <code>number</code>
<p>Get configured sound playback volume (0.0 - 1.0).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getSoundMinIntervalMs"></a>

### tempETAViewModel.\_getSoundMinIntervalMs() ⇒ <code>number</code>
<p>Minimum interval between sound events in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureAudioContext"></a>

### tempETAViewModel.\_ensureAudioContext() ⇒ <code>AudioContext</code> \| <code>null</code>
<p>Ensure and return a WebAudio <code>AudioContext</code> if supported.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getStaticSoundUrl"></a>

### tempETAViewModel.\_getStaticSoundUrl(fileName) ⇒ <code>string</code>
<p>Return the URL for a plugin static sound file.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playSoundFile"></a>

### tempETAViewModel.\_playSoundFile(fileName) ⇒ <code>void</code>
<p>Play a static sound file via HTMLAudio (falls back to WebAudio beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playBeep"></a>

### tempETAViewModel.\_playBeep([opts]) ⇒ <code>void</code>
<p>Play a short WebAudio beep. Options: <code>{ force: true, volume: 0.5 }</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [opts] | <code>Object</code> |

<a name="TempETAViewModel+_playSoundEvent"></a>

### tempETAViewModel.\_playSoundEvent(heaterName, eventKey) ⇒ <code>void</code>
<p>Play the configured sound for an event (or fallback beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+testSound"></a>

### tempETAViewModel.testSound() ⇒ <code>void</code>
<p>Trigger the test sound (bound to settings button).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_pluginSettings"></a>

### tempETAViewModel.\_pluginSettings() ⇒ <code>Object</code> \| <code>null</code>
<p>Return the current plugin settings object (Knockout structure) or null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isComponentEnabled"></a>

### tempETAViewModel.isComponentEnabled(component) ⇒ <code>boolean</code>
<p>Return whether a UI component (sidebar/navbar/tab) is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| component | <code>string</code> | <p>one of 'sidebar','navbar','tab'</p> |

<a name="TempETAViewModel+isProgressBarsEnabled"></a>

### tempETAViewModel.isProgressBarsEnabled() ⇒ <code>boolean</code>
<p>Return whether progress bars are enabled in settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphEnabled"></a>

### tempETAViewModel.isHistoricalGraphEnabled() ⇒ <code>boolean</code>
<p>Return whether the historical graph feature is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+getHistoricalGraphWindowSeconds"></a>

### tempETAViewModel.getHistoricalGraphWindowSeconds() ⇒ <code>number</code>
<p>Get the historical graph window length in seconds (configured).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphVisible"></a>

### tempETAViewModel.isHistoricalGraphVisible(heater) ⇒ <code>boolean</code>
<p>Return whether the historical graph should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+_recordHeaterHistory"></a>

### tempETAViewModel.\_recordHeaterHistory(heaterObj, tsSec, actualC, targetC) ⇒ <code>void</code>
<p>Record a heater sample for the historical graph.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |  |
| tsSec | <code>number</code> | <p>timestamp (seconds)</p> |
| actualC | <code>number</code> | <p>actual temperature (°C)</p> |
| targetC | <code>number</code> | <p>target temperature (°C)</p> |

<a name="TempETAViewModel+_resetHistoricalGraphState"></a>

### tempETAViewModel.\_resetHistoricalGraphState([info]) ⇒ <code>void</code>
<p>Reset cached state used by the historical graph rendering.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [info] | <code>Object</code> |

<a name="TempETAViewModel+_getGraphElements"></a>

### tempETAViewModel.\_getGraphElements(heaterName) ⇒ <code>Object</code> \| <code>null</code>
<p>Retrieve cached SVG graph elements for a heater, or query DOM and cache them.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> \| <code>null</code> - <p>elements or null</p>

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+_formatAxisTime"></a>

### tempETAViewModel.\_formatAxisTime(seconds) ⇒ <code>string</code>
<p>Format seconds for axis labels (M:SS).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| seconds | <code>number</code> |

<a name="TempETAViewModel+_formatAxisTemp"></a>

### tempETAViewModel.\_formatAxisTemp(tempC) ⇒ <code>string</code>
<p>Format temperature for axis labels according to display unit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| tempC | <code>number</code> |

<a name="TempETAViewModel+_isHeaterHeatingNow"></a>

### tempETAViewModel.\_isHeaterHeatingNow(etaValue, actualC, targetC) ⇒ <code>boolean</code>
<p>Determine whether a heater is currently heating.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| etaValue | <code>number</code> \| <code>null</code> |
| actualC | <code>number</code> |
| targetC | <code>number</code> |

<a name="TempETAViewModel+_renderHistoricalGraph"></a>

### tempETAViewModel.\_renderHistoricalGraph(heaterObj) ⇒ <code>void</code>
<p>Render the historical graph for a heater into its SVG element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempDisplay"></a>

### tempETAViewModel.formatTempDisplay(temp) ⇒ <code>string</code>
<p>Format a temperature for display according to user settings.
Uses OctoPrint helper if available, otherwise falls back to simple formatting.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>formatted temperature (e.g. &quot;200°C&quot; or &quot;200°C (392°F)&quot;)</p>

| Param | Type | Description |
| --- | --- | --- |
| temp | <code>number</code> | <p>temperature in °C</p> |

<a name="TempETAViewModel+_cToF"></a>

### tempETAViewModel.\_cToF(celsius) ⇒ <code>number</code>
<p>Convert Celsius to Fahrenheit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| celsius | <code>number</code> |

<a name="TempETAViewModel+_fToC"></a>

### tempETAViewModel.\_fToC(fahrenheit) ⇒ <code>number</code>
<p>Convert Fahrenheit to Celsius.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fahrenheit | <code>number</code> |

<a name="TempETAViewModel+_cDeltaToF"></a>

### tempETAViewModel.\_cDeltaToF(deltaC) ⇒ <code>number</code>
<p>Convert a Celsius delta to Fahrenheit delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaC | <code>number</code> |

<a name="TempETAViewModel+_fDeltaToC"></a>

### tempETAViewModel.\_fDeltaToC(deltaF) ⇒ <code>number</code>
<p>Convert a Fahrenheit delta to Celsius delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaF | <code>number</code> |

<a name="TempETAViewModel+_effectiveThresholdUnit"></a>

### tempETAViewModel.\_effectiveThresholdUnit() ⇒ <code>string</code>
<p>Determine the effective unit for threshold display (&quot;c&quot; or &quot;f&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>&quot;c&quot; or &quot;f&quot;</p>
<a name="TempETAViewModel+onSettingsBeforeSave"></a>

### tempETAViewModel.onSettingsBeforeSave() ⇒ <code>boolean</code>
<p>Hook called before settings are saved. Return false to block save.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handler for messages from OctoPrint's data updater plugin.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (expected 'temp_eta')</p> |
| data | [<code>PluginMessage</code>](#PluginMessage) | <p>payload object</p> |

<a name="TempETAViewModel+_effectiveDisplayTargetC"></a>

### tempETAViewModel.\_effectiveDisplayTargetC(heater) ⇒ <code>number</code>
<p>Determine the effective display target (°C) for a heater, using cooldownTarget when cooling.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>number</code> - <p>target in °C or NaN</p>

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempPair"></a>

### tempETAViewModel.formatTempPair(heater) ⇒ <code>string</code>
<p>Format a pair of temperatures (actual/target) for display.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Return whether an ETA value should be shown.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eta | <code>number</code> \| <code>null</code> |

<a name="TempETAViewModel+getETAClass"></a>

### tempETAViewModel.getETAClass(heater) ⇒ <code>string</code>
<p>Return CSS class for ETA display based on heater state and ETA value.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isProgressVisible"></a>

### tempETAViewModel.isProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the progress bar should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isTabProgressVisible"></a>

### tempETAViewModel.isTabProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the tab progress indicator should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressPercent"></a>

### tempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute progress percent for a heater (0-100).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressBarClass"></a>

### tempETAViewModel.getProgressBarClass(heater) ⇒ <code>string</code>
<p>Return CSS class for progress bar based on ETA and color mode.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Human-readable label for a heater name (i18n-aware for known names).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Idle text for a heater (&quot;Idle&quot; or &quot;Cooling&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIdleClass"></a>

### tempETAViewModel.getHeaterIdleClass(heater) ⇒ <code>string</code>
<p>CSS class for idle/heating state.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+sortHeaters"></a>

### tempETAViewModel.sortHeaters(heaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
<p>Sort heaters into display order (tools, bed, chamber).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: [<code>Array.&lt;Heater&gt;</code>](#Heater) - <p>sorted heaters</p>

| Param | Type |
| --- | --- |
| heaters | [<code>Array.&lt;Heater&gt;</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIcon"></a>

### tempETAViewModel.getHeaterIcon(heaterName) ⇒ <code>string</code>
<p>Return a font-awesome icon class for a heater name.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+_resolveSettingsRoot"></a>

### tempETAViewModel.\_resolveSettingsRoot() ⇒ <code>Object</code>
<p>Resolve the settings root object across OctoPrint versions.
Returns an object that contains <code>plugins</code> and (optionally) <code>appearance</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>settings root (may be an empty object)</p>
<a name="TempETAViewModel+_getSettingsDialogRoot"></a>

### tempETAViewModel.\_getSettingsDialogRoot() ⇒ <code>jQuery</code> \| <code>null</code>
<p>Get the root element of the plugin settings dialog.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>jQuery</code> \| <code>null</code> - <p>jQuery element or null</p>
<a name="TempETAViewModel+_bindSettingsIfNeeded"></a>

### tempETAViewModel.\_bindSettingsIfNeeded() ⇒ <code>void</code>
<p>Bind the view model to the settings dialog if it hasn't been bound yet.
This supports OctoPrint instances that inject the settings template lazily.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getValidationMessages"></a>

### tempETAViewModel.\_getValidationMessages() ⇒ <code>Object</code>
<p>Retrieve localized validation message templates used by the settings UI.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> - <p>messages</p>
<a name="TempETAViewModel+_formatValidationMessage"></a>

### tempETAViewModel.\_formatValidationMessage(template, [params]) ⇒ <code>string</code>
<p>Replace named placeholders in a template string like &quot;{min}&quot;.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| template | <code>string</code> | <p>template string with {keys}</p> |
| [params] | <code>Object.&lt;string, \*&gt;</code> | <p>mapping of key-&gt;value</p> |

<a name="TempETAViewModel+_clearValidationForInput"></a>

### tempETAViewModel.\_clearValidationForInput(inputEl) ⇒ <code>void</code>
<p>Clear inline validation UI for an input element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |

<a name="TempETAViewModel+_setValidationForInput"></a>

### tempETAViewModel.\_setValidationForInput(inputEl, message) ⇒ <code>void</code>
<p>Mark an input as invalid and show an inline message.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>input element</p> |
| message | <code>string</code> | <p>validation message to display</p> |

<a name="TempETAViewModel+_isEmptyValue"></a>

### tempETAViewModel.\_isEmptyValue(v) ⇒ <code>boolean</code>
<p>Return whether a value is considered empty for settings inputs.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_parseFiniteNumber"></a>

### tempETAViewModel.\_parseFiniteNumber(v) ⇒ <code>number</code> \| <code>null</code>
<p>Parse a value into a finite number or return null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| v | <code>\*</code> |

<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a numeric input element using <code>min</code>/<code>max</code> attributes and
custom <code>data-allow-empty</code>. Adds inline error message when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true when valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>the input element to validate</p> |

<a name="TempETAViewModel+_installSettingsValidationHandlers"></a>

### tempETAViewModel.\_installSettingsValidationHandlers(rootEl) ⇒ <code>void</code>
<p>Install validation handlers for numeric inputs inside the settings dialog.
This attaches delegated input/change/blur handlers for <code>input[type=&quot;number&quot;]</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| rootEl | <code>HTMLElement</code> \| <code>jQuery</code> | <p>Root element of the settings dialog</p> |

<a name="TempETAViewModel+_validateAllSettingsNumbers"></a>

### tempETAViewModel.\_validateAllSettingsNumbers() ⇒ <code>boolean</code>
<p>Validate all numeric settings inputs in the settings dialog.
Blocks save when invalid inputs are found.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if all numeric inputs are valid</p>
<a name="TempETAViewModel+_validateNumberInput"></a>

### tempETAViewModel.\_validateNumberInput(inputEl) ⇒ <code>boolean</code>
<p>Validate a single numeric input element according to <code>min</code>/<code>max</code> attributes
and custom data-* attributes used by the settings template. Adds inline
validation messages when invalid.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if valid</p>

| Param | Type | Description |
| --- | --- | --- |
| inputEl | <code>HTMLElement</code> | <p>The input element to validate</p> |

<a name="TempETAViewModel+_unbindSettingsIfBound"></a>

### tempETAViewModel.\_unbindSettingsIfBound() ⇒ <code>void</code>
<p>Unbind the settings dialog if it was previously bound to this viewmodel.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindSettingsWithRetry"></a>

### tempETAViewModel.\_bindSettingsWithRetry() ⇒ <code>void</code>
<p>Attempt to bind the settings dialog, retrying a small number of times
to handle lazy-injection of the template.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_bindElementOnce"></a>

### tempETAViewModel.\_bindElementOnce(selector, dataFlag, [maxAttempts], [delayMs]) ⇒ <code>void</code>
<p>Bind a DOM element once, retrying until it appears in the DOM.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| selector | <code>string</code> | <p>DOM selector</p> |
| dataFlag | <code>string</code> | <p>data flag to mark binding</p> |
| [maxAttempts] | <code>number</code> | <p>maximum attempts</p> |
| [delayMs] | <code>number</code> | <p>delay between attempts in ms</p> |

<a name="TempETAViewModel+_installSettingsDialogHooks"></a>

### tempETAViewModel.\_installSettingsDialogHooks() ⇒ <code>void</code>
<p>Install hooks to bind/unbind settings dialog on show/hidden events.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureSidebarBound"></a>

### tempETAViewModel.\_ensureSidebarBound() ⇒ <code>void</code>
<p>Ensure the sidebar view is bound to this viewmodel (lazy binding).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_throttledEnsureSidebarBound"></a>

### tempETAViewModel.\_throttledEnsureSidebarBound() ⇒ <code>void</code>
<p>Throttled wrapper around <code>_ensureSidebarBound</code> to avoid excessive DOM
operations during rapid updates.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isFrontendDebugEnabled"></a>

### tempETAViewModel.\_isFrontendDebugEnabled() ⇒ <code>boolean</code>
<p>Check whether frontend debug logging is enabled via plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_debugLog"></a>

### tempETAViewModel.\_debugLog(key, message, [payload], [minIntervalMs]) ⇒ <code>void</code>
<p>Throttled frontend debug logger. Usage: <code>self._debugLog(key, message, payload, minIntervalMs)</code></p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| key | <code>string</code> | <p>unique key to throttle messages</p> |
| message | <code>string</code> | <p>message to log</p> |
| [payload] | <code>any</code> | <p>optional payload to log</p> |
| [minIntervalMs] | <code>number</code> | <p>minimum interval between logs for this key</p> |

<a name="TempETAViewModel+_getColorMode"></a>

### tempETAViewModel.\_getColorMode() ⇒ <code>string</code>
<p>Return the configured color mode for ETA display ('bands' or 'status').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_readKoString"></a>

### tempETAViewModel.\_readKoString(value, defaultValue) ⇒ <code>string</code>
<p>Read a Knockout observable or plain value as string, with fallback.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| value | <code>any</code> | <p>observable or value</p> |
| defaultValue | <code>string</code> | <p>fallback value</p> |

<a name="TempETAViewModel+_applyStatusColorVariables"></a>

### tempETAViewModel.\_applyStatusColorVariables() ⇒ <code>void</code>
<p>Apply CSS custom properties for status colors from plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_setupExtendedSettingsSubscriptions"></a>

### tempETAViewModel.\_setupExtendedSettingsSubscriptions() ⇒ <code>void</code>
<p>Subscribe to extended settings (colors etc.) and apply on changes.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_i18nAttrOr"></a>

### tempETAViewModel.\_i18nAttrOr(attrName, fallback) ⇒ <code>string</code>
<p>Read an i18n data-attribute from the hidden i18n element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| attrName | <code>string</code> | <p>attribute name</p> |
| fallback | <code>string</code> | <p>fallback string</p> |

<a name="TempETAViewModel+_isSoundEnabled"></a>

### tempETAViewModel.\_isSoundEnabled() ⇒ <code>boolean</code>
<p>Check whether sound alerts are enabled in the plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEnabled"></a>

### tempETAViewModel.\_isNotificationEnabled() ⇒ <code>boolean</code>
<p>Check whether toast notifications are enabled in plugin settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_isNotificationEventEnabled"></a>

### tempETAViewModel.\_isNotificationEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific notification event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| eventKey | <code>string</code> | <p>event identifier (e.g. 'target_reached')</p> |

<a name="TempETAViewModel+_getNotificationTimeoutMs"></a>

### tempETAViewModel.\_getNotificationTimeoutMs() ⇒ <code>number</code>
<p>Get the configured toast timeout in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getNotificationMinIntervalMs"></a>

### tempETAViewModel.\_getNotificationMinIntervalMs() ⇒ <code>number</code>
<p>Get the minimum interval between notification toasts in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_notifyEvent"></a>

### tempETAViewModel.\_notifyEvent(heaterName, eventKey, displayTargetC) ⇒ <code>void</code>
<p>Show a toast notification for a heater event (target reached, cooldown finished).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier</p> |
| eventKey | <code>string</code> | <p>event key ('target_reached'|'cooldown_finished')</p> |
| displayTargetC | <code>number</code> | <p>temperature to display (°C)</p> |

<a name="TempETAViewModel+_isSoundEventEnabled"></a>

### tempETAViewModel.\_isSoundEventEnabled(eventKey) ⇒ <code>boolean</code>
<p>Return whether a specific sound event is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+_getSoundVolume"></a>

### tempETAViewModel.\_getSoundVolume() ⇒ <code>number</code>
<p>Get configured sound playback volume (0.0 - 1.0).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getSoundMinIntervalMs"></a>

### tempETAViewModel.\_getSoundMinIntervalMs() ⇒ <code>number</code>
<p>Minimum interval between sound events in milliseconds.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_ensureAudioContext"></a>

### tempETAViewModel.\_ensureAudioContext() ⇒ <code>AudioContext</code> \| <code>null</code>
<p>Ensure and return a WebAudio <code>AudioContext</code> if supported.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_getStaticSoundUrl"></a>

### tempETAViewModel.\_getStaticSoundUrl(fileName) ⇒ <code>string</code>
<p>Return the URL for a plugin static sound file.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playSoundFile"></a>

### tempETAViewModel.\_playSoundFile(fileName) ⇒ <code>void</code>
<p>Play a static sound file via HTMLAudio (falls back to WebAudio beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fileName | <code>string</code> |

<a name="TempETAViewModel+_playBeep"></a>

### tempETAViewModel.\_playBeep([opts]) ⇒ <code>void</code>
<p>Play a short WebAudio beep. Options: <code>{ force: true, volume: 0.5 }</code>.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [opts] | <code>Object</code> |

<a name="TempETAViewModel+_playSoundEvent"></a>

### tempETAViewModel.\_playSoundEvent(heaterName, eventKey) ⇒ <code>void</code>
<p>Play the configured sound for an event (or fallback beep).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |
| eventKey | <code>string</code> |

<a name="TempETAViewModel+testSound"></a>

### tempETAViewModel.testSound() ⇒ <code>void</code>
<p>Trigger the test sound (bound to settings button).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+_pluginSettings"></a>

### tempETAViewModel.\_pluginSettings() ⇒ <code>Object</code> \| <code>null</code>
<p>Return the current plugin settings object (Knockout structure) or null.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isComponentEnabled"></a>

### tempETAViewModel.isComponentEnabled(component) ⇒ <code>boolean</code>
<p>Return whether a UI component (sidebar/navbar/tab) is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| component | <code>string</code> | <p>one of 'sidebar','navbar','tab'</p> |

<a name="TempETAViewModel+isProgressBarsEnabled"></a>

### tempETAViewModel.isProgressBarsEnabled() ⇒ <code>boolean</code>
<p>Return whether progress bars are enabled in settings.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphEnabled"></a>

### tempETAViewModel.isHistoricalGraphEnabled() ⇒ <code>boolean</code>
<p>Return whether the historical graph feature is enabled.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+getHistoricalGraphWindowSeconds"></a>

### tempETAViewModel.getHistoricalGraphWindowSeconds() ⇒ <code>number</code>
<p>Get the historical graph window length in seconds (configured).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+isHistoricalGraphVisible"></a>

### tempETAViewModel.isHistoricalGraphVisible(heater) ⇒ <code>boolean</code>
<p>Return whether the historical graph should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+_recordHeaterHistory"></a>

### tempETAViewModel.\_recordHeaterHistory(heaterObj, tsSec, actualC, targetC) ⇒ <code>void</code>
<p>Record a heater sample for the historical graph.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |  |
| tsSec | <code>number</code> | <p>timestamp (seconds)</p> |
| actualC | <code>number</code> | <p>actual temperature (°C)</p> |
| targetC | <code>number</code> | <p>target temperature (°C)</p> |

<a name="TempETAViewModel+_resetHistoricalGraphState"></a>

### tempETAViewModel.\_resetHistoricalGraphState([info]) ⇒ <code>void</code>
<p>Reset cached state used by the historical graph rendering.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| [info] | <code>Object</code> |

<a name="TempETAViewModel+_getGraphElements"></a>

### tempETAViewModel.\_getGraphElements(heaterName) ⇒ <code>Object</code> \| <code>null</code>
<p>Retrieve cached SVG graph elements for a heater, or query DOM and cache them.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>Object</code> \| <code>null</code> - <p>elements or null</p>

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+_formatAxisTime"></a>

### tempETAViewModel.\_formatAxisTime(seconds) ⇒ <code>string</code>
<p>Format seconds for axis labels (M:SS).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| seconds | <code>number</code> |

<a name="TempETAViewModel+_formatAxisTemp"></a>

### tempETAViewModel.\_formatAxisTemp(tempC) ⇒ <code>string</code>
<p>Format temperature for axis labels according to display unit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| tempC | <code>number</code> |

<a name="TempETAViewModel+_isHeaterHeatingNow"></a>

### tempETAViewModel.\_isHeaterHeatingNow(etaValue, actualC, targetC) ⇒ <code>boolean</code>
<p>Determine whether a heater is currently heating.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| etaValue | <code>number</code> \| <code>null</code> |
| actualC | <code>number</code> |
| targetC | <code>number</code> |

<a name="TempETAViewModel+_renderHistoricalGraph"></a>

### tempETAViewModel.\_renderHistoricalGraph(heaterObj) ⇒ <code>void</code>
<p>Render the historical graph for a heater into its SVG element.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterObj | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempDisplay"></a>

### tempETAViewModel.formatTempDisplay(temp) ⇒ <code>string</code>
<p>Format a temperature for display according to user settings.
Uses OctoPrint helper if available, otherwise falls back to simple formatting.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>formatted temperature (e.g. &quot;200°C&quot; or &quot;200°C (392°F)&quot;)</p>

| Param | Type | Description |
| --- | --- | --- |
| temp | <code>number</code> | <p>temperature in °C</p> |

<a name="TempETAViewModel+_cToF"></a>

### tempETAViewModel.\_cToF(celsius) ⇒ <code>number</code>
<p>Convert Celsius to Fahrenheit.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| celsius | <code>number</code> |

<a name="TempETAViewModel+_fToC"></a>

### tempETAViewModel.\_fToC(fahrenheit) ⇒ <code>number</code>
<p>Convert Fahrenheit to Celsius.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| fahrenheit | <code>number</code> |

<a name="TempETAViewModel+_cDeltaToF"></a>

### tempETAViewModel.\_cDeltaToF(deltaC) ⇒ <code>number</code>
<p>Convert a Celsius delta to Fahrenheit delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaC | <code>number</code> |

<a name="TempETAViewModel+_fDeltaToC"></a>

### tempETAViewModel.\_fDeltaToC(deltaF) ⇒ <code>number</code>
<p>Convert a Fahrenheit delta to Celsius delta.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| deltaF | <code>number</code> |

<a name="TempETAViewModel+_effectiveThresholdUnit"></a>

### tempETAViewModel.\_effectiveThresholdUnit() ⇒ <code>string</code>
<p>Determine the effective unit for threshold display (&quot;c&quot; or &quot;f&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>&quot;c&quot; or &quot;f&quot;</p>
<a name="TempETAViewModel+onSettingsBeforeSave"></a>

### tempETAViewModel.onSettingsBeforeSave() ⇒ <code>boolean</code>
<p>Hook called before settings are saved. Return false to block save.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handler for messages from OctoPrint's data updater plugin.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (expected 'temp_eta')</p> |
| data | [<code>PluginMessage</code>](#PluginMessage) | <p>payload object</p> |

<a name="TempETAViewModel+_effectiveDisplayTargetC"></a>

### tempETAViewModel.\_effectiveDisplayTargetC(heater) ⇒ <code>number</code>
<p>Determine the effective display target (°C) for a heater, using cooldownTarget when cooling.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>number</code> - <p>target in °C or NaN</p>

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+formatTempPair"></a>

### tempETAViewModel.formatTempPair(heater) ⇒ <code>string</code>
<p>Format a pair of temperatures (actual/target) for display.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Return whether an ETA value should be shown.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| eta | <code>number</code> \| <code>null</code> |

<a name="TempETAViewModel+getETAClass"></a>

### tempETAViewModel.getETAClass(heater) ⇒ <code>string</code>
<p>Return CSS class for ETA display based on heater state and ETA value.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isProgressVisible"></a>

### tempETAViewModel.isProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the progress bar should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+isTabProgressVisible"></a>

### tempETAViewModel.isTabProgressVisible(heater) ⇒ <code>boolean</code>
<p>Whether the tab progress indicator should be visible for a heater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressPercent"></a>

### tempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute progress percent for a heater (0-100).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getProgressBarClass"></a>

### tempETAViewModel.getProgressBarClass(heater) ⇒ <code>string</code>
<p>Return CSS class for progress bar based on ETA and color mode.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Human-readable label for a heater name (i18n-aware for known names).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Idle text for a heater (&quot;Idle&quot; or &quot;Cooling&quot;).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIdleClass"></a>

### tempETAViewModel.getHeaterIdleClass(heater) ⇒ <code>string</code>
<p>CSS class for idle/heating state.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) |

<a name="TempETAViewModel+sortHeaters"></a>

### tempETAViewModel.sortHeaters(heaters) ⇒ [<code>Array.&lt;Heater&gt;</code>](#Heater)
<p>Sort heaters into display order (tools, bed, chamber).</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: [<code>Array.&lt;Heater&gt;</code>](#Heater) - <p>sorted heaters</p>

| Param | Type |
| --- | --- |
| heaters | [<code>Array.&lt;Heater&gt;</code>](#Heater) |

<a name="TempETAViewModel+getHeaterIcon"></a>

### tempETAViewModel.getHeaterIcon(heaterName) ⇒ <code>string</code>
<p>Return a font-awesome icon class for a heater name.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type |
| --- | --- |
| heaterName | <code>string</code> |

<a name="PluginMessage"></a>

## PluginMessage : <code>Object</code>
<p>TempETAViewModel</p>

**Kind**: global class
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| name | <code>string</code> | <p>heater id (e.g. 'tool0', 'bed')</p> |
| actual | <code>function</code> \| <code>ko.observable.&lt;(number\|null)&gt;</code> | <p>current temperature observable or number</p> |
| target | <code>function</code> \| <code>ko.observable.&lt;(number\|null)&gt;</code> | <p>target temperature observable or number</p> |
| [cooldownTarget] | <code>function</code> \| <code>ko.observable.&lt;(number\|null)&gt;</code> | <p>optional cooldown target observable or number</p> |
| [etaKind] | <code>function</code> \| <code>ko.observable.&lt;string&gt;</code> | <p>'heating'|'cooling' or similar observable</p> |
| [_history] | [<code>Array.&lt;HeaterHistoryEntry&gt;</code>](#HeaterHistoryEntry) | <p>internal history array of samples</p> |
| [_historyStart] | <code>number</code> | <p>index where retained history begins</p> |
| time | <code>number</code> | <p>epoch seconds (or ms depending on implementation) of sample</p> |
| temp | <code>number</code> | <p>temperature in °C</p> |
| [color_mode] | <code>string</code> |  |
| [progress_bars_enabled] | <code>boolean</code> |  |
| [historical_graph_window_seconds] | <code>number</code> |  |
| [debug_logging] | <code>boolean</code> |  |
| enabled | <code>boolean</code> |  |
| volume | <code>number</code> |  |
| files | <code>Array.&lt;string&gt;</code> |  |
| type | <code>string</code> | <p>message type (e.g. 'eta_update','history_reset','settings_reset')</p> |
| [heater] | <code>string</code> | <p>heater id for 'eta_update'</p> |
| [eta] | <code>number</code> |  |
| [eta_kind] | <code>string</code> |  |
| [cooldown_target] | <code>number</code> \| <code>null</code> |  |
| [actual] | <code>number</code> \| <code>null</code> |  |
| [target] | <code>number</code> \| <code>null</code> | <p>TempETAViewModel</p> <p>Main Knockout view model for the Temperature ETA plugin. The <code>parameters</code> array contains OctoPrint view models in the standard order the plugin expects (settings, printerState, printerProfiles, loginState, ...).</p> |


* [PluginMessage](#PluginMessage) : <code>Object</code>
    * [new PluginMessage(parameters)](#new_PluginMessage_new)
    * [new PluginMessage(parameters)](#new_PluginMessage_new)

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |

<a name="resetProfileHistoryHandler"></a>

## resetProfileHistoryHandler(e)
<p>Handler for the &quot;Reset Profile History&quot; settings button.
Delegated click handler so it works regardless of template binding timing.</p>

**Kind**: global function

| Param | Type | Description |
| --- | --- | --- |
| e | <code>Event</code> | <p>Click event</p> |

<a name="restoreDefaultsHandler"></a>

## restoreDefaultsHandler(e)
<p>Handler for the &quot;Restore Defaults&quot; settings button.
Invokes OctoPrint's <code>simpleApiCommand</code> to instruct the plugin to reset
settings to their defaults.</p>

**Kind**: global function

| Param | Type | Description |
| --- | --- | --- |
| e | <code>Event</code> | <p>Click event</p> |

<a name="calculateETA"></a>

## calculateETA(history, target) ⇒ <code>number</code>
<p>calculateETA (placeholder documentation)</p>
<p>ETA calculation is primarily performed on the backend for accuracy and
consistency. If a client-side implementation exists in the future, it
should accept a <code>history</code> array of [HeaterHistoryEntry](#HeaterHistoryEntry) and a numeric <code>target</code>.</p>

**Kind**: global function
**Returns**: <code>number</code> - <p>Seconds to reach target, or null if unavailable</p>

| Param | Type | Description |
| --- | --- | --- |
| history | [<code>Array.&lt;HeaterHistoryEntry&gt;</code>](#HeaterHistoryEntry) | <p>Array of recent samples</p> |
| target | <code>number</code> | <p>Target temperature in Celsius</p> |

<a name="resetProfileHistoryHandler"></a>

## resetProfileHistoryHandler(e)
<p>Handler for the &quot;Reset Profile History&quot; settings button.
Delegated click handler so it works regardless of template binding timing.</p>

**Kind**: global function

| Param | Type | Description |
| --- | --- | --- |
| e | <code>Event</code> | <p>Click event</p> |

<a name="restoreDefaultsHandler"></a>

## restoreDefaultsHandler(e)
<p>Handler for the &quot;Restore Defaults&quot; settings button.
Invokes OctoPrint's <code>simpleApiCommand</code> to instruct the plugin to reset
settings to their defaults.</p>

**Kind**: global function

| Param | Type | Description |
| --- | --- | --- |
| e | <code>Event</code> | <p>Click event</p> |

<a name="calculateETA"></a>

## calculateETA(history, target) ⇒ <code>number</code>
<p>calculateETA (placeholder documentation)</p>
<p>ETA calculation is primarily performed on the backend for accuracy and
consistency. If a client-side implementation exists in the future, it
should accept a <code>history</code> array of [HeaterHistoryEntry](#HeaterHistoryEntry) and a numeric <code>target</code>.</p>

**Kind**: global function
**Returns**: <code>number</code> - <p>Seconds to reach target, or null if unavailable</p>

| Param | Type | Description |
| --- | --- | --- |
| history | [<code>Array.&lt;HeaterHistoryEntry&gt;</code>](#HeaterHistoryEntry) | <p>Array of recent samples</p> |
| target | <code>number</code> | <p>Target temperature in Celsius</p> |

<a name="Heater"></a>

## Heater : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| name | <code>string</code> | <p>heater id (e.g. 'tool0', 'bed')</p> |
| actual | <code>function</code> \| <code>number</code> \| <code>null</code> | <p>current temperature observable or number</p> |
| target | <code>function</code> \| <code>number</code> \| <code>null</code> | <p>target temperature observable or number</p> |
| [cooldownTarget] | <code>function</code> \| <code>number</code> \| <code>null</code> |  |
| [etaKind] | <code>function</code> \| <code>string</code> \| <code>null</code> |  |
| [_history] | [<code>Array.&lt;HeaterHistoryEntry&gt;</code>](#HeaterHistoryEntry) |  |
| [_historyStart] | <code>number</code> |  |

<a name="HeaterHistoryEntry"></a>

## HeaterHistoryEntry : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| t | <code>number</code> | <p>epoch seconds of sample</p> |
| a | <code>number</code> | <p>actual temp</p> |
| [tg] | <code>number</code> \| <code>null</code> | <p>recorded target</p> |

<a name="PluginSettings"></a>

## PluginSettings : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type |
| --- | --- |
| [color_mode] | <code>string</code> |
| [show_in_sidebar] | <code>boolean</code> |
| [show_in_navbar] | <code>boolean</code> |
| [show_in_tab] | <code>boolean</code> |
| [historical_graph_window_seconds] | <code>number</code> |
| [debug_logging] | <code>boolean</code> |

<a name="SoundConfig"></a>

## SoundConfig : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type |
| --- | --- |
| enabled | <code>boolean</code> |
| volume | <code>number</code> |
| files | <code>Array.&lt;string&gt;</code> |

<a name="PluginMessage"></a>

## PluginMessage : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type |
| --- | --- |
| type | <code>string</code> |
| [heater] | <code>string</code> |
| [eta] | <code>number</code> |
| [eta_kind] | <code>string</code> |
| [cooldown_target] | <code>number</code> \| <code>null</code> |
| [actual] | <code>number</code> \| <code>null</code> |
| [target] | <code>number</code> \| <code>null</code> |


* [PluginMessage](#PluginMessage) : <code>Object</code>
    * [new PluginMessage(parameters)](#new_PluginMessage_new)
    * [new PluginMessage(parameters)](#new_PluginMessage_new)

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |

<a name="Heater"></a>

## Heater : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| name | <code>string</code> | <p>heater id (e.g. 'tool0', 'bed')</p> |
| actual | <code>function</code> \| <code>number</code> \| <code>null</code> | <p>current temperature observable or number</p> |
| target | <code>function</code> \| <code>number</code> \| <code>null</code> | <p>target temperature observable or number</p> |
| [cooldownTarget] | <code>function</code> \| <code>number</code> \| <code>null</code> |  |
| [etaKind] | <code>function</code> \| <code>string</code> \| <code>null</code> |  |
| [_history] | [<code>Array.&lt;HeaterHistoryEntry&gt;</code>](#HeaterHistoryEntry) |  |
| [_historyStart] | <code>number</code> |  |

<a name="HeaterHistoryEntry"></a>

## HeaterHistoryEntry : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| t | <code>number</code> | <p>epoch seconds of sample</p> |
| a | <code>number</code> | <p>actual temp</p> |
| [tg] | <code>number</code> \| <code>null</code> | <p>recorded target</p> |

<a name="PluginSettings"></a>

## PluginSettings : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type |
| --- | --- |
| [color_mode] | <code>string</code> |
| [show_in_sidebar] | <code>boolean</code> |
| [show_in_navbar] | <code>boolean</code> |
| [show_in_tab] | <code>boolean</code> |
| [historical_graph_window_seconds] | <code>number</code> |
| [debug_logging] | <code>boolean</code> |

<a name="SoundConfig"></a>

## SoundConfig : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type |
| --- | --- |
| enabled | <code>boolean</code> |
| volume | <code>number</code> |
| files | <code>Array.&lt;string&gt;</code> |

<a name="PluginMessage"></a>

## PluginMessage : <code>Object</code>
**Kind**: global typedef
**Properties**

| Name | Type |
| --- | --- |
| type | <code>string</code> |
| [heater] | <code>string</code> |
| [eta] | <code>number</code> |
| [eta_kind] | <code>string</code> |
| [cooldown_target] | <code>number</code> \| <code>null</code> |
| [actual] | <code>number</code> \| <code>null</code> |
| [target] | <code>number</code> \| <code>null</code> |


* [PluginMessage](#PluginMessage) : <code>Object</code>
    * [new PluginMessage(parameters)](#new_PluginMessage_new)
    * [new PluginMessage(parameters)](#new_PluginMessage_new)

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |

<a name="new_PluginMessage_new"></a>

### new PluginMessage(parameters)
<p>Complex types used throughout the TempETAViewModel.</p>


| Param | Type | Description |
| --- | --- | --- |
| parameters | <code>Array</code> | <p>OctoPrint-injected view model parameters</p> |
