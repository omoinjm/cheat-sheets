package main

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

// FetchSheet returns the raw markdown of a cheat sheet. It runs server-side so
// the web view never has to make a cross-origin request. The URL must be a
// page on the cheat-sheets site.
func (a *App) FetchSheet(raw string) (string, error) {
	if !strings.HasPrefix(raw, siteBase+"/") {
		return "", errors.New("invalid sheet url")
	}
	client := &http.Client{Timeout: 6 * time.Second}
	resp, err := client.Get(raw)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("http %d", resp.StatusCode)
	}
	b, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
	if err != nil {
		return "", err
	}
	return string(b), nil
}
