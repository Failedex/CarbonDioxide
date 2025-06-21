#!/bin/bash

# Taken from Tail-R

ewwPath=$(pwd)

get_con_status() {
    if [ "$(nmcli g | awk '{print $1}' | grep connected)" == "connected" ]; then
        echo "connected" 
    else
        echo "disconnected"
    fi
}

get_ssid() {
    ssid=$(nmcli device show | grep GENERAL.CONNECTION | grep -v -E "\slo$")
    echo $(echo $ssid | awk 'NR == 1 {print $2}')
}

get_inet4() {
    echo $(nmcli --pretty | grep inet4 | awk 'NR == 1 {print $2}')
}

toggle() {
    conName=$(nmcli con show | grep -v -E "^lo\s" | awk 'NR == 2 {print $1}')
    
    if [ "$(get_con_status)" == "connected" ]; then
        nmcli con down $conName  
    else
        nmcli con up $conName
    fi
}

# eeeehh lazy...
update_eww_json() {
    ssidList=$(nmcli -t -f SSID,SIGNAL,IN-USE dev wifi | awk -F: '
NF>=2 {
  ssid = $1
  signal = $2
  connected = ($3 == "*") ? "true" : "false"
  gsub(/"/, "\\\"", ssid)
  printf("{\"ssid\":\"%s\",\"signal\":%s,\"connected\":%s}\n", ssid, signal, connected)
}' | jq -s 'sort_by(.signal) | reverse') 

    eww -c $ewwPath update wifijson="$ssidList"
}

# Main
if [ "$1" == "--con_status" ]; then
    get_con_status
elif [ "$1" == "--ssid" ]; then
    get_ssid
elif [ "$1" == "--inet4" ]; then
    get_inet4
elif [ "$1" == "--toggle" ]; then
    toggle
elif [ "$1" == "--update_eww_json" ]; then
    update_eww_json
fi
