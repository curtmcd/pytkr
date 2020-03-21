#!/bin/bash

if [ ! -r venv/bin/activate ]; then
    echo >&2 'Please use "make venv" first'
    echo >&2 'Note that if your system has the right packages installed'
    echo >&2 'globally then you can just run ./pytkr.py instead.'
    exit 1
fi

. venv/bin/activate

exec python pytkr.py "$@"
