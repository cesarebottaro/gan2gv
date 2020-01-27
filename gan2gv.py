# import easy to use xml parser called minidom
from xml.dom.minidom import parseString

import datetime # to manage calendar dates
import sys # to read command line parameters

if len(sys.argv) < 2:
    print("Name of file .gan is needed!")
    print("Exiting...")
    sys.exit()
filename = sys.argv[1]
# open the xml file for reading:
file = open(filename+".gan",'r')
# convert to string:
data = file.read()
# close file because we dont need it anymore:
file.close()
# parse the xml you got from the file
dom = parseString(data)

print ("digraph "+filename+" {")
print ("  rankdir=LR;")
print ("  graph [nodesep=.7, rankdir=LR, splines=ortho];")
print ("  node [shape=record, width=1.5, height=.1];")
print ("  legenda [label = \"{ES|D|EF} | {Task} | {LF|S|LF}\"]")

for node in dom.getElementsByTagName('task'):  # visit every node <task />
    print ("  node_", node.getAttribute('id'), sep="", end="")
    print (" [label = \"{", sep="", end="") # starts node description
    ES=datetime.datetime.strptime(node.getAttribute('start'), "%Y-%m-%d")
    duration=int(node.getAttribute('duration'))
    print (ES.strftime("%d/%m/%y"), sep="", end="")

    if duration > 0:
        delta=datetime.timedelta(days=duration-1)
        print ("|", duration, "|", sep="", end="")
        EF=ES+delta;
        print (EF.strftime("%d/%m/%y"), sep="", end="")
    else:
        delta=datetime.timedelta(days=0) # not used?

    print ("}|{", sep="", end="")
    print (node.getAttribute('name'), "}", sep="", end="")

    if duration > 0:
        print ("|{LS|S|LF}", sep="", end="") # dummy, to refine

    print ("\"]") #  ends node description

    # cycle to draw edges to successors
    print ("  node_", node.getAttribute('id'), " -> {", sep="", end=" ")
    alist = node.getElementsByTagName('depend')
    for a in alist:
        print ("node_", a.getAttribute('id'), sep="", end=" ")
    print ("}")

print ("}")

