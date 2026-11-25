package main

import (
	"context"
	"errors"
	"os"
	"strings"
	"sync"

	"github.com/wailsapp/wails/v2/pkg/options"
	wruntime "github.com/wailsapp/wails/v2/pkg/runtime"
)

// App holds window context, tray state, the cheat-sheet index, and the last
// suggestions computed from the terminal.
type App struct {
	ctx  context.Context
	tray bool

	index     *Index
	watchStop chan struct{}

	lastMu sync.Mutex
	last   SuggestPayload
}

func newApp() *App {
	return &App{index: &Index{}, watchStop: make(chan struct{})}
}

func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
	if a.tray {
		a.startTray()
	}
	// Dock to the top-left corner and float above everything.
	wruntime.WindowSetPosition(ctx, 12, 12)
	wruntime.WindowSetAlwaysOnTop(ctx, true)

	// Make sure the directory the shell hook writes to exists.
	_ = os.MkdirAll(ctxDir(), 0o755)

	go a.loadIndex()
	a.startWatcher()
}

func (a *App) shutdown(context.Context) {
	close(a.watchStop)
	if a.tray {
		a.stopTray()
	}
}

func (a *App) domReady(context.Context) {
	if a.tray {
		hideTaskbarButton()
	}
}

// onSecondInstance fires when the binary is launched again (e.g. by the OS
// hotkey): bring the overlay back to the corner, on top.
func (a *App) onSecondInstance(options.SecondInstanceData) {
	wruntime.WindowShow(a.ctx)
	wruntime.WindowUnminimise(a.ctx)
	wruntime.WindowSetAlwaysOnTop(a.ctx, true)
	if a.tray {
		hideTaskbarButton()
	}
}

// OpenURL opens an http(s) link in the system browser.
func (a *App) OpenURL(u string) error {
	if !strings.HasPrefix(u, "https://") && !strings.HasPrefix(u, "http://") {
		return errors.New("only web links can be opened")
	}
	wruntime.BrowserOpenURL(a.ctx, u)
	return nil
}

// IndexReady reports how many sheets are loaded (0 until the index is ready).
func (a *App) IndexReady() int { return a.index.size() }
