/*
    KWin - the KDE window manager
    This file is part of the KDE project.

    SPDX-FileCopyrightText: 2012 Martin Gräßlin <mgraesslin@kde.org>

    SPDX-License-Identifier: GPL-2.0-or-later
*/

var currentDPI = "800"

var whitelist = readConfig("Whitelist", "inoaaionoannoa").toString().toLowerCase().split(",");
for (i = 0; i < whitelist.length; ++i)
    whitelist[i] = whitelist[i].trim();

var greylist = readConfig("Greylist", "ineaiaiaaenaoa").toString().toLowerCase().split(",");
for (i = 0; i < greylist.length; ++i)
    greylist[i] = greylist[i].trim();

function setup(window) {
    if (window) {
        if (whitelist.indexOf(window.resourceClass.toString().trim().toLowerCase()) > -1) {
            print("Is whitelist");
            if (currentDPI != "1600") {
                callHIDService("2",window.resourceClass.toString().trim().toLowerCase());
                currentDPI = "1600"
            }
        }
        else if (greylist.indexOf(window.resourceClass.toString().trim().toLowerCase()) > -1) {
            print("Is greylist");
            if (currentDPI != "400") {
                callHIDService("0",window.resourceClass.toString().trim().toLowerCase());
                currentDPI = "400"
            }
        }
    }
}

function remove(window) {
    // print("removed window" + " " + window);
    if (window) {
        if (whitelist.indexOf(window.resourceClass.toString().trim().toLowerCase()) > -1) {
            print("removed whitelist");
            callHIDService("1",window.resourceClass.toString().trim().toLowerCase());
        }
        else if (greylist.indexOf(window.resourceClass.toString().trim().toLowerCase()) > -1) {
            print("removed greylist");
            callHIDService("1",window.resourceClass.toString().trim().toLowerCase());
        }
    }
}


function callHIDService(value, window) {
    callDBus(
        "org.mkt.DPIExecutor",          // Service name from our Python helper
        "/org/mkt/DPIExecutor",         // Object path
        "org.mkt.DPIExecutor",          // Interface name
        "Execute",                          // Method name
        [ value, window ]                   // The parameter ("1" or "0")
    );
    print("Called DPI Executor with value: " + value + " " + window);
}

// workspace.windowAdded.connect(setup);
workspace.windowActivated.connect(setup);
workspace.windowRemoved.connect(remove);
// workspace.windowList().forEach(setup);
