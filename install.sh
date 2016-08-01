#!/bin/sh

if cp present.py /usr/local/bin/present; then
  echo "Installed present to /usr/local/bin/present"
  echo "For key bindings, run 'source present.zsh'"
fi
