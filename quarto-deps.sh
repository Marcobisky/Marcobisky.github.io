#!/bin/bash
# Install Quarto CLI
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.32/quarto-1.7.32-linux-amd64.tar.gz
tar -xvzf quarto-1.7.32-linux-amd64.tar.gz
export PATH=$PATH:$(pwd)/quarto-1.7.32-linux-amd64/bin
# Render webpage (incremental rendering with cache and freezer)
quarto render --use-freezer
cd tinyml
quarto render --use-freezer
cd ..