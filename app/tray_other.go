//go:build !windows && !linux

package main

// macOS: Wails owns the main thread, which the tray library also needs, so the
// app keeps its Dock icon there for now.
func trayAvailable() bool { return false }
func (a *App) startTray()  {}
func (a *App) stopTray()   {}

const windowClass = ""

func hideTaskbarButton() {}
