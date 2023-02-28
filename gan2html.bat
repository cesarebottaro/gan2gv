REM Example batch file
REM Adjust paths to python3 and dot (from Graphviz project)
@echo off
python3.exe gan2gv.py %~n1 > %~n1.gv 
dot.exe -Tsvg -o"%~n1.svg" -Kdot -q1
python3.exe gan2html.py %~n1 > %~n1.html
start %~n1.html
