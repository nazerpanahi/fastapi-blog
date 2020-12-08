#!/bin/bash

read -p "Path: " P

if [ -d $P ]; then 
    files=$(find $P -type f | grep -Ev ".venv|.git|.vscode|.idea|__pycache__" | grep -E ".py$")
    for f in $files;do
        autopep8 --in-place $f
        echo "$f: OK"
    done
elif [ -f $P ]; then
    autopep8 --in-place f
fi
