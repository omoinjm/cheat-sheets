#!/bin/bash
i=0
while IFS= read -r line; do
    line=${line//$'\r'/}
    sed -i -e 's,color'$i'="#.*,color'$i'="'$line'",g' /mnt/c/Users/nhlan/.config/starship/starship.toml
    i=$((i+1))
done < /mnt/c/Users/nhlam/.cache/wal/colors
