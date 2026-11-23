//go:build linux

package main

import "github.com/godbus/dbus/v5"

// trayAvailable reports whether the desktop shows StatusNotifierItem icons
// (KDE, most others; GNOME only with the AppIndicator extension). Without a
// tray, hiding the window on close would leave no way back to it.
func trayAvailable() bool {
	conn, err := dbus.SessionBus()
	if err != nil {
		return false
	}
	var has bool
	err = conn.BusObject().Call("org.freedesktop.DBus.NameHasOwner", 0, "org.kde.StatusNotifierWatcher").Store(&has)
	return err == nil && has
}

// Linux: the window keeps its taskbar entry while open (hiding it needs GTK
// access Wails doesn't expose); closing it still hides it to the tray.
const windowClass = ""

func hideTaskbarButton() {}
