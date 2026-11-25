package main

import (
	"os"
	"path/filepath"
	"strings"
	"time"

	wruntime "github.com/wailsapp/wails/v2/pkg/runtime"
)

// ctxDir is where the shell hook drops the current command line.
// Windows: %USERPROFILE%\.sheets-desk ; elsewhere: ~/.sheets-desk
func ctxDir() string {
	home, err := os.UserHomeDir()
	if err != nil || home == "" {
		if up := os.Getenv("USERPROFILE"); up != "" {
			home = up
		}
	}
	return filepath.Join(home, ".sheets-desk")
}

func ctxFilePath() string { return filepath.Join(ctxDir(), "ctx.txt") }

// SuggestPayload is emitted to the UI as the "suggest" event.
type SuggestPayload struct {
	Query   string  `json:"query"`
	Matches []Match `json:"matches"`
}

// startWatcher polls the ctx file and pushes fresh suggestions to the UI
// whenever the command line the shell wrote to it changes.
func (a *App) startWatcher() {
	path := ctxFilePath()
	go func() {
		var lastMod time.Time
		var lastContent string
		t := time.NewTicker(120 * time.Millisecond)
		defer t.Stop()
		for {
			select {
			case <-a.watchStop:
				return
			case <-t.C:
				fi, err := os.Stat(path)
				if err != nil {
					continue
				}
				if fi.ModTime().Equal(lastMod) {
					continue
				}
				lastMod = fi.ModTime()
				b, err := os.ReadFile(path)
				if err != nil {
					continue
				}
				cmd := strings.Trim(string(b), " \t\r\n")
				if cmd == lastContent {
					continue
				}
				lastContent = cmd
				a.publish(cmd)
			}
		}
	}()
}

// publish computes matches for a command line, stores them, and emits them.
func (a *App) publish(cmd string) {
	payload := SuggestPayload{Query: cmd, Matches: a.index.Match(cmd, 6)}
	a.lastMu.Lock()
	a.last = payload
	a.lastMu.Unlock()
	if a.ctx != nil {
		wruntime.EventsEmit(a.ctx, "suggest", payload)
	}
}

// Current returns the most recent suggestions (so the UI can populate when it
// (re)loads, e.g. after being shown from the tray).
func (a *App) Current() SuggestPayload {
	a.lastMu.Lock()
	defer a.lastMu.Unlock()
	return a.last
}
