import enum
import copy
import queue


class Tiles(enum.Enum):
    Empty = "+"
    River = "*"


class Area:
    def __init__(self, area):
        self.area = area
        self.width = len(area[0])
        self.height = len(area)
        self.currX = None
        self.currY = None

    @classmethod
    def fromSizes(cls, width, height):
        area = [[Tiles.Empty for x in range(width)] for y in range(height)]
        return Area(area)

    @classmethod
    def fromArea(cls, area):
        newArea = copy.deepcopy(area.area)
        return Area(newArea)

    def addRiver(self, x, y):
        self.area[y][x] = Tiles.River
        self.currX = x
        self.currY = y

    def getPossibleNextCoords(self):
        possibleCoords = []
        # West
        westX = self.currX - 1
        if westX >= 0 and self.area[self.currY][westX] == Tiles.Empty:
            possibleCoords.append((westX, self.currY))

        # East
        eastX = self.currX + 1
        if eastX < self.width and self.area[self.currY][eastX] == Tiles.Empty:
            possibleCoords.append((eastX, self.currY))

        # North
        northY = self.currY - 1
        if northY >= 0 and self.area[northY][self.currX] == Tiles.Empty:
            possibleCoords.append((self.currX, northY))

        # South
        southY = self.currY + 1
        if southY < self.height and self.area[southY][self.currX] == Tiles.Empty:
            possibleCoords.append((self.currX, southY))

        return possibleCoords

    def getScore(self):
        score = 0
        for y in range(self.height):
            for x in range(self.width):
                score += self.getTileScore(x, y)
        return score

    def getTileScore(self, x, y):
        if self.area[y][x] != Tiles.Empty:
            return 0

        adjacentRivers = 0
        # West
        westX = x - 1
        if westX >= 0 and self.area[y][westX] == Tiles.River:
            adjacentRivers += 1

        # East
        eastX = x + 1
        if eastX < self.width and self.area[y][eastX] == Tiles.River:
            adjacentRivers += 1

        # North
        northY = y - 1
        if northY >= 0 and self.area[northY][x] == Tiles.River:
            adjacentRivers += 1

        # South
        southY = y + 1
        if southY < self.height and self.area[southY][x] == Tiles.River:
            adjacentRivers += 1

        if adjacentRivers == 0:
            return 1
        elif adjacentRivers == 1:
            return 2
        elif adjacentRivers == 2:
            return 4
        elif adjacentRivers == 3:
            return 6
        else:
            return 8

    def __str__(self):
        return "\n".join(map(lambda row: "".join(map(lambda tile: tile.value, row)), self.area))


class AreaSearcher:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bestScore = -1
        self.bestAreas = []
        self.counter = 0

    def initAreas(self):
        areas = []
        emptyArea = Area.fromSizes(self.width, self.height)
        # Loop over all x and y and only add river source if tile is in the top left quadrant
        # (for symmetry reasons this is enough)
        for x in range(int((self.width + 1) / 2)):
            newArea = Area.fromArea(emptyArea)
            newArea.addRiver(x, 0)
            areas.append(newArea)
        for y in range(int((self.height + 1) / 2)):
            if y == 0:
                continue
            newArea = Area.fromArea(emptyArea)
            newArea.addRiver(0, y)
            areas.append(newArea)
        return areas

    def getNextStepAreas(self, area):
        areas = []
        coords = area.getPossibleNextCoords()
        for coord in coords:
            newArea = Area.fromArea(area)
            newArea.addRiver(coord[0], coord[1])
            areas.append(newArea)
        return areas

    def bfs(self, maxIterations=10000000):
        searchQueue = queue.Queue()
        initAreas = self.initAreas()
        for area in initAreas:
            searchQueue.put(area)
        while not searchQueue.empty() and self.counter < maxIterations:
            currArea = searchQueue.get()
            nextStepAreas = self.getNextStepAreas(currArea)
            for area in nextStepAreas:
                searchQueue.put(area)
                areaScore = area.getScore()
                if areaScore > self.bestScore:
                    self.bestScore = areaScore
                    self.bestAreas = [area]
                elif areaScore == self.bestScore:
                    self.bestAreas.append(area)
            self.counter += 1
        return self.bestAreas, self.counter

    def dfs(self, maxIterations=10000000, initAreas=None):
        searchStack = []
        initAreas = self.initAreas() if initAreas is None else initAreas
        for area in initAreas:
            searchStack.append(area)
            self.dfStep(searchStack, maxIterations)
        return self.bestAreas, self.counter

    def dfStep(self, searchStack, maxIterations):
        if self.counter >= maxIterations:
            return
        self.counter += 1
        currArea = searchStack.pop()
        nextStepAreas = self.getNextStepAreas(currArea)
        for area in nextStepAreas:
            searchStack.append(area)
            areaScore = area.getScore()
            if areaScore > self.bestScore:
                self.bestScore = areaScore
                self.bestAreas = [area]
            elif areaScore == self.bestScore:
                self.bestAreas.append(area)
            self.dfStep(searchStack, maxIterations)


width = 6
height = 12
searcher = AreaSearcher(width, height)
res, counter = searcher.bfs(maxIterations=10000)
print("bfs results:")
print("amount of best areas: " + str(len(res)))
print("score: " + str(res[0].getScore()))
print("counter: " + str(counter))
res, counter = searcher.dfs(maxIterations=10000, initAreas=res)
for area in res:
    print("_" * width)
    print(area)
    print("_" * width)
print("dfs results:")
print("amount of best areas: " + str(len(res)))
print("score: " + str(res[0].getScore()))
print("counter: " + str(counter))
