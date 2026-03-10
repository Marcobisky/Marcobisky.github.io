#!/bin/bash
# This script generates all relevant tex files in generated/ folder for creating English CV pdf only.
# Usage: ./gen.sh <cv-name>  e.g. ./gen.sh cv-lite
NAME=$1
mkdir -p generated/$NAME
python3 utils/json2tex.py global/default.json -s local/$NAME.json -o generated/$NAME/$NAME.tex
sed "s/\\\\input{.*\\.tex}/\\\\input{$NAME.tex}/" template/default.tex > generated/$NAME/main.tex   # change a line in template/default.tex in include $NAME.tex
