#Final Version updated on 21st September,2016 7:00pm.

from collections import OrderedDict
import copy

inp = open('input.txt','r')
fout=open('output.txt','w')
firstline = inp.readline().strip()
maindict = {}
orderinfo={}
path=[]
graph={}
nodelist=[]
parent_child = {}
data = inp.readline().strip()
source=data

data = inp.readline().strip()
destination = data

data = inp.readline().strip()
number_of_lines=int(data)

# Read number of Live Traffic Lines in Path list
for i in range(0,number_of_lines):
    data = inp.readline().strip()
    path.append(data)

#make node list
for i in range(0,len(path)):
    l=path[i].split(" ")
    if l[0] not in nodelist:
        nodelist.append(l[0])
    if l[1] not in nodelist:
        nodelist.append(l[1])


#Read the Live Traffic Lines and make the graph in maindict dictionary
for i in range(0,len(path)):
    l = path[i].split(" ")
    if l[0] in maindict.keys():
        extradict=maindict[l[0]]
        extradict[l[1]]=l[2]
        maindict[l[0]]=extradict
    else:
        innerdict = {}
        innerdict[l[1]]=l[2]
        maindict[l[0]]=innerdict




#Tie Breaking make dictionary orderinfo
a=[]
for i in range(0,len(path)):
    l = path[i].split(" ")
    if l[0] in orderinfo.keys():
         a=orderinfo.get(l[0])
         a.append(l[1])
    else:
        innerlist = []
        innerlist.append(l[1])
        orderinfo[l[0]] = innerlist


#Add None to leaf nodes in maindict and orderinfo
for i in range(0,len(nodelist)):
    if nodelist[i] not in maindict.keys():
        maindict[nodelist[i]]={}
        orderinfo[nodelist[i]]=[]

#----------------------------------------------------------------------------------------------------------------------#
#BFS Traversal Algorithm
def bfs_traversal():
    queue = [source]
    visited = {}
    templist = []


    p = []

    def backtrack(dest):
        if dest != None:
            p.append(dest)
            backtrack(parent_child[dest])
        else:
            writeinfile()

    def writeinfile():
        c=0
        for e in reversed(list(p)):
            fout.write(e+" %d\n"%c)
            c+=1


    if len(maindict)==0 or len(orderinfo)==0:
        if source==destination:
            fout.write(source + " 0 \n")
    elif source==destination:
        fout.write(source+" 0 \n")
    else:
        parent_child[source]=None
        while len(queue)!=0:
            popped=queue[0]
            del queue[0]
            if popped!=destination:
                templist=orderinfo[popped]
                if templist!=None:
                    for i in range(0,len(templist)):
                        if templist[i] not in parent_child.keys():
                            queue.append(templist[i])
                            parent_child[templist[i]] = popped


            elif popped==destination:
                backtrack(destination)

# print(orderinfo)
# print(path)
# print(maindict)
#----------------------------------------------------------------------------------------------------------------------#
dfsqueue=[]
keyparent={}
dfsexplored=[]

def enqueue(dfssource):
    flag=True
    if dfssource==None:
        return
    elif dfssource in dfsqueue:
        if len(orderinfo):
            dfschildlist=orderinfo[dfssource]
            if len(dfschildlist):
                dfschildlist = dfschildlist[::-1]
                for i in range(0,len(dfschildlist)):
                    if dfschildlist[i] not in dfsqueue:
                        dfsqueue.insert(0,dfschildlist[i])
                        keyparent[dfschildlist[i]]=dfssource
                        flag=False
                if flag==True:
                    return
            else:
                return
        else:
            return
    elif dfssource not in dfsqueue:
        dfsqueue.insert(0,dfssource)
        keyparent[dfssource]=None
    enqueue(dfsqueue[0])

def Call_Dfs():
    flag1=False
    front=dfsqueue[0]
    if front==destination:
        return
    else:
        templist4=orderinfo[front]
        if len(templist4):
            for i in range(0,len(templist4)):
                if templist4[i] not in dfsexplored and templist4[i] not in dfsqueue:
                    flag1=True
            if flag1==True:
                enqueue(front)
            else:
                del dfsqueue[0]
                dfsexplored.append(front)
        else:
            del dfsqueue[0]
            dfsexplored.append(front)
        Call_Dfs()

