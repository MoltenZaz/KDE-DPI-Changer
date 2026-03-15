#!/usr/bin/env python3
import subprocess
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
import time
import shutil
import os, signal
import glob
import struct

print("Starting")

SERVICE_NAME = "org.mkt.DPIExecutor"
OBJECT_PATH = "/org/mkt/DPIExecutor"
INTERFACE_NAME = "org.mkt.DPIExecutor"

class DPIExecutor(dbus.service.Object):
    def __init__(self, bus, object_path=OBJECT_PATH):
        super().__init__(bus, object_path)


    @dbus.service.method(INTERFACE_NAME, in_signature="s", out_signature="s")
    def Execute(self, value):
        print("helper start at", time.time())

        if isinstance(value, dbus.Array):
            if len(value) > 0:
                received = str(value[0]).strip()
                window = str(value[1]).strip()
            else:
                received = ""
                window = ""
        else:
            received = str(value).strip()
            window = str(value).strip()

        print("DPIExecutor received value: '{}'".format(received))
        print("DPIExecutor received window: '{}'".format(window))
        # Decide which output to use based on the passed string.
        # print(value)
        if received == "0":
            subprocess.run(["python3", "/home/mitchell/Documents/KWinScripts/dpichangerhelper/Mouse_DPI_400.py"])
            subprocess.call(["/home/mitchell/Documents/KWinScripts/dpichangerhelper/set_speed_double.sh"])
        elif received == "2":
            subprocess.run(["python3", "/home/mitchell/Documents/KWinScripts/dpichangerhelper/Mouse_DPI_1600.py"])
            subprocess.call(["/home/mitchell/Documents/KWinScripts/dpichangerhelper/set_speed_half.sh"])
        else:
            subprocess.run(["python3", "/home/mitchell/Documents/KWinScripts/dpichangerhelper/Mouse_DPI_800.py"])
            subprocess.call(["/home/mitchell/Documents/KWinScripts/dpichangerhelper/set_speed_normal.sh"])
        print(received)
        return received


if __name__ == "__main__":
    # Set up the DBus main loop and register the service.
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    name = dbus.service.BusName(SERVICE_NAME, bus)
    executor = DPIExecutor(bus)
    loop = GLib.MainLoop()
    loop.run()
