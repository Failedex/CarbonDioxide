#!/bin/bash

PWD="$HOME/.config/eww/carbondioxide"

STAT="$(eww -c $PWD get revealsearch)"
if [[ $STAT == "true" || $1 == "close" ]]; then
    # $PWD/scripts/ricon.py 0 &
    eww -c $PWD update revealsearch=false ricon=0
    eww -c $PWD close launcher
    $PWD/scripts/apps.py &
else 
    eww -c $PWD open launcher
    eww -c $PWD update revealbar=1 ricon=360
    # $PWD/scripts/ricon.py 100 &
    eww -c $PWD update revealsearch=true
fi
