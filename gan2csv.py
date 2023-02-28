from xml.dom.minidom import parseString # import easy to use xml parser called minidom
import datetime # to manage calendar dates
import sys # to read command line parameters
import numpy as np # to manage working days and holidays

###### START FUNCTIONS ######

# function that visit each node to determine LS
def find_LS(node,start_nxt_activity,last):
    if not last:
        possible_LS=np.busday_offset(start_nxt_activity,-data[node][0],roll='backward',weekmask=workdays,holidays=holidays_list)
        if possible_LS<data[node][1]:
           data[node][1]=possible_LS
    else:
        data[node][1]=start_nxt_activity
    if node in predecessors:
        for i in predecessors[node]:
            delay="following"
            if -int(i[1])<0:
                delay="backward"
            find_LS(int(i[0]),np.busday_offset(data[node][1],-int(i[1]),roll=delay,weekmask=workdays,holidays=holidays_list),0) 

# function that convert a datetime64 type to datetime type, when string is 1 this function returns a string otherwise a datetime data
def datetime64_to_datetime(date,string):
    new_date=datetime.datetime.strptime(str(date)[:10], "%Y-%m-%d")
    if string:
       return new_date.strftime("%d/%m/%y")
    else:
       return new_date

def create_column(tag, data, style):
    return "<"+tag+" style=\""+style+"\">"+data+"</"+tag+">"

###### END FUNCTIONS ######

if len(sys.argv) < 2:
    print("Name of file .gan is needed!")
    print("Exiting...")
    sys.exit()

filename = sys.argv[1]
file = open(filename+".gan",'r') # open the xml file for reading
data_ganfile = file.read() # convert to string
file.close() # close file because we dont need it anymore
dom = parseString(data_ganfile) # parse the xml you got from the file

predecessors = dict()
data=dict() # contain {duration, LS (infinity at first(9999-12-31))}
nodes_to_visit=dict()
days=['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
holidays_list=[]    # list to handle holidays
workdays=""         # string to manage working days (1 working day, 0 no working day)
start_year=datetime.datetime.strptime("9999-12-31","%Y-%m-%d")
end_year=datetime.datetime.strptime("1000-01-01","%Y-%m-%d")

for node in dom.getElementsByTagName('task'):  # visit every node <task />
    
    if node.getElementsByTagName('task').length==0:
        for a in node.getElementsByTagName('depend'):
            predecessors.setdefault(int(a.getAttribute('id')), []).append([node.getAttribute('id'),a.getAttribute('difference')])
        
        data.setdefault(int(node.getAttribute('id')), []).append(int(node.getAttribute('duration')))
        data.setdefault(int(node.getAttribute('id')), []).append(np.datetime64('9999-12-31','D'))
        
        if node.getElementsByTagName('depend').length==0:
            nodes_to_visit[int(node.getAttribute('id'))]=np.datetime64(node.getAttribute('start'),'D')
        
        if datetime64_to_datetime(node.getAttribute('start'),0)<start_year:
            start_year=datetime64_to_datetime(node.getAttribute('start'),0)
        if datetime64_to_datetime(node.getAttribute('start'),0)>end_year:
            end_year=datetime64_to_datetime(node.getAttribute('start'),0)

#cycle to determine working days
for i in range(0,7):
    workdays=workdays+("1" if dom.getElementsByTagName('default-week')[0].getAttribute(days[i]) == "0" else "0")
workdays = workdays[1:] + workdays[:1]

#cycle to determine holidays
for i in dom.getElementsByTagName('date'):
    if i.getAttribute("year")=="":
        for year in range (int(str(start_year)[:4]),int(str(end_year)[:4])+1):
            holidays_list.append(str(year)+"-"+i.getAttribute("month").zfill(2)+"-"+i.getAttribute("date").zfill(2))
    else:
        holidays_list.append(i.getAttribute("year")+"-"+i.getAttribute("month").zfill(2)+"-"+i.getAttribute("date").zfill(2))

for key in nodes_to_visit:    
    find_LS(key,nodes_to_visit[key],1)

# start creating the graph

print("Name", "D", "ES", "EF", "LS", "LF", "S", sep="|" , end="\n")

for node in dom.getElementsByTagName('task'):
    if node.getElementsByTagName('task').length==0:
        task_id=int(node.getAttribute('id'))
        slack=np.busday_count(np.datetime64(node.getAttribute('start'),'D'),data[task_id][1],weekmask=workdays,holidays=holidays_list)
        
        print (node.getAttribute('name'), sep="", end="|")
        print (str(data[task_id][0]), sep="", end="|")
        print (datetime64_to_datetime(node.getAttribute('start'),1), sep="", end="|") 
      
        if data[task_id][0]>0:
            print (datetime64_to_datetime(np.busday_offset(np.datetime64(node.getAttribute('start'),'D'),
            data[task_id][0]-1, roll='forward', weekmask=workdays, holidays=holidays_list), 1), sep="", end="|")
            
            print (datetime64_to_datetime(data[task_id][1],1), sep="", end="|")
            print (datetime64_to_datetime(np.busday_offset((data[task_id][1]),data[task_id][0]-1,
            roll='following', weekmask=workdays, holidays=holidays_list), 1), sep="", end="|")
            
            print (str(slack), sep="", end="")
        else:
            for x in range(4):
                  print ("-", sep="", end="|")
           
        print ("", sep="", end="\n")
