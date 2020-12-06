#Kerem CÖMERT - 2315190

from Node import Node
from Point import Point
from Candidate import Candidate

def manhattanDistance(p1, p2): return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def isAsterix(space, point): return space[point.y][point.x] == '*'

def decideATie(c1, c2): 
    if(c1.y != c2.y):
        if c1.y < c2.y: return c1
        else: return c2
    else: 
        if(c1.x < c2.x): return c1
        else: return c2

def mapPrinter(space, point):
    print("\n")
    print(" ",end="")
    for x in range(9): 
        if(x == 8): print(x)
        else: print(x, end="") 
    for i, line in enumerate(space):
        print(i,end="")
        if point == None: print(line)
        else:
            if(i == point.y):
                print(line[:point.x] + "X" + line[point.x + 1:])
            else: print(line)
        
with open("map.txt") as f: 
    space = f.read().splitlines()

nodesList = []
for y, line in enumerate(space): 
    for x, char in enumerate(line):
        if char not in ['*', ' ']:
            nodesList.append(Node(char, x, y))

"""ordering nodesList alphabetically, for better clarity especially in the second part
of this task"""
nodesList.sort(key=lambda n: n.name)

for n in nodesList: print(n.name, n.x, n.y)
mapPrinter(space, None)

graph = []
for index, startNode in enumerate(nodesList):
    for targetNode in nodesList:
        if startNode.name == targetNode.name: continue
        candidate = Candidate(startNode.x, startNode.y, 
                            0, manhattanDistance(startNode,targetNode))

        closedList = [] 
        cToExpand = candidate
        fringe = [cToExpand]
        path = [cToExpand]
        #print(f"Start: {startNode.__dict__} Target: {targetNode.__dict__}")
        while cToExpand.x != targetNode.x or cToExpand.y != targetNode.y:
            #print(f"\nTo expand: {cToExpand.__dict__}")
            possibleMoves = [
                            Point(cToExpand.x+1,cToExpand.y), #right
                            Point(cToExpand.x-1,cToExpand.y), #left
                            Point(cToExpand.x,cToExpand.y+1), #down
                            Point(cToExpand.x,cToExpand.y-1)  #up
                            ]
            for point in possibleMoves:
                if not isAsterix(space, point): 
                    candidate = Candidate(point.x,
                                        point.y, 
                                        cToExpand.g + 1, 
                                        manhattanDistance(point, targetNode))
                    if not any(c.__eq__(candidate) for c in closedList):
                        fringe.append(candidate)
            
            #remove the cToExpand from fringe, put to closedList
            closedList.append(fringe.pop(fringe.index(cToExpand)))
            
            cToExpand = fringe[0]
            for c in fringe[1:]:
                if (c.g + c.h) < (cToExpand.g +cToExpand.h):
                    cToExpand = c
                elif (c.g + c.h) == (cToExpand.g +cToExpand.h):
                    cToExpand = decideATie(c, cToExpand)
            #printCurrentPos(space, cToExpand)
            
        #print(f"Found: {cToExpand.__dict__} ")
        graph.append([startNode.name, targetNode.name, cToExpand.g])
        #mapPrinter(space, cToExpand)
        #print(f"{startNode.name},{targetNode.name},{cToExpand.g}")

#print(graph)


#---------TFS, obtaining a dict of dicts------------
adjacencyMatrix = {}
s = 0
for node in nodesList:
    weights = {}
    for pair in graph[s:(s+len(nodesList)-1)]:
        weights[pair[1]] = pair[2]
    #weights.insert(i, 0)
    s += len(nodesList)-1
    adjacencyMatrix[node.name] = weights
    
print(adjacencyMatrix)
#print("\n")

#--------------UCS-----------------------
matrix = adjacencyMatrix #copied it as it will be used again for the next algorithm
nodeNames = list(matrix.keys())
cost = 0
origin = nodeNames[0]
cToExpand = origin
visited = {cToExpand}
visitStr = ""
while len(nodeNames) > len(visited):
    minNode = min(matrix[cToExpand], key=matrix[cToExpand].get)
    while minNode in visited:
        matrix[cToExpand].pop(minNode, None)
        minNode = min(matrix[cToExpand], key=matrix[cToExpand].get)
    cost += matrix[cToExpand][minNode]
    visited.add(minNode)
    print(f"Visited {minNode}")
    visitStr += minNode + "-"
    cToExpand = minNode

#loop is over and everywhere is visited, go back to the initial node regardless
cost += matrix[cToExpand][origin]
visitStr += origin
print(visitStr)






        



        
         
        


       
    
        
              


 
