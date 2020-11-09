import time
import networkx as nx
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
starttime = time.time()
file = open("romEdges.txt", "r")
edges = file.read().split("\n")
file = open("romNodes.txt", "r")
nodes = file.read().split("\n")
file = open("romFullNames.txt", "r")
names = file.read().split("\n")

namesDict = {}
for i in names:
    namesDict[i[0]] = i

nodesDict = {}
for i in nodes:
    templist = i.split(' ')
    nodesDict[templist[0]] = (float(templist[2]), float(templist[1]))

G = nx.Graph()
for i in nodes:
    dict = {}
    dict['pos'] = nodesDict[i[0]]
    G.add_node(i[0], pos=nodesDict[i[0]])

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
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
   #
#
# end of file
#
# print(edges)
# exit()

for i in edges:
    G.add_edge(i[0], i[2])
    totaldistance += calcd(nodesDict[i[0]][1], nodesDict[i[0]][0], nodesDict[i[2]][1], nodesDict[i[2]][0])
# G.add_edge('F','V')
print(totaldistance, "miles")

positions = nx.get_node_attributes(G, 'pos')
#nx.draw(G, nodesDict)
# print(nodesDict)
nx.draw(G, pos=nodesDict, with_labels=True)
#nx.draw_networkx_labels(G, nodesDict, namesDict)
plt.savefig("graph.png")