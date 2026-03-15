#!/bin/bash

# Get all device sysnames
devices=$(qdbus org.kde.KWin /org/kde/KWin/InputDevice org.kde.KWin.InputDeviceManager.devicesSysNames)

for dev in $devices; do
    path="/org/kde/KWin/InputDevice/$dev"

    name=$(qdbus org.kde.KWin $path \
        org.freedesktop.DBus.Properties.Get \
        org.kde.KWin.InputDevice \
        name 2>/dev/null)

    if [[ "$name" == *"keyd virtual pointer"* ]]; then
        echo "Found keyd device at $path"
        qdbus org.kde.KWin $path org.kde.KWin.InputDevice.pointerAcceleration "0.5"
        exit 0
    fi
done

echo "Keyd virtual pointer not found"
exit 1
