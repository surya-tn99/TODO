#!/bin/bash

echo 'cleaning terminal'
clear

echo 'Activating Python Virtual Environment'
source ~/.virtualenv/pyenv/bin/activate

echo 'Start Executing TODO'
python3 ~/Software/TODO/TODO.py

echo ''
echo 'Deactivating Python Virtual Environment'
deactivate

