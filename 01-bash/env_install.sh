#!/bin/bash

pretty_print() {
    printf "\n=== %s ===\n\n" "$1"
}

if [[ "$OSTYPE" == darwin* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == linux-gnu* ]]; then
    OS="linux"
else
    OS="unknown"
fi

pretty_print "Detected OS: $OS"

if command -v python3 > /dev/null; then
    pretty_print "Python 3 is already installed."
    python3 --version
else
    pretty_print "Python 3 is not found, installing ..."
    brew install python3
fi

if python3 -m pip --version > /dev/null 2>&1; then
    pretty_print "Python 3 pip is already installed."
    python3 -m pip --version
else
    pretty_print "Python 3 pip is not found, installing ..."
    python3 -m ensurepip --upgrade
fi    

if [[ "$OS" == "macos" ]]; then
    pretty_print "Installing jupyterlab ..."
    brew install jupyterlab
elif [[ "$OS" == "linux" ]]; then
    pretty_print "Installing jupyter-notebook ..."
    sudo apt install -y jupyter-notebook
fi

if [[ "$OS" == "macos" ]]; then
    pretty_print "Installing doctor ..."
    brew doctor
fi