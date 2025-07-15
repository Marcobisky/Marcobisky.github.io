#!/bin/bash
# Install Quarto CLI only if not already installed
if ! command -v quarto &> /dev/null; then
    echo "Quarto not found, installing..."
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.32/quarto-1.7.32-linux-amd64.tar.gz
    tar -xvzf quarto-1.7.32-linux-amd64.tar.gz
    export PATH=$PATH:$(pwd)/quarto-1.7.32-linux-amd64/bin
else
    echo "Quarto is already installed"
fi
# Render webpage (incremental rendering with cache and freezer)
quarto render --use-freezer --no-clean
cd tinyml
quarto render --use-freezer --no-clean
cd ..