# 0: New, 1:Open, 2: Close
# Tuples (Y, X) since grid[rows][cols]

class Block(object):
    def __init__(self, g, s, o,  name):
        self.goal = g
        self.start = s
        self.obstacle = o
        self.tag = 0
        self.name = name
    
    def setH(self, val):
        self.H = val
    def setK(self, val):
        self.K = val
    def setB(self, val):
        self.B = val
    def setTag(self, val):
        self.Tag = val
    def setGoal(self, val):
        self.goal = val
    def setStart(self, val):
        self.start = val
    def setObstacle(self, val):
        self.obstacle = val

width = 6
length = 6
goalIndex = (5, 5)
startIndex = (0, 0)
obstacles = [(2, 2), (2, 3), (2, 4), (2, 5)]

def initialize():
    grid = [[Block(0, 0, 0, (y, x)) for x in range(width)] for y in range(length)]

    grid[goalIndex[0]][goalIndex[1]].setGoal(1)
    grid[goalIndex[0]][goalIndex[1]].setH(0)
    grid[goalIndex[0]][goalIndex[1]].setK(0)
    grid[startIndex[0]][startIndex[1]].setStart(1)
    for entry in obstacles:
        grid[entry[0]][entry[1]].setObstacle(1)

    open = []
    open.append(grid[goalIndex[0]][goalIndex[1]])
    grid[goalIndex[0]][goalIndex[1]].setTag(1)

    return open, grid

def sortList(list):
    for num in range(len(list)-1, 0, -1):
        for i in range(passnum):
            if list[i].K > list[i+1].K:
                temp = list[i].K
                list[i].setK(list[i+1].K)
                list[i+1].setK(temp)

def neighbor(current):
    n = []
    diag = []
    
    # Up 1
    if (current[0]-1) >= 0:
        n.append((current[0]-1, current[1]))
        # UP 1 right
        if (current[1]+1) < width:
            diag.append((current[0]-1, current[1]+1))
        # Up 1 left
        if (current[1]-1) >= 0:
            diag.append((current[0]-1, current[1]-1))

    # Down 1
    if (current[0]+1) < width:
        n.append((current[0]+1, current[1]))
        # Down 1 right
        if (current[1]+1) < width:
            diag.append((current[0]+1, current[1]+1))
        # Down 1 left
        if (current[1]-1) >= 0:
            diag.append((current[0]+1, current[1]-1))

    # Left
    if (current[1]-1) >= 0:
        n.append((current[0], current[1]-1))

    # Right
    if (current[1]+1) < width:
        n.append((current[0], current[1]+1))

    return n, diag


cur = goalIndex
prev = goalIndex
openList, grid = initialize()

while(prev == startIndex):
    openList.pop(0)
    neigh, diagonal = neighbor(cur)

    for val in neigh:
        if grid[val[0]][val[1]].tag == 0:
            openList.append(grid[val[0]][val[1]])
            grid[val[0]][val[1]].setTag(1)
            grid[val[0]][val[1]].setB(cur)
            
            if grid[val[0]][val[1]].obstacle == 0:
                grid[val[0]][val[1]].setH(grid[cur[0]][cur[1]].H + 1)
                grid[val[0]][val[1]].setK(grid[cur[0]][cur[1]].H + 1)
            else:
                grid[val[0]][val[1]].setH(10000)
                grid[val[0]][val[1]].setK(10000)

    for d in diagonal:
        if grid[val[0]][val[1]].tag == 0:
            openList.append(grid[val[0]][val[1]])
            grid[val[0]][val[1]].setTag(1)
            grid[val[0]][val[1]].setB(cur)
            if grid[val[0]][val[1]].obstacle == 0:
                grid[val[0]][val[1]].setH(grid[cur[0]][cur[1]].H + 1.4)
                grid[val[0]][val[1]].setK(grid[cur[0]][cur[1]].H + 1.4)
            else:
                grid[val[0]][val[1]].setH(10000)
                grid[val[0]][val[1]].setK(10000)

    sortList(openList)
    prev = cur
    cur = openList[1].name


