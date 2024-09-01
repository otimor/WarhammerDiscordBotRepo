#!/bin/bash

VENV="venv"

test -d $VENV || python3 -m venv $VENV || return
$VENV/bin/pip install -r WarhammerDiscordBot/tests/requirements.txt
$VENV/bin/pip install -r WarhammerDiscordBot/hello_world/requirements.txt
. $VENV/bin/activate
