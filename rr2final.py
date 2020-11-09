import networkx as nx
import time
import sys
import matplotlib.pyplot as plt
import queue as Q

starttime = time.time()
NODESIZE = 1
from math import pi , acos , sin , cos
def shortestPath(init, dest, nToL, G):
    openSet = Q.PriorityQueue()
    closedSet = set()
    openSet.put((cal(init, dest, nToL), 0, init, None))
    #positions = nx.get_node_attributes(G, 'pos')
    z = 0
    ax = plt.gca()
    canvas = ax.figure.canvas
    background = canvas.copy_from_bbox(ax.bbox)
    pos = positions
    while True:
        z+=1
        c = openSet.get()
        closedSet.add(c[2])
        G.node[c[2]]['draw'] = nx.draw_networkx_nodes(G,pos,nodelist=[c[2]],node_size=NODESIZE,alpha=1.0,node_color='b')
        ax.draw_artist(G.node[c[2]]['draw'])
        if z%5000 ==0:
          #nx.draw_networkx(G, positions, node_size=.1,with_labels= False,node_color=[i for i in nx.get_node_attributes(G, 'color').values()])
            canvas.blit(ax.bbox)
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
                for item in short:
                    G.node[item]['draw'] = nx.draw_networkx_nodes(G,pos,nodelist=[item],node_size=NODESIZE,alpha=1.0,node_color='r')
                    ax.draw_artist(G.node[item]['draw'])
                print("HELLO")
                canvas.blit(ax.bbox)
                time.sleep(100)
                plt.savefig('yashgraph.png')
                print(z)
                return short
                # reconstruct path
            if n in closedSet:
                continue
            openSet.put((cal(n, dest, nToL) + c[1] + cal(c[2], n, nToL), c[1] + cal(c[2], n, nToL), n, c))
            G.node[n]['draw'] = nx.draw_networkx_nodes(G,pos,nodelist=[c[2]],node_size=NODESIZE,alpha=1.0,node_color='g')
            ax.draw_artist(G.node[c[2]]['draw'])
            #nx.draw_networkx(G, positions, node_size=1, font_size=1,
                            # node_color=[i for i in nx.get_node_attributes(G, 'color').values()])

def cal(init, dest, nToL):
    return calcd(nToL[init][0], nToL[init][1], nToL[dest][0], nToL[dest][1])
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
positions = nx.get_node_attributes(G,'pos')
cf = plt.figure(1, figsize=(10,10))
ax = cf.add_axes((0,0,1,1))
nx.draw(G, positions, node_size = 1, width = .5, node_color ='black')
# nx.draw_networkx_edge_labels(G,positions,edge_labels =nx.get_edge_attributes(G,"weight"),font_size = 7)
plt.axis("off")
plt.ion()
plt.show()
print("BUILT")

# print("nodeToEdges: ",  nodeToEdges)
# print("nodeToLatLong: ", nodeToLatLong)
# print("fullToShortName: ", fullToShortName)
# print("Total Distance ", totalD, "miles")
short = shortestPath(fullToShortName[sys.argv[1]], fullToShortName[sys.argv[2]], nodeToLatLong, G)


print("SHORTEST PATH: ", short)
# print("SHORTEST PATH: ", shortestPath(sys.argv[1], sys.argv[2], nodeToLatLong))

print (time.time()-starttime)
