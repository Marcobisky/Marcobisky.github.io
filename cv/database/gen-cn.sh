#!/bin/bash
# This script generates all relevant tex files in generated/ folder for creating Chinese CV pdf only.
# Usage: ./gen-cn.sh <cv-name>  e.g. ./gen-cn.sh cv-lite-cn
NAME=$1
mkdir -p generated/$NAME
python3 utils/json2tex.py global/default-cn.json -s local/$NAME.json -o generated/$NAME/$NAME.tex
sed "s/\\\\input{.*\\.tex}/\\\\input{$NAME.tex}/" template/default-cn.tex > generated/$NAME/main.tex   # change a line in template/default-cn.tex in include $NAME.tex
