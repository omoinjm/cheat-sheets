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

# Reliable fallback: always fire when a command is run, regardless of whether
# the per-keystroke bindings took. Auto-registers when this function is defined.
function __sheets_preexec --on-event fish_preexec
    set -q __sheets_ctx[1]; or return
    printf '%s' $argv[1] >$__sheets_ctx 2>/dev/null &
    disown 2>/dev/null
end

function __sheets_install_bindings --description 'notify the overlay on word boundaries'
    # Rebinding every printable key made typing lag badly: each keystroke forked
    # a background job and wrote across the WSL->Windows boundary (drvfs), which
    # backs up fish's input loop. Instead fire only on space — i.e. once per
    # word/subcommand, which is when a match becomes meaningful — and on Enter
    # (via fish_preexec). Normal letters keep fish's fast native self-insert.
    bind ' ' __sheets_self_insert 2>/dev/null
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
