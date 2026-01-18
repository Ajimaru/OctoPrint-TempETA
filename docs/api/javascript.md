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

<a name="TempETAViewModel"></a>

## TempETAViewModel
**Kind**: global class  

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)

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

