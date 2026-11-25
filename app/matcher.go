package main

import (
	_ "embed"
	"encoding/json"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"
)

// siteBase is the hosted cheat-sheets site (the data source).
const siteBase = "https://sheets.njmtech.co.za"

//go:embed navdata/nav.json
var navSnapshot []byte

// ---- nav.json shape ----

type navEntry struct {
	Label string `json:"label"`
	Path  string `json:"path"`
}

type navNode struct {
	ID       string     `json:"id"`
	Label    string     `json:"label"`
	Icon     string     `json:"icon"`
	Children []navNode  `json:"children"`
	Entries  []navEntry `json:"entries"`
}

type navRoot struct {
	Home     string    `json:"home"`
	Sections []navNode `json:"sections"`
}

// Sheet is one cheat-sheet page, flattened for matching.
type Sheet struct {
	Label      string `json:"label"`
	Breadcrumb string `json:"breadcrumb"`
	Icon       string `json:"icon"`
	Path       string `json:"path"`
	URL        string `json:"url"` // hash deep-link into the SPA
	Raw        string `json:"raw"` // raw markdown URL (for in-panel render)

	keywords map[string]bool
}

// Match is a scored Sheet returned to the UI.
type Match struct {
	Sheet
	Score int `json:"score"`
}

// Index holds all sheets and supports keyword matching.
type Index struct {
	mu     sync.RWMutex
	sheets []Sheet
}

// command token -> extra topic keywords it should also match.
var aliases = map[string][]string{
	"nvim": {"vim", "neovim"}, "vim": {"vim", "neovim"},
	"psql": {"postgres", "postgresql"}, "pg": {"postgres", "postgresql"}, "postgres": {"postgresql"},
	"k8s": {"kubernetes"}, "kubectl": {"kubernetes"},
	"docker": {"docker", "dockerfile", "compose"}, "docker-compose": {"docker", "compose"},
	"py": {"python"}, "python3": {"python"}, "pip": {"python"},
	"dotnet": {"csharp", "dotnet"}, "cs": {"csharp"},
	"mssql": {"sqlserver", "sql"}, "sqlcmd": {"sqlserver", "mssql"},
	"ssh": {"ssh", "shell"}, "scp": {"ssh"}, "ssh-keygen": {"ssh"},
	"g": {"git"}, "nginx": {"nginx"}, "jwt": {"jwt", "token"},
}

func tokenize(s string) []string {
	s = strings.ToLower(s)
	fields := strings.FieldsFunc(s, func(r rune) bool {
		return !(r >= 'a' && r <= 'z' || r >= '0' && r <= '9' || r == '+' || r == '#')
	})
	out := fields[:0]
	for _, f := range fields {
		if len(f) >= 2 && f != "md" && f != "readme" {
			out = append(out, f)
		}
	}
	return out
}

func (ix *Index) load(sheets []Sheet) {
	ix.mu.Lock()
	ix.sheets = sheets
	ix.mu.Unlock()
}

func (ix *Index) size() int {
	ix.mu.RLock()
	defer ix.mu.RUnlock()
	return len(ix.sheets)
}

// Match ranks sheets against a command line and returns the best few.
func (ix *Index) Match(cmd string, limit int) []Match {
	toks := tokenize(cmd)
	if len(toks) == 0 {
		return nil
	}
	// Expand command tokens with their aliases.
	want := map[string]bool{}
	for _, t := range toks {
		want[t] = true
		for _, a := range aliases[t] {
			want[a] = true
		}
	}
	first := toks[0] // the program being run — strongest signal

	ix.mu.RLock()
	defer ix.mu.RUnlock()

	var matches []Match
	for _, s := range ix.sheets {
		score := 0
		for w := range want {
			if s.keywords[w] {
				score += 3
			} else {
				for kw := range s.keywords {
					if len(w) >= 3 && (strings.HasPrefix(kw, w) || strings.HasPrefix(w, kw)) {
						score++
						break
					}
				}
			}
		}
		// Bonus when the program itself (or its alias) names the topic.
		if s.keywords[first] {
			score += 3
		}
		for _, a := range aliases[first] {
			if s.keywords[a] {
				score += 3
				break
			}
		}
		if score > 0 {
			matches = append(matches, Match{Sheet: s, Score: score})
		}
	}
	// Sort by score desc, then label asc; cap at limit.
	for i := 1; i < len(matches); i++ {
		for j := i; j > 0 && less(matches[j], matches[j-1]); j-- {
			matches[j], matches[j-1] = matches[j-1], matches[j]
		}
	}
	if limit > 0 && len(matches) > limit {
		matches = matches[:limit]
	}
	return matches
}

func less(a, b Match) bool {
	if a.Score != b.Score {
		return a.Score > b.Score
	}
	return a.Label < b.Label
}

// flatten walks the nav tree into a flat list of sheets.
func flatten(root navRoot) []Sheet {
	var out []Sheet
	var walk func(n navNode, crumbs []string, icon string)
	walk = func(n navNode, crumbs []string, icon string) {
		if n.Icon != "" {
			icon = n.Icon
		}
		nc := crumbs
		if n.Label != "" {
			nc = append(append([]string{}, crumbs...), n.Label)
		}
		for _, e := range n.Entries {
			out = append(out, makeSheet(e, nc, icon))
		}
		for _, c := range n.Children {
			walk(c, nc, icon)
		}
	}
	for _, s := range root.Sections {
		walk(s, nil, "📄")
	}
	return out
}

func makeSheet(e navEntry, crumbs []string, icon string) Sheet {
	kw := map[string]bool{}
	for _, t := range tokenize(e.Path) {
		kw[t] = true
	}
	for _, t := range tokenize(e.Label) {
		kw[t] = true
	}
	return Sheet{
		Label:      e.Label,
		Breadcrumb: strings.Join(crumbs, " › "),
		Icon:       icon,
		Path:       e.Path,
		URL:        siteBase + "/#" + url.PathEscape(e.Path),
		Raw:        siteBase + "/" + encodePath(e.Path),
		keywords:   kw,
	}
}

func encodePath(p string) string {
	parts := strings.Split(p, "/")
	for i, s := range parts {
		parts[i] = url.PathEscape(s)
	}
	return strings.Join(parts, "/")
}

// loadIndex populates the index: live nav.json if reachable, else the
// embedded snapshot.
func (a *App) loadIndex() {
	var root navRoot
	if data, err := fetchNav(); err == nil && json.Unmarshal(data, &root) == nil && len(root.Sections) > 0 {
		a.index.load(flatten(root))
		return
	}
	if json.Unmarshal(navSnapshot, &root) == nil {
		a.index.load(flatten(root))
	}
}

func fetchNav() ([]byte, error) {
	client := &http.Client{Timeout: 4 * time.Second}
	resp, err := client.Get(siteBase + "/nav.json")
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	buf := make([]byte, 0, 32*1024)
	tmp := make([]byte, 4096)
	for {
		n, rerr := resp.Body.Read(tmp)
		buf = append(buf, tmp[:n]...)
		if rerr != nil {
			break
		}
		if len(buf) > 1<<20 {
			break
		}
	}
	return buf, nil
}
