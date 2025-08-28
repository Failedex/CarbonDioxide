# Carbon Dioxide

The totally unnecessary sequel to Carbon Monoxide!

> [!NOTE]
> Despite popular beliefs, Carbon Dioxide is a niri rice, not a swayfx rice.

## What's in this config?
- An eww config of a single bar.
- A `bin` dir of scripts used to interact with the bar
- An example `niri` config that uses the config 

## Quirks
- The config is centered around a single bar! The bar includes an app launcher, notifications, timer, media player, volume and brightness osd, and can transform into a dashboard with more features.
- This may be the first ever eww config to utilize `-gtk-icon-transform`, it was mainly used for adding transitions to icon rotation.
- Custom animations were said to be impossible in gtk due to its limitations on revealers. This is true. However, the config bypasses this restriction by using css transitions instead.

A copius amount of tricks and ideas went into this config, I hope you have fun looking through it.

## Dependencies
- playerctl
- python i3ipc, dbus, gobject, Pillow
- pamixer
- brightnessctl
- nmcli
- bluetoothctl
- jq

## Installation

> [!WARNING]
> These dotfiles are untested and may not work on other devices. 
> It's safer to use this as a reference.

1. Clone the repo under `~/.config/eww/carbondioxide`
```
mkdir -p ~/.config/eww
git clone https://github.com/Failedex/CarbonDioxide ~/.config/eww/carbondioxide
```
2. Refer to the `niri` directory for an example config (it is my config). Alternatively, look at the `bin` directory for all the scripts you may want to use.

