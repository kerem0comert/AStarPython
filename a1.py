#Kerem CÖMERT - 2315190

from Node import Node
from Point import Point
from Candidate import Candidate

def manhattanDistance(point, dest):
    return abs(dest.x - point.x) + abs(dest.y - point.y)

def isAsterix(space, point):  return space[point.y][point.x] == '*'
 
def decideATie(c1, c2): 
    if(c1.y != c2.y):
        if c1.y < c2.y: return c1
        else: return c2
    else: 
        if(c1.x < c2.x): return c1
        else: return c2


def mapPrinter(space):
    print("\n")
    print(" ",end="")
    for x in range(9): 
        if(x == 8): print(x)
        else: print(x, end="") 
    for i, line in enumerate(space):
        print(i,end="")
        print(line)
        
def printCurrentPos(space, point):
    print("\n")
    print(" ",end="")
    for x in range(9): 
        if(x == 8): print(x)
        else: print(x, end="") 
    for i, line in enumerate(space):
        print(i,end="")
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


for n in nodesList: print(n.name, n.x, n.y)
mapPrinter(space)


graph = []
for index, startNode in enumerate(nodesList):
    for targetNode in nodesList[index:]:
        if startNode.name == targetNode.name: continue
        candidate = Candidate(startNode.x, startNode.y, 
                            0, manhattanDistance(startNode,targetNode))

        closedList = [] 
        cToExpand = candidate
        fringe = [cToExpand]
        path = [cToExpand]
        print(f"Start: {startNode.__dict__} Target: {targetNode.__dict__}")
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
                                        cToExpand.g, 
                                        manhattanDistance(point, targetNode))
                    if not any(c.__eq__(candidate) for c in closedList):
                        fringe.append(candidate)
            
            visited = fringe.pop(fringe.index(cToExpand))
            if not any(c.__eq__(visited) for c in closedList):
                closedList.append(visited)  
            
            for c in closedList:
                print(c.__dict__)
           
            cToExpand = fringe[0]
            for c in fringe[1:]:
                if (c.g + c.h) > (cToExpand.g +cToExpand.h):
                    cToExpand = c
                elif (c.g + c.h) == (cToExpand.g +cToExpand.h):
                    cToExpand = decideATie(c, cToExpand)
            printCurrentPos(space, cToExpand)
            
        #print(f"Found: {cToExpand.__dict__} ")
        print(f"{startNode.name},{targetNode.name},{cToExpand.g}")
        
        


       
    
        
              


 
