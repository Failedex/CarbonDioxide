#! /bin/bash

# Taken from Tail-R. Thanks man love your stuff.
# Certain changes were made

ewwPath=$(pwd)

get_device_name() {
    if [ "$(get_con_status)" == "connected" ]; then
        knownDeviceNumber=$(bluetoothctl devices | awk '{print $2}')

        for deviceNumber in $knownDeviceNumber; do
            if [ "$(bluetoothctl info $deviceNumber | grep Connected: | awk '{print $2}')" == "yes" ]; then
                echo $(bluetoothctl info $deviceNumber | grep Name: | awk '{for (i = 2; i <= NF; i++) {printf "%s ", $i}; printf "\n"}') 
                return
            fi
        done
    fi
        
    echo "--"
}

get_con_status() {
    knownDeviceNumber=$(bluetoothctl devices | awk '{print $2}')

    for deviceNumber in $knownDeviceNumber; do
        conStatus=$(bluetoothctl info $deviceNumber | grep Connected: | awk '{print $2}')
        if [ "$conStatus" == "yes" ]; then
            echo "connected"
            return
        fi
    done

    echo "disabled"
}

toggle() {
    if [ "$(get_con_status)" == "connected" ]; then
        bluetoothctl disconnect
    else
        knownDeviceNumber=$(bluetoothctl devices | awk '{print $2}')
        
        for deviceNumber in $knownDeviceNumber; do
            bluetoothctl connect $deviceNumber 
        done    
    fi  
}

# Modified to return json array
update_eww_json() {
    macs=$(bluetoothctl devices | awk '/Device/ {print $2}')

    # Create json array
    json_array="["
    first=1

    for mac in $macs; do 
        info=$(bluetoothctl info "$mac")

        paired=$(echo "$info" | awk -F': ' '/Paired/ {print $2}')

        # Only return paired 
        # if [[ "$paired" != "yes" ]]; then 
        #     continue
        # fi

        name=$(echo "$info" | awk -F': ' '/Name/ {print $2}')
        connected=$(echo "$info" | awk -F': ' '/Connected/ {print $2}')
        trusted=$(echo "$info" | awk -F': ' '/Trusted/ {print $2}')
        name_escaped=$(echo "$name" | sed 's/"/\\"/g')

        if [ $first -eq 0 ]; then 
            json_array+=','
        else
            first=0
        fi

        json_array+=$(cat <<EOF
{
  "mac": "$mac",
  "name": "$name_escaped",
  "paired": "$paired",
  "connected": "$connected",
  "trusted": "$trusted"
}
EOF
)
    done

    json_array+="]"
    eww -c $ewwPath update bluetoothjson="$json_array"
}

# Main
if [ "$1" == "--con_status" ]; then
    get_con_status
elif [ "$1" == "--devname" ]; then
    get_device_name
elif [ "$1" == "--toggle" ]; then
    toggle
elif [ "$1" == "--update_eww_json" ]; then
    update_eww_json
fi
