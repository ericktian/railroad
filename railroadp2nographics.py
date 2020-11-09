import time
import networkx as nx
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import queue as Q
starttime = time.time()
file = open("rrEdges.txt", "r")
edges = file.read().split("\n")
file = open("rrNodes.txt", "r")
nodes = file.read().split("\n")
file = open("rrNodeCity.txt", "r")
names = file.read().split("\n")
import sys

namesDict = {}
namesDict2 = {}
for i in names:
    temp = i.split(' ')
    namesDict[temp[1]] = temp[0]
    namesDict2[temp[0]] = temp[1]
#print(namesDict)

nodesDict = {}
for i in nodes:
    templist = i.split(' ')
    nodesDict[templist[0]] = (float(templist[2]), float(templist[1]))

# G = nx.Graph()
for i in nodes:
    dict = {}
    temp = i.split(' ')
    dict['pos'] = nodesDict[temp[0]]
    # G.add_node(temp[0], pos=nodesDict[temp[0]], color='r')
edgesDict = {}
for i in edges:
    temp = i.split(' ')
    if temp[0] in edgesDict: edgesDict[temp[0]].append(temp[1])
    else: edgesDict[temp[0]] = [temp[1]]
    if temp[1] in edgesDict: edgesDict[temp[1]].append(temp[0])
    else: edgesDict[temp[1]] = [temp[0]]

totaldistance = 0
# def calcEdge(s1, s2):
#     return ((nodesDict[s1][0]-nodesDict[s2][0])**2 + (nodesDict[s1][1]-nodesDict[s2][1])**2)**.5
#
# Torbert, 22 Sept 2014
# White (ed), 5 Oct 2016
#
from math import pi , acos , sin , cos
#
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
   #a = sin(y1)*sin(y2)
   #b = cos(y1)*cos(y2)*cos(x2-x1)
   #return acos(a+b)*R

    return acos( round((sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)), 5) ) * R #I ROUNDED THIS BC OTHERWISE THERE WAS A WEIRD 1.000000002
   #
#
# end of file
#
weightDict = {}
for i in edges:
    temp = i.split(' ')
    weight = round(calcd(nodesDict[temp[0]][1], nodesDict[temp[0]][0], nodesDict[temp[1]][1], nodesDict[temp[1]][0]), 2)
    weightDict[(temp[0], temp[1])] = weight
    weightDict[(temp[1], temp[0])] = weight

def neighbors(node):
    return edgesDict[node]

def finish(start, end, dictAlreadySeen):
    path = []
    counter = 1
    pathlocation = end
    path.insert(0, pathlocation)
    while (dictAlreadySeen[pathlocation] != start):
        path.insert(0, dictAlreadySeen[pathlocation])
        pathlocation = dictAlreadySeen[pathlocation]
    path.insert(0, start)
    #print(path)
    #tempsizes = [0.1] * len(list(namesDict))
    totalweight = 0
    last = start
    #print(start)
    for i in path:
        # G.node[i]['color'] = 'g'
        # print(namesDict2[last])
        # print(i)
        # a = float(last[1])*pi/180.0
        # b = float(last[0])*pi/180.0
        # c = float(i[1])*pi/180.0
        # d = float(i[0])*pi/180.0
        # print('a: ', a)
        # print('b: ', b)
        # print('c: ', c)
        # print('d: ', d)
        # ans = sin(a) * sin(c) + cos(a) * cos(c) * cos(d - b)
        # print(ans)
        # print(acos(ans))
        # print(acos(ans) * 3958.76)
        # print(calcd(a, b, c, d))
        #totalweight += calcd(a, b, c, d)


        totalweight += calcd(last[1], last[0], i[1], i[0])
        last = i
        #G.node[i][]
    # G.node[end]['color'] = 'g'
    print("totalweight: ", totalweight)
    # color = nx.get_node_attributes(G, 'color')
    # nx.draw(G, pos, with_labels=True, node_color=list(color.values()))
    # plt.pause(10)
    # plt.savefig('romp2.png')

def Astar(start, end):
    openSet = Q.PriorityQueue()
    tuproot = (calcd(nodesDict[start][1], nodesDict[start][0], nodesDict[end][1], nodesDict[end][0]), start)
    openSet.put(tuproot)
    closedSet = set()
    alreadySeen = {start: start}
    pathlens = {start: 0}

    numTimesImproved = 0
    numTimesRemoved = 0

    notdone = True
    # G.node[start]['color'] = 'b'
    # color = nx.get_node_attributes(G, 'color')
    # nx.draw(G, pos, node_color=list(color.values()), node_size=0.1)
    # plt.draw()

    while notdone and openSet.qsize() > 0:
        current = openSet.get(0)[1]
        numTimesRemoved += 1
        if current == end:
            notdone = False
            finish(start, end, alreadySeen)
            continue
        closedSet.add(current)
        for n in neighbors(current):
            newpathlencount = pathlens[current] + weightDict[(current, n)]

            if not n in pathlens or newpathlencount < pathlens[n]:
                if n in pathlens:
                    numTimesImproved += 1
                alreadySeen[n] = current
                pathlens[n] = newpathlencount
                openSet.put((calcd(nodesDict[n][1], nodesDict[n][0], nodesDict[end][1], nodesDict[end][0]) + pathlens[current], n))
        # G.node[current]['color'] = 'b'
        # color = nx.get_node_attributes(G, 'color')
        # nx.draw(G, pos, node_color=list(color.values()), node_size=0.1)
        # plt.draw()
        # plt.pause(.5)


for i in edges:
    temp = i.split(' ')
    # G.add_edge(temp[0], temp[1], weight=weightDict[(temp[0], temp[1])])
    totaldistance += calcd(nodesDict[temp[0]][1], nodesDict[temp[0]][0], nodesDict[temp[1]][1], nodesDict[temp[1]][0])

print("Total distance:", totaldistance, "miles")
# print(namesDict) initial to name
# print(nodesDict) initial to position
# print(edges) list of "edge1 edge2"
# print(edgesDict) edge1 to all edges
# print(weightDict) (edge1, edge2) to weight

# tempcolors = ['r']*len(list(namesDict))

# pos=nx.get_node_attributes(G,'pos')
# color = nx.get_node_attributes(G, 'color')
# nx.draw(G,pos, node_color = list(color.values()), node_size=0.1)
# print(color.values())
# print(len(list(color.values())))
# print(len(list(namesDict)))
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

# plt.ion()
# plt.draw()

one = namesDict[sys.argv[1]]
if(len(sys.argv)<4):two = namesDict[sys.argv[2]]# + " " + sys.argv[3]]
if(len(sys.argv)==4): two = namesDict[sys.argv[2]+sys.argv[3]]

Astar(one, two)


# positions = nx.get_node_attributes(G, 'pos')
# #nx.draw(G, nodesDict)
# nx.draw(G, pos=nodesDict, with_labels=True)
# #nx.draw_networkx_labels(G, nodesDict, namesDict)
#
# pos=nx.get_node_attributes(G,'pos')
# color = nx.get_node_attributes(G, 'color')
# nx.draw(G,pos, with_labels=True, node_color = list(color.values()))
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

# plt.ion()
# plt.draw()

# plt.show()