#!/bin/bash

read -p "Path: " P
find "$P" | grep -E "(__pycache__|\.pyc|\.pyo$)" | grep -Ev "(.venv)" | xargs rm -rf

