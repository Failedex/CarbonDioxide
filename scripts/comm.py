#!/usr/bin/env python3

import subprocess
import json
import socket
import os 
from iconfetch import fetch

eww_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

class NiriComm: 
    def __init__(self, client): 
        self.client = client
        self.fwsid = 0
        self.fwinid = 0
        self.windows = {}
        self.workspaces = {}

    def setup(self):
        client.sendall('"Windows"\n'.encode())
        data = client.recv(1024)
        data = json.loads(data.decode())["Ok"]["Windows"]
        
        for win in data:
            if win["is_focused"]:
                self.fwinid = win["id"]
            self.windows[win['id']] = win

        client.sendall('"Workspaces"\n'.encode())
        data = client.recv(1024)
        data = json.loads(data.decode())["Ok"]["Workspaces"]
        
        for ws in data:
            if ws["is_focused"]:
                self.fwsid = ws["id"]
            self.workspaces[ws['id']] = ws

        self.update_workspace()
        self.update_window()

        client.sendall('"EventStream"\n'.encode())
        while True: 
            data = client.recv(1024)
            if not data: 
                break
            
            data = data.decode()
            for line in data.split('\n'):
                line = line.strip()
                if line == '':
                    continue
                try:
                    d = json.loads(line)
                except:
                    continue
                
                if "WindowFocusChanged" in d: 
                    fid = d["WindowFocusChanged"]["id"]
                    if self.fwinid in self.windows:
                        self.windows[self.fwinid]["is_focused"] = False
                    if fid in self.windows:
                        self.windows[fid]["is_focused"] = True
                    self.fwinid = fid
                    self.update_window()

                if "WindowOpenedOrChanged" in d:
                    window = d["WindowOpenedOrChanged"]["window"]
                    self.windows[window["id"]] = window
                    if window["is_focused"]:
                        if self.fwinid in self.windows:
                            self.windows[self.fwinid]["is_focused"] = False
                        self.fwinid = window["id"]
                        # This is usually called twice so when it sees it for a second time it toggles it to false lmao
                        self.windows[self.fwinid]["is_focused"] = True
                    self.update_window()

                if "WindowClosed" in d:
                    fid = d["WindowClosed"]["id"]
                    del self.windows[fid]
                    self.update_window()

                if "OverviewOpenedOrClosed" in d:
                    ow = d["OverviewOpenedOrClosed"]["is_open"]
                    self.update("overview", json.dumps(ow))

                if "WorkspaceActivated" in d:
                    fid = d["WorkspaceActivated"]["id"] 
                    self.workspaces[self.fwsid]["is_focused"] = False
                    self.workspaces[fid]["is_focused"] = True
                    self.fwsid = fid
                    self.update_workspace()

                if "WorkspacesChanged" in d: 
                    self.workspaces = {}
                    for ws in d["WorkspacesChanged"]["workspaces"]:
                        if ws["is_focused"]:
                            self.fwsid = ws["id"]
                        self.workspaces[ws['id']] = ws
                    self.update_workspace()

    def update_window(self): 
        wins = list(self.windows.values())
        wins.sort(key=lambda x: x["id"])
        idx = len(wins)/2
        fwin = "false"
        for i, win in enumerate(wins): 
            win["icon"] = fetch(win["app_id"].lower()) or fetch("unknown")
            if win["is_focused"]:
                idx = i
                fwin = "true"

        self.update("focusedwin", fwin)
        self.update("winidx", idx)
        self.update("windows", json.dumps(wins))

    def update_workspace(self):
        wss = list(self.workspaces.values())
        wss.sort(key=lambda x: x["id"])
        output = [[], []]
        translate = {"eDP-1": 0, "DP-1": 1}
        active_mon = 0
        for ws in wss:
            if ws["output"] not in translate:
                continue
            t = translate[ws["output"]]
            if ws["is_focused"]:
                active_mon = t
            output[t].append({"is_active": ws["is_focused"], "empty": ws["active_window_id"] == None})
        self.update("outidx", active_mon)

        for out in output:
            for i, ws in enumerate(out):
                if ws["is_active"]:
                    self.update("wsidx", i)
                    break
        self.update("workspace", json.dumps(output))

    def update(self, var, val): 
        subprocess.run(["eww", "-c", eww_dir, "update", f"{var}={val}"])

if __name__ == "__main__":
    sock = os.getenv("NIRI_SOCKET")
    assert type(sock) == str

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(sock)
        NiriComm(client).setup()
