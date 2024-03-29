#Kerem CÖMERT - 2315190

from Node import Node
from Point import Point
from Candidate import Candidate
from time import time_ns

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
            
def expansionPrinter(space, path):
    print(" ",end="")
    for x in range(9): 
        if(x == 8): print(x)
        else: print(x, end="") 
    for i, line in enumerate(space):
        print(i,end="")
        xsToCross = [c.x for c in path[2] if c.y == i]
        for j, char in enumerate(line):
            if j in xsToCross: print("X",end="")
            else: print(char,end="") 
        print("")
    print("\n")

        
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
nodeNames = [n.name for n in nodesList]

mapPrinter(space, None)

graph = []
paths = []
for index, startNode in enumerate(nodesList):
    for targetNode in nodesList:
        if startNode.name == targetNode.name: continue
        candidate = Candidate(startNode.x, startNode.y, 
                            0, manhattanDistance(startNode,targetNode))

        closedList = [] 
        cToExpand = candidate
        fringe = [cToExpand]
        path = []
        while cToExpand.x != targetNode.x or cToExpand.y != targetNode.y:
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
            
            if space[cToExpand.y][cToExpand.x] not in nodeNames:
                path.append(cToExpand)
        
            
            cToExpand = fringe[0]
            for c in fringe[1:]:
                if (c.g + c.h) < (cToExpand.g +cToExpand.h):
                    cToExpand = c
                elif (c.g + c.h) == (cToExpand.g +cToExpand.h):
                    cToExpand = decideATie(c, cToExpand)
            #printCurrentPos(space, cToExpand)
        graph.append([startNode.name, targetNode.name, cToExpand.g])
        paths.append([startNode.name, targetNode.name, path])

print("\nThese expansions are not the final decided path, but rather "
      "they denote all the candidate points the A* algorithm considered.")
for path in paths:
    print(f"Expanding from {path[0]} to {path[1]}") 
    expansionPrinter(space, path)


#---------TFS, obtaining a dict of dicts------------
adjacencyMatrix = {}
s = 0
for node in nodesList:
    weights = {}
    for pair in graph[s:(s+len(nodesList)-1)]:
        weights[pair[1]] = pair[2]
    s += len(nodesList)-1
    adjacencyMatrix[node.name] = weights
    
for origin in adjacencyMatrix.keys():
    for dest in adjacencyMatrix[origin].keys():
        print(f"{origin},{dest},{adjacencyMatrix[origin][dest]}")


#--------------UCS-----------------------
matrix = adjacencyMatrix #copied it as it will be used again for the next algorithm


startTime = time_ns()
cost = 0
origin = nodeNames[0]
cToExpand = origin
visited = {cToExpand}
visitStr = "A-"
while len(nodeNames) > len(visited):
    minNode = min(matrix[cToExpand], key=matrix[cToExpand].get)
    while minNode in visited:
        matrix[cToExpand].pop(minNode, None)
        minNode = min(matrix[cToExpand], key=matrix[cToExpand].get)
    cost += matrix[cToExpand][minNode]
    visited.add(minNode)
    visitStr += minNode + "-"
    cToExpand = minNode

#loop is over and everywhere is visited, go back to the initial node regardless
cost += matrix[cToExpand][origin]
visitStr += origin
print("\n---Statistics---")
print("With node A taken as a sample, the results below are calculated:")
print("Algorithm Used\tNodes\tTime\tCost")
print(f"UCS\t     {visitStr}\t {time_ns() - startTime}\t{cost}")


#--------------BFS-----------------------
"""even though 2 for loops is a possible solution for this set,
a recursive solution would be a better generalization"""

def breathFirstSearch(cToExpand, matrix, visited):
    visited.append(cToExpand)
    fringe.append(cToExpand)
    visitStr = "A-"
    while fringe:
        s = fringe.pop(0) 
        visitStr += s
        for node in matrix[s]:
            if node not in visited:
                visited.append(node)
                fringe.append(node)
    print(visitStr)
    

startTime = time_ns()
cost = 0
origin = nodeNames[0]
cToExpand = origin
visited = [cToExpand]
fringe = [cToExpand]
visitStr = ""
cost = 0
while fringe:
    s = fringe.pop(0) 
    visitStr += s + "-"
    for node in matrix[s]:
        if node not in visited:
            visited.append(node)
            cost += adjacencyMatrix[origin][node]
            fringe.append(node)
cost += adjacencyMatrix[origin][node]
visitStr += "A" 

print(f"BFS\t     {visitStr}\t {time_ns() - startTime}\t{cost}")
print("Since there are only 4 nodes with a max. depth of 2 in this particular case,"
      "the calculated runtimes of both algorithms are insignificantly small. Even with"
      " nanosecond precision, no difference is detected."
      "A larger data set is neeeded in order to accurately judge the performance.")





        



        
         
        


       
    
        
              


 
