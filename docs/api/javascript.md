## Classes

<dl>
<dt><a href="#PluginMessage">PluginMessage</a> : <code>Object</code></dt>
<dd><p>TempETAViewModel</p></dd>
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
should accept a <code>history</code> array of [HeaterHistoryEntry](HeaterHistoryEntry) and a numeric <code>target</code>.</p></dd>
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
should accept a <code>history</code> array of [HeaterHistoryEntry](HeaterHistoryEntry) and a numeric <code>target</code>.</p></dd>
</dl>

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
| [_history] | <code>Array.&lt;HeaterHistoryEntry&gt;</code> | <p>internal history array of samples</p> |
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
| [_history] | <code>Array.&lt;HeaterHistoryEntry&gt;</code> | <p>internal history array of samples</p> |
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
should accept a <code>history</code> array of [HeaterHistoryEntry](HeaterHistoryEntry) and a numeric <code>target</code>.</p>

**Kind**: global function  
**Returns**: <code>number</code> - <p>Seconds to reach target, or null if unavailable</p>  

| Param | Type | Description |
| --- | --- | --- |
| history | <code>Array.&lt;HeaterHistoryEntry&gt;</code> | <p>Array of recent samples</p> |
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
should accept a <code>history</code> array of [HeaterHistoryEntry](HeaterHistoryEntry) and a numeric <code>target</code>.</p>

**Kind**: global function  
**Returns**: <code>number</code> - <p>Seconds to reach target, or null if unavailable</p>  

| Param | Type | Description |
| --- | --- | --- |
| history | <code>Array.&lt;HeaterHistoryEntry&gt;</code> | <p>Array of recent samples</p> |
| target | <code>number</code> | <p>Target temperature in Celsius</p> |

