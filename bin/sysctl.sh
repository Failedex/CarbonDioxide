#!/bin/bash

EWW_DIR="$HOME/.config/eww/carbondioxide"
COUNTER="/tmp/.osdind"

if [[ ! -f $COUNTER ]]; then
    touch $COUNTER
    echo '0' > $COUNTER
fi

check_eww () {
    if [[ ! $(eww -c $EWW_DIR ping) ]]; then 
        exit 0
    fi
}

update_eww_vol() {
    eww -c $EWW_DIR update volume=$(pamixer --get-volume) &
    eww -c $EWW_DIR update volumemute=$(pamixer --get-mute) &
}

update_eww_bri() {
    eww -c $EWW_DIR update brightness=$(brightnessctl -m | awk -F, '{print substr($4, 0, length($4)-1)}' | tr -d '%') &
}

popup() {
    eww -c $EWW_DIR update revealchangemode=$1
    count=$(cat $COUNTER)

    if [[ $count == 0 ]]; then 
        eww -c $EWW_DIR update revealosd=true
    fi

    count=$(($count + 1))
    echo $count > $COUNTER

    sleep 2 

    count=$(cat $COUNTER)
    count=$(($count - 1))
    echo $count > $COUNTER

    if [[ $count == 0 ]]; then 
        eww -c $EWW_DIR update revealosd=false
    fi
}

if [[ $1 == "incvol" ]]; then
    pamixer -i 5
    check_eww
    update_eww_vol
    popup "0"
elif [[ $1 == "decvol" ]]; then 
    pamixer -d 5
    check_eww
    update_eww_vol
    popup "0"
elif [[ $1 == "togvol" ]]; then 
    pamixer --toggle-mute
    check_eww
    update_eww_vol
    popup "0"
elif [[ $1 == "incbri" ]]; then 
    light -A 5
    check_eww
    update_eww_bri
    popup "1"
elif [[ $1 == "decbri" ]]; then 
    light -U 5
    check_eww
    update_eww_bri
    popup "1"
else 
    echo "???"
fi