finalqueue=[]
def printDFS(dest1):
    if dest1==None:
        return
    else:
        finalqueue.append(dest1)
        printDFS(keyparent[dest1])

def finalPrintPathDFS():
    global finalqueue
    count=0
    finalqueue=finalqueue[::-1]
    for i in range(0,len(finalqueue)):
        fout.write(str(finalqueue[i])+" "+str(count)+"\n")
        count+=1


#----------------------------------------------------------------------------------------------------------------------#
openq = {}
openlist = []
closed = {}
childrenlist = []
timeline={}
privatecount=0
def Call_UCS(source):
    global openq
    global openlist
    global closed
    global childrenlist
    global timeline
    global privatecount
    makequeue(source)
    closed={}
    while True:
        if len(openlist) is 0:
            return None
        currnode=openlist[0]
        del openlist[0]
        if currnode==destination:
            return currnode
        Neworderinfo1 = copy.deepcopy(orderinfo)
        childrenlist=Neworderinfo1[currnode]

        for i in range(0,len(childrenlist)):
            child=childrenlist[0]
            del childrenlist[0]
            if child not in openq and child not in closed:
                openlist.append(child)
                privatecount+=1
                timeline[child]=privatecount
                parentlist=openq[currnode]
                nvalue=maindict[currnode][child]
                gvalue=int(parentlist[0])+int(nvalue)
                openq[child]=[gvalue,currnode]
            elif child in openq:
                templist2=openq[child]
                oldvalue=int(templist2[0])
                parentlist = openq[currnode]
                nvalue = maindict[currnode][child]
                gvalue = int(parentlist[0]) + int(nvalue)
                if gvalue<oldvalue:
                    openq[child]=[gvalue,currnode]
                    privatecount+=1
                    timeline[child]=privatecount
            elif child in closed:
                templist3=closed[child]
                oldvalue2=int(templist3[0])
                parentlist = closed[currnode]
                nvalue = maindict[currnode][child]
                gvalue = int(parentlist[0]) + int(nvalue)
                if gvalue < oldvalue:
                    openq[child] = [gvalue, currnode]
                    privatecount += 1
                    timeline[child] = privatecount
                    del closed[child]
                    openlist.append(child)
        closed[currnode]=openq[currnode]
        newq = []
        newdict={}
        for i in range(0, len(openlist)):
            templist = openq[openlist[i]]
            tmvalue=timeline[openlist[i]]
            newlist1=[templist[0],tmvalue]
            newdict[openlist[i]] = newlist1

        sorteddict = OrderedDict(sorted(newdict.items(), key=lambda x: ((x[1][0]),(x[1][1]))))
        for key in sorteddict:
            newq.append(key)
        openlist = newq


def makequeue(source):
    global openq
    global openlist
    global timeline

    openq[source]=[0,None]
    timeline[source]=0
    openlist.insert(0,source)


#def sortByPathCost():
printlist=[]
def printUCS(DestNode):
    global printlist
    printlist.insert(0,DestNode)
    templist1=openq[DestNode]
    if(templist1[1]==None):
        return
    else:
        printUCS(templist1[1])

def printFinalPath():
    for i in range(0,len(printlist)):
        tem=openq[printlist[i]]
        fout.write(str(printlist[i])+" "+str(tem[0])+"\n")

#----------------------------------------------------------------------------------------------------------------------#
sundayline=[]
sundaydict={}
Sunopenq = {}
Sunopenlist = []
Sunclosed = {}
Sunchildrenlist = []
Suntimeline={}
privatecount2=0

def makeSundayDict():
    global sundayline
    global sundaydict
    data = inp.readline().strip()
    number_of_lines = (data)

    if number_of_lines=='' or int(number_of_lines)==0:
        sundaydict={}
    else:
        for i in range(0, int(number_of_lines)):
            data = inp.readline().strip()
            sundayline.append(data)
        for i in range(0,len(sundayline)):
            temp1=(sundayline[i])
            temp2=temp1.split()
            sundaydict[temp2[0]]=temp2[1]

