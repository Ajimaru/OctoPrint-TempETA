## Classes

<dl>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd></dd>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd><p>Knockout view model for the Temperature ETA plugin.</p></dd>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd></dd>
<dt><a href="#TempETAViewModel">TempETAViewModel</a></dt>
<dd><p>Knockout view model for the Temperature ETA plugin.</p></dd>
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
</dl>

<a name="TempETAViewModel"></a>

## TempETAViewModel
**Kind**: global class  

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel"></a>

## TempETAViewModel
<p>Knockout view model for the Temperature ETA plugin.</p>

**Kind**: global class  

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel"></a>

## TempETAViewModel
**Kind**: global class  

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel"></a>

## TempETAViewModel
<p>Knockout view model for the Temperature ETA plugin.</p>

**Kind**: global class  

* [TempETAViewModel](#TempETAViewModel)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [new TempETAViewModel()](#new_TempETAViewModel_new)
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>
    * [.onSettingsShown(dialog)](#TempETAViewModel.onSettingsShown)
    * [.onSettingsHidden()](#TempETAViewModel.onSettingsHidden)
    * [.onDataUpdaterPluginMessage(msg)](#TempETAViewModel.onDataUpdaterPluginMessage)
    * [.getHeaterLabel(heaterId)](#TempETAViewModel.getHeaterLabel) ⇒ <code>string</code>
    * [.isETAVisible(heater)](#TempETAViewModel.isETAVisible) ⇒ <code>boolean</code>
    * [.getProgressPercent(heater)](#TempETAViewModel.getProgressPercent) ⇒ <code>number</code>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>Knockout view model for the Temperature ETA plugin.
The runtime implementation lives in <code>temp_eta.js</code>; this file provides
non-invasive JSDoc typedefs and an overview for documentation generation.</p>

<a name="new_TempETAViewModel_new"></a>

### new TempETAViewModel()
<p>TempETA runtime JSDoc (small safe step).</p>
<p>This comment block documents the public class <code>TempETAViewModel</code> used by the
plugin. It is intentionally brief and only contains descriptive JSDoc so
adding it should not alter runtime behavior.</p>

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | [<code>PluginMessage</code>](#PluginMessage) | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | [<code>Heater</code>](#Heater) | 

<a name="TempETAViewModel.onSettingsShown"></a>

### TempETAViewModel.onSettingsShown(dialog)
<p>Called when the settings dialog is shown.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| dialog | <code>HTMLElement</code> | <p>The settings dialog element.</p> |

<a name="TempETAViewModel.onSettingsHidden"></a>

### TempETAViewModel.onSettingsHidden()
<p>Called when the settings dialog is hidden.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  
<a name="TempETAViewModel.onDataUpdaterPluginMessage"></a>

### TempETAViewModel.onDataUpdaterPluginMessage(msg)
<p>Handle incoming plugin messages delivered by OctoPrint's data updater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type | Description |
| --- | --- | --- |
| msg | <code>Object</code> | <p>The incoming plugin message payload.</p> |

<a name="TempETAViewModel.getHeaterLabel"></a>

### TempETAViewModel.getHeaterLabel(heaterId) ⇒ <code>string</code>
<p>Return a user-facing label for a heater id.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heaterId | <code>string</code> | 

<a name="TempETAViewModel.isETAVisible"></a>

### TempETAViewModel.isETAVisible(heater) ⇒ <code>boolean</code>
<p>Whether the ETA should be visible for a given heater.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

<a name="TempETAViewModel.getProgressPercent"></a>

### TempETAViewModel.getProgressPercent(heater) ⇒ <code>number</code>
<p>Compute a progress percentage (0-100) for the heater towards its target.</p>

**Kind**: static method of [<code>TempETAViewModel</code>](#TempETAViewModel)  

| Param | Type |
| --- | --- |
| heater | <code>Object</code> | 

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
| [_history] | <code>Array.&lt;Object&gt;</code> |  |
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
| [_history] | <code>Array.&lt;Object&gt;</code> |  |
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

