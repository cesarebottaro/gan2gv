@echo off
if exist %~n1.svg del %~n1.svg
F:\PortableApps\"Portable Python 3.2.5.1"\App\python.exe gan2gv.py %~n1 > %~n1.gv 
F:\PortableApps\GraphvizPortable\App\graphviz\bin\dot.exe -Tsvg -o"%~n1.svg" -Kdot -q1 "%~n1.gv"
if exist %~n1.svg start %~n1.svg
