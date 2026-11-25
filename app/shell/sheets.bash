# sheets-desk — bash integration (fallback)
#
# Bash has no simple per-keystroke hook, so this sends each command to the
# overlay just before it runs. Install: add to ~/.bashrc
#
#     source /path/to/sheets.bash

__sheets_ctx=""
if command -v cmd.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1; then
    __sheets_up="$(cmd.exe /c 'echo %USERPROFILE%' 2>/dev/null | tr -d '\r')"
    [ -n "$__sheets_up" ] && __sheets_ctx="$(wslpath "$__sheets_up" 2>/dev/null)/.sheets-desk/ctx.txt"
fi
[ -z "$__sheets_ctx" ] && __sheets_ctx="$HOME/.sheets-desk/ctx.txt"
mkdir -p "$(dirname "$__sheets_ctx")" 2>/dev/null

__sheets_send() { printf '%s' "$1" >"$__sheets_ctx" 2>/dev/null & }

# Fire just before each interactive command runs.
trap '[ -n "$PS1" ] && __sheets_send "$BASH_COMMAND"' DEBUG
