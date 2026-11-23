package main

import (
	"context"
	"errors"
	"strings"

	"github.com/wailsapp/wails/v2/pkg/options"
	wruntime "github.com/wailsapp/wails/v2/pkg/runtime"
)

// App holds the window context and tray state.
type App struct {
	ctx  context.Context
	tray bool // icon in the system tray; the window hides on close
}

func newApp() *App { return &App{} }

func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
	if a.tray {
		a.startTray()
	}
}

func (a *App) shutdown(context.Context) {
	if a.tray {
		a.stopTray()
	}
}

// domReady: the window is up; a tray app has no taskbar button.
func (a *App) domReady(context.Context) {
	if a.tray {
		hideTaskbarButton()
	}
}

// onSecondInstance fires when the binary is launched again (e.g. by a global
// keyboard shortcut) while one copy is already running: bring the window up.
func (a *App) onSecondInstance(options.SecondInstanceData) {
	wruntime.WindowUnminimise(a.ctx)
	wruntime.Show(a.ctx)
	if a.tray {
		hideTaskbarButton()
	}
}

// OpenURL opens an http(s) link in the system browser. Exposed to JS as
// window.go.main.App.OpenURL; harmless if unused.
func (a *App) OpenURL(u string) error {
	if !strings.HasPrefix(u, "https://") && !strings.HasPrefix(u, "http://") {
		return errors.New("only web links can be opened")
	}
	wruntime.BrowserOpenURL(a.ctx, u)
	return nil
}
