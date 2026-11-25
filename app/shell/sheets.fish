# sheets-desk — fish integration
#
# Streams your current command line (as you type) to the sheets-desk overlay,
# which shows matching cheat sheets. Install: add this to ~/.config/fish/config.fish
#
#     source /path/to/sheets.fish
#
# It writes the command line to a file the Windows overlay polls:
#   %USERPROFILE%\.sheets-desk\ctx.txt   (resolved via cmd.exe + wslpath on WSL)
# Falls back to ~/.sheets-desk/ctx.txt when not on WSL.

function __sheets_write --description 'send current command line to the overlay'
    set -q __sheets_ctx[1]; or return
    printf '%s' (commandline) >$__sheets_ctx 2>/dev/null &
    disown 2>/dev/null
end

function __sheets_self_insert
    commandline -f self-insert
    __sheets_write
end

function __sheets_backspace
    commandline -f backward-delete-char
    __sheets_write
end

function __sheets_delete
    commandline -f delete-char
    __sheets_write
end

function __sheets_install_bindings --description 'bind printable keys to notify the overlay'
    # Printable ASCII (space..~), excluding backslash (0x5c) which bind parses specially.
    for n in (seq 32 126)
        test $n -eq 92; and continue
        set -l ch (printf "%b" (printf '\\x%02x' $n))
        bind -- $ch __sheets_self_insert
    end
    # Deletions
    bind \x7f __sheets_backspace
    bind \b __sheets_backspace
    bind -k backspace __sheets_backspace 2>/dev/null
    bind -k dc __sheets_delete 2>/dev/null
    bind \e\[3~ __sheets_delete 2>/dev/null
end

if status is-interactive
    if not set -q __sheets_ctx
        set -l up ""
        if command -q cmd.exe
            set up (cmd.exe /c 'echo %USERPROFILE%' 2>/dev/null | string trim | string trim --chars=\r)
        end
        if test -n "$up"; and command -q wslpath
            set -g __sheets_ctx (wslpath "$up" 2>/dev/null)/.sheets-desk/ctx.txt
        else
            set -g __sheets_ctx "$HOME/.sheets-desk/ctx.txt"
        end
        mkdir -p (dirname "$__sheets_ctx") 2>/dev/null
    end
    __sheets_install_bindings
end
