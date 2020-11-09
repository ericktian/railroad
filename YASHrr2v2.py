import networkx as nx
import time
import sys
import queue as Q
import heapq
from tkinter import * #Tk, Canvas, Frame, BOTH
from math import pi , acos , sin , cos


starttime = time.time()

master = Tk()
wid, hei = 1200,700
w = Canvas(master, width=wid, height=hei)
w.pack()


NODESIZE = 1
def shortestPath(init, dest, nToL, G):
    openSet = []
    closedSet = set()
    heapq.heappush(openSet, (cal(init, dest, nToL), 0, init, None))
    z = 0
    while True:
        z+=1
        c = heapq.heappop(openSet)
        closedSet.add(c[2])
        #color blue
        if c[3]!= None:
            w.create_line(x(nodeToLatLong[c[2]][1]), y(nodeToLatLong[c[2]][0]), x(nodeToLatLong[c[3][2]][1]), y(nodeToLatLong[c[3][2]][0]), fill='blue')
        else:
            print("NO")
        if z%10000 ==0:
          #update
          w.update()
          print(z)
        # print(str(c) + " " + str(nodeToEdges[c[2]]))
        for n in nodeToEdges[c[2]]:
            #print(n)
            if n == dest:
                path = [(0,0,n,c)]
                while path[-1][3]:
                    path.append(path[-1][3])

                print("total dist: ", (c[1]+cal(c[2],n,nToL)))
                short =  [yay[2] for yay in path[::-1]]
                #make path red
                for i in range(len(short)-1):
                    w.create_line(x(nodeToLatLong[short[i]][1]), y(nodeToLatLong[short[i]][0]), x(nodeToLatLong[short[i+1]][1]),
                                  y(nodeToLatLong[short[i+1]][0]), fill='red', width=3)

                print("HELLO")
                return short
                # reconstruct path
            if n in closedSet:
                continue
            heapq.heappush(openSet, (cal(n, dest, nToL) + c[1] + cal(c[2], n, nToL), c[1] + cal(c[2], n, nToL), n, c))
            x1 = nodeToLatLong[n][1]
            y1 = nodeToLatLong[n][0]
            x2 = nodeToLatLong[c[2]][1]
            y2 = nodeToLatLong[c[2]][0]
            w.create_line(x(x1), y(y1), x(x2), y(y2), fill='green')
            #w.update()

def cal(init, dest, nToL):
    return calcd(nToL[init][0], nToL[init][1], nToL[dest][0], nToL[dest][1])

def x(l):
    return wid - ((l + 53) / (84) * wid * (-1))
def y(l):
    return (l - 18) / (50) * hei * (-1) + hei - 65
def calcd(y1,x1, y2,x2):
   #
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees

   # if (and only if) the input is strings
 # use the following conversions

   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   #
   R   = 3958.76 # miles = 6371 km
   #
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   #
   # approximate great circle distance with law of cosines
   #
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

G=nx.Graph()

f = open("rrEdges.txt", "r")
edges = f.read().split()
g = open("rrNodes.txt", "r")
nodes = g.read().split()
h = open("rrNodeCity.txt", "r")
fullNames = h.read().split()

nodeToEdges = {}
nodeToLatLong = {}
fullToShortName = {}
# print(edges)
count = 0
for i in edges:
    nodeToEdges[i] = []
while count < len(edges)-1:
    nodeToEdges[edges[count]].append(edges[count+1])
    nodeToEdges[edges[count+1]].append(edges[count])
    count+=2
count = 0
while count < len(nodes)-1:
  nodeToLatLong[nodes[count]] = (float(nodes[count+1]), float(nodes[count+2]))
  count+=3

count = 0
while count < len(fullNames):
    if fullNames[count].isdigit():
        fullToShortName[fullNames[count]] = fullNames[count+1]
        count+=1
    else:
        fullToShortName[fullNames[count-2]] = fullNames[count-1] + fullNames[count]
    count+=1
fullToShortName = {v: k for k, v in fullToShortName.items()}

for n in nodeToLatLong.keys():
    pos1 = (nodeToLatLong[n][1], nodeToLatLong[n][0])
    G.add_node(n, pos=pos1, color="black")
totalD = 0
for n in nodeToEdges.keys():
    for e in nodeToEdges[n]:
        y1 = nodeToLatLong[n][0]
        x1 = nodeToLatLong[n][1]
        y2 = nodeToLatLong[e][0]
        x2 = nodeToLatLong[e][1]
        dist = round(calcd(y1, x1, y2, x2), 2)
        # print(n, " to ", e, dist)
        totalD += dist
        G.add_edge(n, e, weight=dist)
        x1 = wid-((x1+53)/(84)*wid*(-1))
        x2 = wid-((x2+53)/(84)*wid*(-1))
        y1 = (y1-18)/(50)*hei*(-1)+hei-65
        y2 = (y2-18)/(50)*hei*(-1)+hei-65
        w.create_line(x1, y1, x2, y2)

# print("nodeToEdges: ",  nodeToEdges)
# print("nodeToLatLong: ", nodeToLatLong)
# print("fullToShortName: ", fullToShortName)
# print("Total Distance ", totalD, "miles")
short = shortestPath(fullToShortName[sys.argv[1]], fullToShortName[sys.argv[2]], nodeToLatLong, G)


print("SHORTEST PATH: ", short)
# print("SHORTEST PATH: ", shortestPath(sys.argv[1], sys.argv[2], nodeToLatLong))
time.sleep(5)
print (time.time()-starttime)
master.mainloop()
