#!/usr/bin/bash 

pipewire & 
wireplumber &
pipewire-pulse &

syncthing &
eww -c ~/.config/eww/carbondioxide open-many bar barslide &
swaybg -m fill -i ~/.config/niri/walls/flowerbw.png &

