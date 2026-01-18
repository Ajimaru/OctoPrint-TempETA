## Classes

<dl>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd></dd>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd></dd>
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
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block exists in the runtime file but should not be used as a
source for generated API documentation (see <code>temp_eta.docs.js</code>).</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block exists in the runtime file but should not be used as a
source for generated API documentation (see <code>temp_eta.docs.js</code>).</p>

<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (should be &quot;temp_eta&quot;)</p> |
| data | <code>Object</code> | <p>plugin message payload</p> |
| data.type | <code>string</code> | <p>message type (e.g. 'history_reset','settings_reset','heater_update')</p> |
| [data.heater] | <code>string</code> | <p>heater id when applicable (e.g. 'tool0','bed')</p> |
| [data.eta] | <code>number</code> | <p>ETA in seconds when provided</p> |
| [data.eta_kind] | <code>string</code> | <p>kind of ETA ('linear','exponential',...)</p> |
| [data.cooldown_target] | <code>number</code> \| <code>null</code> |  |
| [data.actual] | <code>number</code> \| <code>null</code> |  |
| [data.target] | <code>number</code> \| <code>null</code> |  |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Determine whether an ETA value should be considered visible.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if ETA should be shown to the user</p>

| Param | Type | Description |
| --- | --- | --- |
| eta | <code>number</code> \| <code>null</code> \| <code>undefined</code> | <p>ETA in seconds (may be null/undefined)</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Return the localized idle text for a heater (e.g. 'Idle' or 'Cooling').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized idle text</p>

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (should be &quot;temp_eta&quot;)</p> |
| data | <code>Object</code> | <p>plugin message payload</p> |
| data.type | <code>string</code> | <p>message type (e.g. 'history_reset','settings_reset','heater_update')</p> |
| [data.heater] | <code>string</code> | <p>heater id when applicable (e.g. 'tool0','bed')</p> |
| [data.eta] | <code>number</code> | <p>ETA in seconds when provided</p> |
| [data.eta_kind] | <code>string</code> | <p>kind of ETA ('linear','exponential',...)</p> |
| [data.cooldown_target] | <code>number</code> \| <code>null</code> |  |
| [data.actual] | <code>number</code> \| <code>null</code> |  |
| [data.target] | <code>number</code> \| <code>null</code> |  |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Determine whether an ETA value should be considered visible.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if ETA should be shown to the user</p>

| Param | Type | Description |
| --- | --- | --- |
| eta | <code>number</code> \| <code>null</code> \| <code>undefined</code> | <p>ETA in seconds (may be null/undefined)</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Return the localized idle text for a heater (e.g. 'Idle' or 'Cooling').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized idle text</p>

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

<a name="TempETAViewModel"></a>

## TempETAViewModel
**Kind**: global class

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.onDataUpdaterPluginMessage(plugin, data)](#TempETAViewModel+onDataUpdaterPluginMessage) ⇒ <code>void</code>
    * [.isETAVisible(eta)](#TempETAViewModel+isETAVisible) ⇒ <code>boolean</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>
    * [.getHeaterIdleText(heater)](#TempETAViewModel+getHeaterIdleText) ⇒ <code>string</code>
    * [.getHeaterLabel(heaterName)](#TempETAViewModel+getHeaterLabel) ⇒ <code>string</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block exists in the runtime file but should not be used as a
source for generated API documentation (see <code>temp_eta.docs.js</code>).</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block exists in the runtime file but should not be used as a
source for generated API documentation (see <code>temp_eta.docs.js</code>).</p>

<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (should be &quot;temp_eta&quot;)</p> |
| data | <code>Object</code> | <p>plugin message payload</p> |
| data.type | <code>string</code> | <p>message type (e.g. 'history_reset','settings_reset','heater_update')</p> |
| [data.heater] | <code>string</code> | <p>heater id when applicable (e.g. 'tool0','bed')</p> |
| [data.eta] | <code>number</code> | <p>ETA in seconds when provided</p> |
| [data.eta_kind] | <code>string</code> | <p>kind of ETA ('linear','exponential',...)</p> |
| [data.cooldown_target] | <code>number</code> \| <code>null</code> |  |
| [data.actual] | <code>number</code> \| <code>null</code> |  |
| [data.target] | <code>number</code> \| <code>null</code> |  |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Determine whether an ETA value should be considered visible.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if ETA should be shown to the user</p>

| Param | Type | Description |
| --- | --- | --- |
| eta | <code>number</code> \| <code>null</code> \| <code>undefined</code> | <p>ETA in seconds (may be null/undefined)</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Return the localized idle text for a heater (e.g. 'Idle' or 'Cooling').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized idle text</p>

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

<a name="TempETAViewModel+onDataUpdaterPluginMessage"></a>

### tempETAViewModel.onDataUpdaterPluginMessage(plugin, data) ⇒ <code>void</code>
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)

| Param | Type | Description |
| --- | --- | --- |
| plugin | <code>string</code> | <p>plugin identifier (should be &quot;temp_eta&quot;)</p> |
| data | <code>Object</code> | <p>plugin message payload</p> |
| data.type | <code>string</code> | <p>message type (e.g. 'history_reset','settings_reset','heater_update')</p> |
| [data.heater] | <code>string</code> | <p>heater id when applicable (e.g. 'tool0','bed')</p> |
| [data.eta] | <code>number</code> | <p>ETA in seconds when provided</p> |
| [data.eta_kind] | <code>string</code> | <p>kind of ETA ('linear','exponential',...)</p> |
| [data.cooldown_target] | <code>number</code> \| <code>null</code> |  |
| [data.actual] | <code>number</code> \| <code>null</code> |  |
| [data.target] | <code>number</code> \| <code>null</code> |  |

<a name="TempETAViewModel+isETAVisible"></a>

### tempETAViewModel.isETAVisible(eta) ⇒ <code>boolean</code>
<p>Determine whether an ETA value should be considered visible.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>boolean</code> - <p>true if ETA should be shown to the user</p>

| Param | Type | Description |
| --- | --- | --- |
| eta | <code>number</code> \| <code>null</code> \| <code>undefined</code> | <p>ETA in seconds (may be null/undefined)</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

<a name="TempETAViewModel+getHeaterIdleText"></a>

### tempETAViewModel.getHeaterIdleText(heater) ⇒ <code>string</code>
<p>Return the localized idle text for a heater (e.g. 'Idle' or 'Cooling').</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized idle text</p>

| Param | Type | Description |
| --- | --- | --- |
| heater | [<code>Heater</code>](#Heater) | <p>heater object</p> |

<a name="TempETAViewModel+getHeaterLabel"></a>

### tempETAViewModel.getHeaterLabel(heaterName) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: instance method of [<code>TempETAViewModel</code>](#TempETAViewModel)
**Returns**: <code>string</code> - <p>localized label</p>

| Param | Type | Description |
| --- | --- | --- |
| heaterName | <code>string</code> | <p>heater identifier (e.g. 'tool0','bed')</p> |

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
