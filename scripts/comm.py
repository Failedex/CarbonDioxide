#!/usr/bin/env python3

import subprocess
import json
import os
from iconfetch import fetch

eww_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

proc = subprocess.Popen(["niri", "msg", "-j", "event-stream"], stdout=subprocess.PIPE, text=True)

def update(var, val): 
    subprocess.run(["eww", "-c", eww_dir, "update", f"{var}={val}"])

def active_mon():
    t = subprocess.getoutput("niri msg -j focused-output")
    translate = {"eDP-1": 0, "DP-1": 1}
    data = json.loads(t)
    update("outidx", translate.get(data["name"], 0))

def workspace(): 
    global idx
    t = subprocess.getoutput("niri msg -j workspaces")
    data = json.loads(t)
    # Dual monitor
    output = [[], []]
    data.sort(key=lambda x: x["id"])
    translate = {"eDP-1": 0, "DP-1": 1}
    for ws in data: 
        if ws["output"] not in translate: 
            continue
        t = translate[ws["output"]]
        output[t].append({"is_active": ws["is_active"], "empty": ws["active_window_id"] == None})

    active_mon()

    for out in output:
        for i, ws in enumerate(out):
            if ws["is_active"]: 
                if i != idx: 
                    idx = i
                    update("wsidx", idx)
                break
    update("workspace", json.dumps(output))

def window(): 
    t = subprocess.getoutput("niri msg -j windows")
    data = json.loads(t)
    data.sort(key=lambda x: x["id"])
    idx = len(data)/2
    fwin = "false"
    for i, win in enumerate(data): 
        win["icon"] = fetch(win["app_id"].lower()) or fetch("unknown")
        if win["is_focused"]:
            idx = i
            fwin = "true"

    update("focusedwin", fwin)
    update("winidx", idx)
    update("windows", json.dumps(data))

def overview():
    t = subprocess.getoutput("niri msg -j overview-state")
    data = json.loads(t)
    update("overview", 'true' if data["is_open"] else 'false')

if __name__ == "__main__":
    idx = 0
    workspace()
    window()
    overview()
    while True: 
        out = proc.stdout.readline().strip()
        data = json.loads(out)
        if "WorkspaceActivated" in list(data.keys())[0]: 
            workspace()
        if "WindowFocusChanged" in list(data.keys())[0]: 
            window()
        if "WindowOpenedOrChanged" in list(data.keys())[0]: 
            window()
        if "OverviewOpenedOrClosed" in list(data.keys())[0]:
            overview()

