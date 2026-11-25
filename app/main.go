// sheets-desk is an always-on-top corner overlay that watches your terminal
// and suggests matching cheat sheets from sheets.njmtech.co.za.
//
// A shell hook writes your current command line to a file; the overlay polls
// it and shows the best-matching cheat sheets. The window is frameless, floats
// above every other app, and docks to the top-left corner. It also lives in
// the system tray (close hides it; the tray icon or a second launch — e.g. an
// OS hotkey — brings it back via the single-instance lock).
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
		Width:            380,
		Height:           500,
		MinWidth:         300,
		MinHeight:        160,
		MaxWidth:         1400,
		MaxHeight:        1200,
		Frameless:        true,
		AlwaysOnTop:      true,
		DisableResize:    false,
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
