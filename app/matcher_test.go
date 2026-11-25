package main

import (
	"encoding/json"
	"strings"
	"testing"
)

func testIndex(t *testing.T) *Index {
	t.Helper()
	var root navRoot
	if err := json.Unmarshal(navSnapshot, &root); err != nil {
		t.Fatalf("unmarshal snapshot: %v", err)
	}
	ix := &Index{}
	ix.load(flatten(root))
	if ix.size() == 0 {
		t.Fatal("index empty")
	}
	return ix
}

func TestMatch(t *testing.T) {
	ix := testIndex(t)
	t.Logf("index has %d sheets", ix.size())
	cases := []struct {
		cmd  string
		want string // substring expected in at least one match label
	}{
		{"git merge feature", "Git Merge Conflicts"},
		{"git tag -a v1.0", "Git Tags"},
		{"nvim main.go", "Vim"},
		{"psql -U postgres", "PostgreSQL"},
		{"docker compose up", "Docker"},
		{"ssh user@host", "SSH"},
	}
	for _, c := range cases {
		ms := ix.Match(c.cmd, 6)
		t.Logf("%q -> %d matches", c.cmd, len(ms))
		found := false
		for _, m := range ms {
			t.Logf("    %2d  %-26s [%s]", m.Score, m.Label, m.Breadcrumb)
			if strings.Contains(m.Label, c.want) {
				found = true
			}
		}
		if !found {
			t.Errorf("%q: no match containing %q", c.cmd, c.want)
		}
	}
}
