#!/usr/bin/env python3
import time
import sys
from dbus.mainloop.glib import DBusGMainLoop
import dbus 
import dbus.service
from gi.repository import GLib
from threading import Thread

FPS = 30
DX = lambda t: 1 - (1-t)*(1-t)
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

            if lid != self.anim_id: 
                return
            
            self.rotate = (self.target-f) * dx + f
            print(self.rotate, flush = True)

            if t >= 1:
                return

            time.sleep(max(1/FPS-(fstart-time.time()), 0))
        self.rotate = self.target
        print(self.rotate, flush = True)

    @dbus.service.method("com.Failed.RIcon", in_signature="i", out_signature="")
    def Set(self, r): 
        self.target = r
        self.anim_id += 1
        thd = Thread(target=self.update)
        thd.start()

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

        if a.isdigit():
            bus = dbus.SessionBus()
            remote = bus.get_object("com.Failed.RIcon", "/com/Failed/RIcon")
            remote.Set(int(a))
        else: 
            bus = dbus.SessionBus()
            remote = bus.get_object("com.Failed.RIcon", "/com/Failed/RIcon")
            remote.Set(100 + (len(a) - 1)*5)
