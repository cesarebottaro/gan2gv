# gan2gv project
Python code to convert a .gan files (created by [Ganttproject](https://www.ganttproject.biz/))
to different formats, mainly to .gv format ([Graphviz](https://graphviz.org/) dot format).
The goal is to show the related PERT diagram, with all timings
(ES, EF, LS, LF and slack), and critical path activities in evidence
as a **scalable vectorial graph**.

Main developer: Stefano Livella

Also in this project: 
- example bash script for Linux
- example batch file for Dos/Windows
to convert .gv file to .svg and display it in a web browser.

## Usage examples:

`$ python3 gan2gv.py <ganfile_no_ext>`

produces a .gv file in the standard output; this file must be
processed by Graphviz dot program to show the PERT diagram

`$ python3 gan2csv.py <ganfile_no_ext>`

produces a .csv file in the standard output, containing a table with
all the project activities and timings

`$ python3 gan2html.py <ganfile_no_ext>`

produces a .html file in the standard output, containing all the project
activities and timings

`$ ./gan2html.sh <ganfile_no_ext>`

produces (and opens in web browser) a html page with complete activities table
and PERT diagram (scalable svg generated from .gv file)

## Notes
Graphviz must be installed

Examples provided are for Linux; see the batch file for DOS
