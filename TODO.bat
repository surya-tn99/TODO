@echo off
title "TODO"
start /b cmd /k "python TODO.py"

timeout /t 2 > nul
start http://127.0.0.1:2006
