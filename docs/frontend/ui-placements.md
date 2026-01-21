# UI Placements

This page describes where and how OctoPrint-TempETA integrates into the OctoPrint user interface.

## Overview

The plugin adds ETA displays in multiple locations:

1. **Temperature Graph** - Inline ETA display
2. **Sidebar Widget** - Compact ETA overview
3. **Settings Page** - Plugin configuration

## Temperature Graph Integration

### Location

The ETA is displayed directly in the temperature graph area, next to each heater's temperature reading.

### Display Format

```
Tool 0: 150.0°C / 200.0°C ⏱ 01:30
Bed: 60.0°C / 80.0°C ⏱ 00:45
```

### Template

Located in: `octoprint_temp_eta/templates/temp_eta_tab.jinja2`

```html
<div
  class="temp-eta-graph-display"
  data-bind="visible: settings.plugins.temp_eta.show_in_graph()"
>
  <!-- ko foreach: heaters -->
  <div class="heater-eta" data-bind="visible: hasETA()">
    <span class="heater-name" data-bind="text: name"></span>:
    <span class="eta-value" data-bind="text: formattedETA()"></span>
    <span class="eta-icon">⏱</span>
  </div>
  <!-- /ko -->
</div>
```

### Styling

Styled via LESS: `octoprint_temp_eta/static/less/temp_eta.less`

```less
.temp-eta-graph-display {
  margin-top: 5px;
  font-size: 0.9em;

  .heater-eta {
    display: inline-block;
    margin-right: 15px;

    .eta-value {
      font-weight: bold;
      color: @brand-primary;
    }

    .eta-icon {
      margin-left: 3px;
    }
  }
}
```

Compile LESS to CSS:

```bash
lessc octoprint_temp_eta/static/less/temp_eta.less > octoprint_temp_eta/static/css/temp_eta.css
```

## Sidebar Widget

### Location

Right sidebar, temperature section

### Display Format

```
╔════════════════════╗
║ Temperature ETA    ║
╠════════════════════╣
║ 🔥 Tool 0: 01:30  ║
║ 🛏️  Bed:   00:45  ║
╚════════════════════╝
```

### Template

Located in: `octoprint_temp_eta/templates/temp_eta_sidebar.jinja2`

```html
<div class="temp-eta-sidebar">
  <div data-bind="visible: settings.plugins.temp_eta.show_in_sidebar()">
    <h4>Temperature ETA</h4>
    <table class="table table-condensed">
      <!-- ko foreach: heaters -->
      <tr data-bind="visible: hasETA()">
        <td>
          <i class="fa" data-bind="css: icon"></i>
          <span data-bind="text: name"></span>
        </td>
        <td class="text-right">
          <span data-bind="text: formattedETA()"></span>
        </td>
      </tr>
      <!-- /ko -->
    </table>
  </div>
</div>
```

### Knockout Bindings

```javascript
self.heaters = ko.observableArray([
  {
    name: ko.observable("Tool 0"),
    icon: ko.observable("fa-fire"),
    eta: ko.observable(90),
    hasETA: ko.computed(function () {
      return this.eta() !== null;
    }, this),
    formattedETA: ko.computed(function () {
      return self.formatETA(this.eta());
    }, this),
  },
]);
```

## Settings Page

### Location

OctoPrint Settings → Plugins → Temperature ETA

### Template

Located in: `octoprint_temp_eta/templates/temp_eta_settings.jinja2`

```html
<form class="form-horizontal">
  <h3>{{ _('General Settings') }}</h3>

  <div class="control-group">
    <label class="control-label">{{ _('Enable Plugin') }}</label>
    <div class="controls">
      <input
        type="checkbox"
        data-bind="checked: settings.plugins.temp_eta.enabled"
      />
    </div>
  </div>

  <div class="control-group">
    <label class="control-label">{{ _('Algorithm') }}</label>
    <div class="controls">
      <select data-bind="value: settings.plugins.temp_eta.algorithm">
        <option value="linear">{{ _('Linear') }}</option>
        <option value="exponential">{{ _('Exponential') }}</option>
      </select>
    </div>
  </div>

  <!-- More settings... -->
</form>
```

### Settings Sections

1. **General**: Enable/disable, algorithm selection
2. **Heating ETA**: Heating-specific settings
3. **Cool-down ETA**: Cooling-specific settings
4. **Display**: UI customization
5. **MQTT**: External integration
6. **Advanced**: Expert settings

## Custom Bindings

### ETA Formatter

