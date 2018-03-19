# 0: New, 1:Open, 2: Close
# Tuples (Y, X) since grid[rows][cols]

class Block(object):
    def __init__(self, name):
        self.obstacle = 0
        self.tag = 0
        self.name = name
        self.H = None
        self.K = None
        self.B = None

class DStar(object):
    def __init__(self, g, s, w, l, o):
        self.goal = g
        self.start = s
        self.obstacles = o
        self.open = []
        self.cmax = 100000
        self.grid = []
        self.robot = s
        self.width = w
        self.length = l
        self.path = []

    def initialize(self):
        self.grid = [[Block((y, x)) for x in range(self.width)] for y in range(self.length)]

        self.grid[self.goal[0]][self.goal[1]].H = 0
        self.grid[self.goal[0]][self.goal[1]].K = 0
        for entry in self.obstacles:
            self.grid[entry[0]][entry[1]].obstacle = 1

        self.grid[self.goal[0]][self.goal[1]].tag = 1
        self.open.append(self.grid[self.goal[0]][self.goal[1]])

    def sortList(self):
        for num in range(len(self.open)-1, 0, -1):
            for i in range(num):
                if self.open[i].K > self.open[i+1].K:
                    temp = self.open[i]
                    self.open[i] = self.open[i+1]
                    self.open[i+1] = temp

    def neighbor(self, current, new):
        n = []
        newN = []
        
        # Up 1
        if (current[0]-1) >= 0:
            n.append((current[0]-1, current[1]))
            if self.grid[current[0]-1][current[1]].tag == 0:
                newN.append((current[0]-1, current[1]))
            # Up 1 right
            if (current[1]+1) < self.width:
                n.append((current[0]-1, current[1]+1))
                if self.grid[current[0]-1][current[1]+1].tag == 0:
                    newN.append((current[0]-1, current[1]+1))
            # Up 1 left
            if (current[1]-1) >= 0:
                n.append((current[0]-1, current[1]-1))
                if self.grid[current[0]-1][current[1]-1].tag == 0:
                    newN.append((current[0]-1, current[1]-1))

        # Down 1
        if (current[0]+1) < self.length:
            n.append((current[0]+1, current[1]))
            if self.grid[current[0]+1][current[1]].tag == 0:
                newN.append((current[0]+1, current[1]))
            # Down 1 right
            if (current[1]+1) < self.width:
                n.append((current[0]+1, current[1]+1))
                if self.grid[current[0]+1][current[1]+1].tag == 0:
                    newN.append((current[0]+1, current[1]+1))
            # Down 1 left
            if (current[1]-1) >= 0:
                n.append((current[0]+1, current[1]-1))
                if self.grid[current[0]+1][current[1]-1].tag == 0:
                    newN.append((current[0]+1, current[1]-1))

        # Left
        if (current[1]-1) >= 0:
            n.append((current[0], current[1]-1))
            if self.grid[current[0]][current[1]-1].tag == 0:
                newN.append((current[0], current[1]-1))

        # Right
        if (current[1]+1) < self.width:
            n.append((current[0], current[1]+1))
            if self.grid[current[0]][current[1]+1].tag == 0:
                newN.append((current[0], current[1]+1))

        if new == True:
            return newN
            
        return n

    def c(self, X ,Y):
        if Y.obstacle == 1:
            return self.cmax
        elif X.name[0] == Y.name[0] or X.name[1] == Y.name[1]:
            return 1
        else:
            return 1.4

    def insert(self, point, hnew):
        hnew = min(self.cmax, hnew)
        if point.tag == 0:
            point.K = hnew
        elif point.tag == 1:
            point.K = min(hnew, point.K)
        else:
            point.K = min(hnew, point.H)
        point.H = hnew
        point.tag = 1
        self.open.append(point)
        self.sortList()
        return point

    def backpointerList(self):
        cur = self.grid[self.robot[0]][self.robot[1]]
        while cur.name != self.goal:
            self.path.append(cur.name)
            print(cur.name)
            cur = self.grid[cur.B[0]][cur.B[1]]
        if len(self.path) == 0:
            print("No Possible Path")

        self.path.append(cur.name)
        return self.path
        
    def processState(self, new):

        cur = self.open.pop(0)
        kold = cur.K
        self.grid[cur.name[0]][cur.name[1]].tag = 2

        n = self.neighbor(cur.name, new)

        if kold < cur.H:
            for entry in n:
                Y = self.grid[entry[0]][entry[1]]
                if Y.H <= kold and cur.H >=Y.H + self.c(Y, cur):
                    self.grid[cur.name[0]][cur.name[1]].B = Y.name
                    self.grid[cur.name[0]][cur.name[1]].H = Y.H + self.c(Y, cur)
        elif kold == cur.H:
            for entry in n:
                Y = self.grid[entry[0]][entry[1]]
                if (Y.tag == 0 or (Y.B == cur.name and Y.H != cur.H + self.c(cur, Y)) or
                        (Y.B!= cur.name and Y.H > cur.H + self.c(cur, Y))):
                        Y.B = cur.name
                        self.grid[entry[0]][entry[1]] = self.insert(Y, cur.H + self.c(cur, Y))
        else:
            for entry in n:
                Y = self.grid[entry[0]][entry[1]]
                if Y.tag == 0 or (Y.B == cur.name and Y.H != cur.H + self.c(cur, Y)):
                    Y.B = cur.name
                    self.grid[entry[0]][entry[1]] = self.insert(Y, cur.H + self.c(cur, Y))
                else:
                    if Y.B!= cur.name and Y.H > cur.H + self.c(cur, Y):
                        self.grid[cur.name[0]][cur.name[1]] = self.insert(cur, cur.H)
                    else:
                        if (Y.B!= cur.name and cur.H > Y.H + self.c(Y, cur) and Y.tag == 2
                                and Y.H > kold):
                            self.grid[entry[0]][entry[1]] = self.insert(Y, Y.H)

        if (len(self.open) == 0):
            return -1
        return self.open[0].K

    def initPlan(self):
        self.initialize()
        while 1:
            kmin = self.processState(True)
            if kmin == -1 or self.grid[self.start[0]][self.start[1]].tag == 2:
                break
        return self.backpointerList()

    def modifyCost(self, X):
        X = self.grid[X[0]][X[1]]
        if X.tag == 2 and X.obstacle == 1:
            self.grid[X.name[0]][X.name[1]] = self.insert(X, self.cmax)
        elif X.tag == 2:
            self.grid[X.name[0]][X.name[1]] = self.insert(X, X.H)
        
    
    def prepareRepair(self):
        n = self.neighbor(self.robot, False)
        toEdit = []
        for elem in n:
            if self.grid[elem[0]][elem[1]].obstacle == 0 and (elem in self.obstacles):
                self.grid[elem[0]][elem[1]].obstacle = 1
                toEdit.append(elem)
                toEdit.extend(self.neighbor(elem, False))
        for e in toEdit:
            self.modifyCost(e)

    def repairReplan(self):
        while 1:
            kmin = self.processState(False)
            if kmin == -1 or self.grid[self.start[0]][self.start[1]].tag == 2:
                break
        return self.backpointerList()

    def run2(self):
        index = 0
        while self.robot != self.goal:
            self.prepareRepair()
            path = self.repairReplan()
            if len(path) == 0:
                return -1
            index += 1
            self.robot = path[index]
        return path
            
