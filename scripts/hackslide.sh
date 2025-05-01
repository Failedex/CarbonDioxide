#!/bin/bash

PWD="$HOME/.config/eww/carbondioxide/"

WINDOW="$1"
CTRL="reveal$1"

STAT="$(eww -c $PWD get $CTRL)"
if [[ $STAT == "true" || $2 == "close" ]]; then
    $PWD/scripts/ricon.py 0 &
    eww -c $PWD update $CTRL=false
    sleep 0.5
    STAT="$(eww -c $PWD get $CTRL)"
    OPEN="$(eww -c $PWD active-windows | grep $WINDOW)"
    if [[ $STAT == "false" && $OPEN ]]; then 
        eww -c $PWD close $WINDOW
    fi
else
    $PWD/scripts/ricon.py 100 &
    eww -c $PWD open $WINDOW
    eww -c $PWD update $CTRL=true
fi

