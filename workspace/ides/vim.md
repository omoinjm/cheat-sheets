---
title: Vim Commands and Tips
description: A collection of essential Vim commands for basics, window management, and language-specific operations.
type: content
path: workspace/ides/vim.md
tags: [workspace, ides, vim, text-editing, productivity]
---
# Vim Commands and Tips

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the IDEs documentation, specifically for the Vim editor.

## Contents Overview

This file provides a collection of essential Vim commands and tips for basic operations, text manipulation, window management, and navigation, aiming to enhance productivity for Vim users.

## Role in System

This resource serves as a quick reference for developers and system administrators who use Vim as their primary text editor. It helps in quickly recalling commands for efficient text editing and workflow management directly within the terminal.

## Key Vim Commands and Operations

### Basics

-   **Delete Selected Text**:
    -   Reference: [How to delete selected text in the vi editor?](https://stackoverflow.com/questions/3114936/how-to-delete-selected-text-in-the-vi-editor)

-   **Undo and Redo Changes**:
    -   Reference: [How to Undo and Redo Changes in Vim?](https://phoenixnap.com/kb/vim-undo-redo)

-   **Move Entire Line Up and Down**:
    -   Move a line up: `ddkP`
    -   Move a line down: `ddp`
    -   Reference: [Move entire line up and down in Vim?](https://stackoverflow.com/questions/741814/move-entire-line-up-and-down-in-vim)

### Window Management

-   `sf`: Fuzzy Finder (custom mapping, typically `CtrlP` or `fzf` integration)
-   `sv`: Vertical split
-   `ss`: Horizontal split
-   `CTRL-w CTRL-o`: Close split window

### Text Selection and Insertion

-   `SHift + v`: Select text (visual line mode)
-   `Shift + n`: Insert new file name (context-dependent, likely custom mapping)
-   `p`: Paste

### TSX File Operations (Likely Language Server Protocol Mappings)

-   `ctrl + j`: Hint TSX file (context-dependent)
-   `shift + k`: Element TSX file (context-dependent)
-   `gd`: Go to definition
-   `gb`: Go back (context-dependent)