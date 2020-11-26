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
        
        


with open("map.txt") as f: 
    space = f.read().splitlines()

nodesList = []
for y, line in enumerate(space): 
    for x, char in enumerate(line):
        if char not in ['*', ' ']:
            nodesList.append(Node(char, x, y))


for n in nodesList: print(n.name, n.x, n.y)
mapPrinter(space)

targetNode = nodesList[0]
startNode = nodesList[3]
print(f"Start: {startNode.__dict__} Target: {targetNode.__dict__}")
candidate = Candidate(startNode.x, startNode.y, 0, manhattanDistance(startNode,targetNode))


closedList = []
cToExpand = candidate
fringe = [cToExpand]
path = [cToExpand]
while cToExpand.x != targetNode.x or cToExpand.y != targetNode.y:
    print(f"\nTo expand: {cToExpand.__dict__}")
    path.append(cToExpand)
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
                                manhattanDistance(point, startNode), 
                                manhattanDistance(point, targetNode))
            #print(f"Possible Move: {candidate.__dict__}")
            if not any(c.__eq__(candidate) for c in closedList):
                #print(f"Appending for {candidate.__dict__}")
                fringe.append(candidate)
            """print(f"Candidate {candidate.__dict__}")
            if candidate.g < cToExpand.g and any(c.__eq__(candidate) for c in closedList):
                candidate = Candidate(point.x, point.y, 1, currH)
                print(f"New Candidate by h: {candidate.__dict__}")
            elif(candidate.h == cToExpand.h): 
                print(f"New Candidate by tie: {candidate.__dict__}")
                candidate = decideATie(candidate, Candidate(point.x, point.y, 1, currH))"""
    
    
    closedList.append(fringe.pop(fringe.index(cToExpand)))          
    """for n in fringe:
        print(f"Fringe: {n.__dict__}")"""
    cToExpand = min(fringe, key=lambda c: (c.g + c.h))

print(f"Found: {cToExpand.__dict__} ")
for p in path:
    print(p.__dict__)

"""while currentPos.x != targetNode.x or currentPos.y != targetNode.y:
    print(f"Current pos: {candidate.__dict__}")
    possibleMoves = [
                    Point(currentPos.x+1,currentPos.y), #right
                    Point(currentPos.x-1,currentPos.y), #left
                    Point(currentPos.x,currentPos.y+1), #down
                    Point(currentPos.x,currentPos.y-1)  #up
                    ]
    for point in possibleMoves:
        if not isAsterix(space, point): 
            print(f"Possible move not *: {point.x}, {point.y}")
            print(f'From {point.x},{point.y} to {targetNode.x},{targetNode.y}'
                    f' Distance: {manhattanDistance(point, targetNode)}\n')
            currDistance = manhattanDistance(point, targetNode)
            if (candidate.mDistance == -1 or 
                currDistance < candidate.mDistance):
                candidate = Candidate(point.x, point.y, currDistance)
            elif(candidate.mDistance == currDistance): 
                candidate = decideATie(candidate, Candidate(point.x, point.y, currDistance))
            

    print(f"\nMy candidate is: {candidate.x},{candidate.y} with d= {candidate.mDistance}")
    currentPos = candidate  
    candidate = Candidate(-1,-1,-1)  """

       
    
        
              


 
