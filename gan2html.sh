# Example bash command file
python3 gan2gv.py  "$1" > "$1.gv"
dot -Tsvg "$1.gv" > "$1.svg"
python3 gan2html.py "$1" > "$1.html"
# Choose your browser: firefox, google-chrome, chromium...
google-chrome "$1.html" &
