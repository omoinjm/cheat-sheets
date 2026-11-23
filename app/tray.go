//go:build windows || linux

package main

import (
	_ "embed"
	"runtime"

	"fyne.io/systray"
	wruntime "github.com/wailsapp/wails/v2/pkg/runtime"
)

//go:embed build/tray.png
var trayPNG []byte

//go:embed build/windows/icon.ico
var trayICO []byte

// startTray shows the tray icon. The window then hides to the tray on close
// instead of quitting (main sets HideWindowOnClose when trayAvailable).
func (a *App) startTray() {
	go func() {
		// Windows delivers the tray window's messages only to the thread that
		// created it, so creation and the message loop share this one.
		runtime.LockOSThread()
		systray.Run(a.onTrayReady, nil)
	}()
}

func (a *App) stopTray() { systray.Quit() }

func (a *App) onTrayReady() {
	if runtime.GOOS == "windows" {
		systray.SetIcon(trayICO)
	} else {
		systray.SetIcon(trayPNG)
	}
	systray.SetTitle("Cheat Sheets")
	systray.SetTooltip("Cheat Sheets")
	systray.SetOnTapped(a.showWindow) // left click opens; right click shows the menu

	open := systray.AddMenuItem("Open Cheat Sheets", "Show the window")
	systray.AddSeparator()
	quit := systray.AddMenuItem("Quit", "Close Cheat Sheets")

	for {
		select {
		case <-open.ClickedCh:
			a.showWindow()
		case <-quit.ClickedCh:
			wruntime.Quit(a.ctx)
			return
		}
	}
}

func (a *App) showWindow() {
	wruntime.WindowShow(a.ctx)
	wruntime.WindowUnminimise(a.ctx)
	hideTaskbarButton()
}
