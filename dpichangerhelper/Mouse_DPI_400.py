#!/usr/bin/env python3
import usb.core
import usb.util
import binascii

VENDOR_ID  = 0x5253
PRODUCT_ID = 0x1020
INTERFACE  = 2  # HID interface for config

DPI_800_1 = bytes.fromhex("12bffffffe6ffedffcbff9bff9ffe6ef5bfc006ffedffcbff9bff9ffe6ef5bffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
DPI_800_2 = bytes.fromhex("11fbffffffffffffffffffffffffffffffffffffff")
DPI_800_3 = bytes.fromhex("11fb55ffffffffffffffffffffffffffffffffffff")
DPI_800_4 = bytes.fromhex("1298ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
DPI_800_5 = bytes.fromhex("11fcffffffffffffffffffffffffffffffffffffff")

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

send_feature(dev, 0x11, DPI_800_1)
send_feature(dev, 0x11, DPI_800_2)
send_feature(dev, 0x11, DPI_800_3)
send_feature(dev, 0x11, DPI_800_4)
send_feature(dev, 0x11, DPI_800_5)

print("DPI set to 400.")
