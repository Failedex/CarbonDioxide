#!/usr/bin/env python3
import time
import sys
from dbus.mainloop.glib import DBusGMainLoop
import dbus 
import dbus.service
from gi.repository import GLib
from threading import Thread
import subprocess
import json
import math

FPS = 30

# experimentation with functions lol
def ease_in_out_back(t): 
    c1 = 1.70158
    c2 = c1 * 1.525

    if t < 0.5: 
        return (math.pow(2*t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
    else:
        return (math.pow(2*t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1

    return 1+c3*math.pow(t-1, 3) + c1*math.pow(t-1, 2)

DX = ease_out_back
# DX = lambda t: 1 - (1-t)*(1-t)
DURATION = 1

class RIcon(dbus.service.Object):
    def __init__(self): 
        super().__init__(
            dbus.service.BusName("com.Failed.RIcon",
            bus=dbus.SessionBus()), 
            "/com/Failed/RIcon")
        self.rotate = 0
        self.target = 0
        self.anim_id = 0
        self.pctlspin = False
        self.mode = 0
        self.dr = 1

    def update(self): 
        f = self.rotate
        lid = self.anim_id
        start = time.time()
        frames = int(DURATION * FPS)
        for _ in range(frames): 
            fstart = time.time()
            t = (fstart - start) / DURATION
            dx = DX(t)
            if t >= 1: 
                dx = 1

            if lid != self.anim_id or self.mode != 0: 
                return
            
            self.rotate = (self.target-f) * dx + f
            print(self.rotate, flush = True)

            if t >= 1:
                return

            time.sleep(max(1/FPS-(fstart-time.time()), 0))
        self.rotate = self.target
        print(self.rotate, flush = True)

    def PctlSpin(self):
        proc = subprocess.Popen("./scripts/cava_pipe.sh", stdout=subprocess.PIPE, text=True)
        while self.mode == 1:
            out = proc.stdout.readline().strip()
            data = json.loads(out)
            self.rotate += data[1] * (3/100)
            self.rotate %= 100
            print(self.rotate, flush=True)
        proc.kill()

    def LinSpin(self): 
        while self.mode == 2:
            self.rotate += self.dr
            self.rotate %= 100
            print(self.rotate, flush=True)
            time.sleep(1/FPS)

    def SongSpin(self): 
        playing = [False]
        def checkplay(playing): 
            out = subprocess.getoutput("playerctl status").strip()
            proc = subprocess.Popen(["playerctl", "status", "-F"], stdout=subprocess.PIPE, text=True)
            playing[0] = out == "Playing"
            while self.mode == 3:
                out = proc.stdout.readline().strip()
                playing[0] = out == "Playing"

        Thread(target=checkplay, args=(playing,), daemon=True).start()
        while self.mode == 3: 
            if playing[0]:
                self.rotate += 0.2
                self.rotate %= 100
                print(self.rotate, flush=True)
            time.sleep(1/FPS)

    @dbus.service.method("com.Failed.RIcon", in_signature="i", out_signature="")
    def Set(self, r): 
        if self.mode != 0: 
            return
        self.target = r
        self.anim_id += 1
        thd = Thread(target=self.update)
        thd.start()

    @dbus.service.method("com.Failed.RIcon", in_signature="i", out_signature="")
    def SetMode(self, mode): 
        self.mode = mode
        if self.mode == 0:
            self.Set(0)
        elif self.mode == 1:
            thd = Thread(target=self.PctlSpin)
            thd.start()
        elif self.mode == 2: 
            thd = Thread(target=self.LinSpin)
            thd.start()
        elif self.mode == 3: 
            thd = Thread(target=self.SongSpin)
            thd.start()

    @dbus.service.method("com.Failed.RIcon", in_signature="i", out_signature="")
    def SetLinSpeed(self, r): 
        self.dr += r
        self.dr = min(max(self.dr, 0), 100)

if __name__ == "__main__": 
    if len(sys.argv) <= 1: 
        DBusGMainLoop(set_as_default=True)
        loop = GLib.MainLoop()
        RIcon()
        try: 
            loop.run()
        except KeyboardInterrupt: 
            exit(0)
    else:
        a = sys.argv[1]
        bus = dbus.SessionBus()
        remote = bus.get_object("com.Failed.RIcon", "/com/Failed/RIcon")
        if a.isdigit():
            remote.Set(int(a))
        elif a == 'mode': 
            b = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 0
            remote.SetMode(b)
        elif a == 'type': 
            b = sys.argv[2] if len(sys.argv) > 2 else ""
            remote.Set(100 + len(b)*5)
        elif a == 'inc': 
            b = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 0
            remote.SetLinSpeed(b)
        elif a == 'dec': 
            b = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 0
            remote.SetLinSpeed(-b)

