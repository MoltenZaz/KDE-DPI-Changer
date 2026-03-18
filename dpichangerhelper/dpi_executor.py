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

import usb.core
import usb.util
import binascii

VENDOR_ID  = 0x5253
PRODUCT_ID = 0x1020
INTERFACE  = 2  # HID interface for config

DPI_400 = bytes.fromhex("12bffffffe6ffedffcbff9bff9ffe6ef5bfc006ffedffcbff9bff9ffe6ef5bffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
DPI_800 = bytes.fromhex("12bffefefd6ffedffcbff9bff9ffe6ef5bfc006ffedffcbff9bff9ffe6ef5bffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
DPI_1600 = bytes.fromhex("12bffdfdfd6ffedffcbff9bff9ffe6ef5bfc006ffedffcbff9bff9ffe6ef5bffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

def send_feature(dev, report_id, data):
    wValue = (3 << 8) | report_id  # Feature report
    dev.ctrl_transfer(
        0x21,        # Host-to-device | Class | Interface
        0x09,        # SET_REPORT
        wValue,
        INTERFACE,
        data,
        timeout=2000
    )

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev.is_kernel_driver_active(INTERFACE):
    dev.detach_kernel_driver(INTERFACE)

# print("Starting")

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
            # subprocess.run(["python3", "/home/mitchell/Documents/KWinScripts/dpichangerhelper/Mouse_DPI_400.py"])
            send_feature(dev, 0x12, DPI_400)
            subprocess.call(["/home/mitchell/Documents/KWinScripts/dpichangerhelper/set_speed_double.sh"])
        elif received == "2":
            # subprocess.run(["python3", "/home/mitchell/Documents/KWinScripts/dpichangerhelper/Mouse_DPI_1600.py"])
            send_feature(dev, 0x12, DPI_1600)
            subprocess.call(["/home/mitchell/Documents/KWinScripts/dpichangerhelper/set_speed_half.sh"])
        else:
            # subprocess.run(["python3", "/home/mitchell/Documents/KWinScripts/dpichangerhelper/Mouse_DPI_800.py"])
            send_feature(dev, 0x12, DPI_800)
            subprocess.call(["/home/mitchell/Documents/KWinScripts/dpichangerhelper/set_speed_normal.sh"])
            print("DPI set to 800.")
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
