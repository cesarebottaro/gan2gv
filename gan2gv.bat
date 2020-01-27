@echo off
F:\PortableApps\"Portable Python 3.2.5.1"\App\python.exe gan2gv.py %~n1 > %~n1.gv 
F:\PortableApps\GraphvizPortable\App\graphviz\bin\dot.exe -Tsvg -o"%~n1.svg" -Kdot -q1 "%~n1.gv"
start %~n1.svg
