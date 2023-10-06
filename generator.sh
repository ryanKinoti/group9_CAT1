#!/usr/bin/zsh

python3 main.py -t=1a -ofo ./outputs

python3 main.py -t=2 -ofo ./outputs

python3 main.py -t=upload -du ./outputs -df hello