def Call_Astar():
    global Sunopenq
    global Sunopenlist
    global Sunclosed
    global Sunchildrenlist
    global Suntimeline
    global privatecount2
    global sundaydict

    makeSunqueue(source)
    Sunclosed = {}

    while True:
        if len(Sunopenlist) is 0:
            return None
        currnode = Sunopenlist[0]
        del Sunopenlist[0]
        if currnode == destination:
            return currnode
        Neworderinfo = copy.deepcopy(orderinfo)
        Sunchildrenlist = Neworderinfo[currnode]
        for i in range(0, len(Sunchildrenlist)):
            child = Sunchildrenlist[0]
            del Sunchildrenlist[0]

            if child not in Sunopenq and child not in Sunclosed:
                Sunopenlist.append(child)
                privatecount2+=1
                Suntimeline[child]=privatecount2
                parentlist = Sunopenq[currnode]
                nvalue = maindict[currnode][child]
                gvalue = int(parentlist[0]) + int(nvalue)
                Sunopenq[child] = [gvalue, currnode]
            elif child in Sunopenq and child not in Sunclosed :
                if child in sundaydict.keys():
                    SunDictValue=int(sundaydict[child])
                else:
                    SunDictValue=0
                templist2 = Sunopenq[child]
                oldvalue = int(templist2[0])+SunDictValue
                parentlist = Sunopenq[currnode]
                nvalue = maindict[currnode][child]
                gvalue = int(parentlist[0]) + int(nvalue)+SunDictValue
                fvalue=int(parentlist[0]) + int(nvalue)
                if gvalue < oldvalue:
                    Sunopenq[child] = [fvalue, currnode]
                    privatecount2 += 1
                    Suntimeline[child] = privatecount2
            elif child in Sunclosed:
                if child in sundaydict.keys():
                    SunDictValue=int(sundaydict[child])
                else:
                    SunDictValue=0
                templist3 = Sunclosed[child]
                oldvalue2 = int(templist3[0])+SunDictValue
                parentlist = Sunopenq[currnode]
                nvalue = maindict[currnode][child]
                gvalue = int(parentlist[0]) + int(nvalue)+SunDictValue
                fvalue = int(parentlist[0]) + int(nvalue)
                if gvalue < oldvalue2:
                    Sunopenq[child] = [fvalue, currnode]
                    privatecount2 += 1
                    Suntimeline[child] = privatecount2
                    del Sunclosed[child]
                    Sunopenlist.append(child)
        Sunclosed[currnode] = Sunopenq[currnode]
        newq = []
        newdict = {}
        for i in range(0, len(Sunopenlist)):
            templist = Sunopenq[Sunopenlist[i]]
            if Sunopenlist[i] in sundaydict.keys():
                newlist2=[templist[0]+int(sundaydict[Sunopenlist[i]]),Suntimeline[Sunopenlist[i]]]
            else:
                newlist2 = [templist[0], Suntimeline[Sunopenlist[i]]]
            newdict[Sunopenlist[i]] =newlist2

        sorteddict = OrderedDict(sorted(newdict.items(), key=lambda x: (x[1][0],x[1][1])))
        for key in sorteddict:
            newq.append(key)
        Sunopenlist = newq


def makeSunqueue(source):
    global Sunopenq
    global Sunopenlist
    global Suntimeline
    Sunopenq[source] = [0, None]
    Suntimeline[source]=0
    Sunopenlist.insert(0, source)

    # def sortByPathCost():
printlist = []

def printAstar(DestNode):
    global printlist
    printlist.insert(0, DestNode)
    templist1 = Sunopenq[DestNode]
    if (templist1[1] == None):
        return
    else:
        printAstar(templist1[1])

def printFinalPathSun():
    for i in range(0, len(printlist)):
        tem = Sunopenq[printlist[i]]
        fout.write(str(printlist[i]) + " " + str(tem[0]) + "\n")


#----------------------------------------------------------------------------------------------------------------------#
if firstline=='BFS':
    bfs_traversal()

elif firstline=='DFS':
    enqueue(source)
    Call_Dfs()
    printDFS(destination)
    finalPrintPathDFS()



elif firstline=='UCS':
    destnode=(Call_UCS(source))
    printUCS(destnode)
    printFinalPath()


elif firstline=='A*':
    makeSundayDict()
    destnode1 =Call_Astar()
    printAstar(destnode1)
    printFinalPathSun()



