```javascript
ko.bindingHandlers.formattedETA = {
  update: function (element, valueAccessor) {
    var seconds = ko.unwrap(valueAccessor());
    var formatted = self.formatETA(seconds);
    $(element).text(formatted);
  },
};
```

Usage:

```html
<span data-bind="formattedETA: heaters['tool0'].eta"></span>
```

### Temperature Progress Bar

```javascript
ko.bindingHandlers.tempProgress = {
  update: function (element, valueAccessor) {
    var data = ko.unwrap(valueAccessor());
    var percent = (data.current / data.target) * 100;
    $(element).css("width", percent + "%");
  },
};
```

Usage:

```html
<div class="progress">
  <div
    class="progress-bar"
    data-bind="tempProgress: {current: temp(), target: target()}"
  ></div>
</div>
```

## Notification System

### Toast Notifications

Display temporary notifications:

```javascript
self.showToast = function (type, title, message) {
  new PNotify({
    title: title,
    text: message,
    type: type, // 'success', 'info', 'warning', 'error'
    hide: true,
    delay: 5000,
    addclass: "temp-eta-toast",
  });
};
```

Usage:

```javascript
// Heating complete
self.showToast(
  "success",
  "Heating Complete",
  "Tool 0 has reached target temperature",
);

// Error
self.showToast("error", "ETA Error", "Failed to calculate ETA");
```

### Sound Notifications

Play sound on temperature reached:

```javascript
self.playSound = function (soundFile) {
  if (!self.settings.sound_enabled()) return;

  var audio = new Audio("/plugin/temp_eta/static/sounds/" + soundFile);
  audio.play();
};
```

## Responsive Design

The UI adapts to different screen sizes:

```less
// Desktop
@media (min-width: 768px) {
  .temp-eta-sidebar {
    display: block;
  }
}

// Mobile
@media (max-width: 767px) {
  .temp-eta-sidebar {
    display: none; // Hide on small screens
  }

  .temp-eta-graph-display {
    font-size: 0.8em; // Smaller text
  }
}
```

## Accessibility

### ARIA Labels

```html
<div
  class="heater-eta"
  role="status"
  aria-live="polite"
  aria-label="Temperature ETA"
>
  <span data-bind="text: formattedETA()"></span>
</div>
```

### Keyboard Navigation

Settings page supports keyboard navigation:

```javascript
self.onKeyPress = function (data, event) {
  if (event.keyCode === 13) {
    // Enter
    self.saveSettings();
    return false;
  }
  return true;
};
```

## Theme Support

The plugin respects OctoPrint's theme:

```less
// Use OctoPrint variables
.temp-eta-value {
  color: @text-color;
  background: @background-color;
  border: 1px solid @border-color;
}

// Dark theme support
.dark-theme {
  .temp-eta-value {
    color: @dark-text-color;
    background: @dark-background-color;
  }
}
```

## Icon Usage

Font Awesome icons:

```html
<!-- Heating -->
<i class="fa fa-arrow-up text-danger"></i>

<!-- Cooling -->
<i class="fa fa-arrow-down text-info"></i>

<!-- Target reached -->
<i class="fa fa-check text-success"></i>

<!-- Clock/Timer -->
<i class="fa fa-clock-o"></i>
```

## Customization

Users can customize via CSS overrides:

```css
/* In OctoPrint's custom CSS */
#temp-eta-sidebar {
  background-color: #f0f0f0;
  border-radius: 5px;
  padding: 10px;
}

.temp-eta-graph-display .eta-value {
  color: #ff6600;
  font-weight: bold;
}
```

## Plugin Dependencies

UI requires:

- jQuery
- Knockout.js
- Bootstrap (OctoPrint's version)
- Font Awesome
- PNotify (for notifications)

All provided by OctoPrint core.

## Testing UI

### Browser Console

```javascript
// Get view model
var vm = window.OCTOPRINT_VIEWMODELS.find((v) => v.name === "tempEtaViewModel");

// Simulate ETA update
vm.updateETA("tool0", {
  current: 150,
  target: 200,
  eta_seconds: 90,
  rate: 0.5,
});

// Check settings
console.log(vm.settings.plugins.temp_eta.enabled());
```

### Chrome DevTools

1. Open DevTools (F12)
2. Go to Elements tab
3. Find `.temp-eta-sidebar`
4. Modify attributes/styles live

## Next Steps

- [Internationalization](i18n.md) - Translation system
- [JavaScript API](../api/javascript.md) - Frontend API reference
- [Settings Reference](../architecture/settings.md) - Configuration options
