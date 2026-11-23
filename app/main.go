// sheets-desk is a tiny tray-resident desktop window that shows the hosted
// cheat-sheets site (sheets.njmtech.co.za) in a native web view.
//
// It lives in the system tray: closing the window hides it; the tray icon (or
// a second launch) brings it back. Bind an OS keyboard shortcut to run the
// binary again — SingleInstanceLock catches the second launch and pops the
// existing window forward (OnSecondInstanceLaunch), so the shortcut toggles
// the window into view without ever starting a second copy.
package main

import (
	"embed"
	"io/fs"
	"log"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
	"github.com/wailsapp/wails/v2/pkg/options/linux"
	"github.com/wailsapp/wails/v2/pkg/options/mac"
	"github.com/wailsapp/wails/v2/pkg/options/windows"
)

// version is set at build time: -ldflags "-X main.version=v1.2.3"
var version = "dev"

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	dist, err := fs.Sub(assets, "frontend/dist")
	if err != nil {
		log.Fatal(err)
	}

	app := newApp()
	opts := &options.App{
		Title:            "Cheat Sheets",
		Width:            1200,
		Height:           820,
		MinWidth:         480,
		MinHeight:        400,
		AssetServer:      &assetserver.Options{Assets: dist},
		BackgroundColour: &options.RGBA{R: 15, G: 17, B: 21, A: 255},
		OnStartup:        app.startup,
		OnDomReady:       app.domReady,
		OnShutdown:       app.shutdown,
		Bind:             []any{app},
		Windows:          &windows.Options{WindowClassName: windowClass},
		Mac: &mac.Options{
			About: &mac.AboutInfo{Title: "Cheat Sheets", Message: "sheets.njmtech.co.za\n" + version},
		},
		Linux: &linux.Options{ProgramName: "sheets-desk"},
	}

	if trayAvailable() {
		// Live in the tray: closing the window hides it; the tray icon or a
		// second launch brings it back, "Quit" exits.
		opts.HideWindowOnClose = true
		app.tray = true
	}
	opts.SingleInstanceLock = &options.SingleInstanceLock{
		UniqueId:               "sheets-desk.main.9a7c1b",
		OnSecondInstanceLaunch: app.onSecondInstance,
	}

	if err := wails.Run(opts); err != nil {
		log.Fatal(err)
	}
}
