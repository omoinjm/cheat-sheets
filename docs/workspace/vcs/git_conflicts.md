---
title: Git - Resolving Merge Conflicts (Neovim)
description: Step-by-step reference for resolving Git merge conflicts, with the exact Neovim keymaps from this machine's config (git-conflict.nvim + diffview.nvim).
type: content
path: workspace/vcs/git_conflicts.md
tags: [workspace, vcs, git, merge, conflict, neovim, nvim]
---
# Git - Resolving Merge Conflicts (Neovim)

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## 📌 TL;DR Loop
`git merge` → open file → `]x` jump → `co`/`ct`/`cb`/`c0` (or hand-edit) → `:w` → `git add` → `git commit`

---

## 1. Understand the markers
When Git can't auto-merge, it writes both sides into the file:

```
<<<<<<< HEAD          ← "ours"   (your current branch)
your code
=======
their code
>>>>>>> some-branch   ← "theirs" (the incoming branch)
```

Goal: delete the markers and leave the final, correct code.

## 2. Trigger / inspect (terminal)
```bash
git merge some-branch     # or: git pull / git rebase main
git status                # lists files marked "both modified" (unmerged)
```

## 3. Resolve in Neovim — inline (git-conflict.nvim)
Open the conflicted file; conflict blocks are highlighted automatically.

**Navigate**

| Key          | Action                                    |
|--------------|-------------------------------------------|
| `]x`         | Jump to next conflict                     |
| `[x`         | Jump to previous conflict                 |
| `<leader>gc` | List **all** conflicts in quickfix (`:GitConflictListQf`) |

**Choose a side (cursor inside the conflict)**

| Key  | Keeps                         | Command                      |
|------|-------------------------------|------------------------------|
| `co` | **Ours** (HEAD)               | `:GitConflictChooseOurs`     |
| `ct` | **Theirs** (incoming)         | `:GitConflictChooseTheirs`   |
| `cb` | **Both** (ours then theirs)   | `:GitConflictChooseBoth`     |
| `c0` | **None** (delete both sides)  | `:GitConflictChooseNone`     |

> `<leader>` is **Space**. The chosen key rewrites the block and removes all markers.
> If neither side alone is right, just **edit the block by hand** — delete the markers and write the merged result yourself.

## 4. Resolve in Neovim — side-by-side (diffview.nvim)
For tricky 3-way merges:

| Key / Command         | Action                                        |
|-----------------------|-----------------------------------------------|
| `<leader>gd`          | `:DiffviewOpen` — OURS / result / THEIRS panes |
| `<leader>gh`          | `:DiffviewFileHistory`                        |
| `<leader>co`          | Take **ours** for the current hunk            |
| `<leader>ct`          | Take **theirs** for the current hunk          |
| `]x` / `[x`           | Next / previous conflict hunk                 |
| `:DiffviewClose`      | Close the diff view                           |

## 5. Verify — no markers left behind
```vim
/<<<<<<<        " search; also check =======  and  >>>>>>>
```
If the search finds nothing, the file is clean. Then `:w`.

## 6. Finish the operation (terminal)
```bash
git add <file>        # stage each resolved file
git status            # confirm nothing is still "unmerged"
git commit            # completes a MERGE (opens editor for the message)
```

**If rebasing instead of merging:**
```bash
git add <file>
git rebase --continue
```

**Bail out entirely (reset to pre-merge state):**
```bash
git merge  --abort
git rebase --abort
```

---

## ⚡ Quick Reference

| Situation                        | Do this                                      |
|----------------------------------|----------------------------------------------|
| See every conflict at once       | `<leader>gc` (quickfix list)                 |
| Take my version everywhere       | `co` on each block                           |
| Take incoming version everywhere | `ct` on each block                           |
| Need parts of both               | Hand-edit the block, delete markers          |
| Visual 3-way merge               | `<leader>gd` (Diffview)                       |
| Messed it up, start over         | `git merge --abort` / `git rebase --abort`   |
| Done with a file                 | `:w` → `git add <file>`                       |
| Done with all files              | `git commit` (merge) / `git rebase --continue` |

## 🧰 Plumbing (resolve whole files, no editor)
```bash
git checkout --ours   <file>   # keep our version of the entire file
git checkout --theirs <file>   # keep their version of the entire file
git add <file>
```
