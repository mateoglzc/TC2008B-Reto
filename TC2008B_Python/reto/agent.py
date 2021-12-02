from mesa import Agent
from queue import PriorityQueue

directions = {"down": 0, "up": 180, "left": 90, "right": 270}
intermediate = {directions["down"]: (0, -1), directions["up"]: (0, 1), directions["left"]: (-1, 0), directions["right"]: (1, 0)}

def h(src, dst):
    x1, y1 = src
    x2, y2 = dst 
    return abs(x1 - x2) + abs(y1 - y2)


class Destination(Agent):
    """Agent that represents a destination tile"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.realNeighbors = [] # neighbors not including obstacles
        self.hasCar = False

    def step(self): # check whether car is parked in destination
        if not self.hasCar:
            for agent in self.model.grid.get_cell_list_contents(self.pos):
                if isinstance(agent, CarAgent):
                    self.hasCar = True

class Obstacle(Agent):
    """Agent that represents a tile containing a building"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Road(Agent):
    """Agent that represents a road tile"""
    def __init__(self, unique_id, model, directions: list):
        super().__init__(unique_id, model)
        self.realNeighbors = [] # neighbors only including where a car can go from current road
        self.directions = directions # list of road directions (intersections have 2 directions)
        

class TrafficLightAgent(Agent):
    """Traffic light Agent that switches light color every X steps (default X = 10)"""
    def __init__(self, unique_id, model, state, direction, timeToChange = 10):
        super().__init__(unique_id, model)
        self.state = state # traffic light color (red or green)
        self.timeToChange = timeToChange # steps in between light color change
        self.numSteps = 0 # counter to keep track of steps
        self.reverse = {"green": "red", "red": "green"} # dict to reverse light color
        self.direction = direction # direction for Unity visual representation
    
    def step(self):
        self.numSteps += 1
        if self.numSteps % self.timeToChange == 0: # if current number of steps is divisible by 10
            self.state = self.reverse[self.state] # change light colors


class CarAgent(Agent):
    """Car agent that finds path between current position and assigned destination tile,
        responds to its environment to prevent collisions with other cars and follow traffic light rules"""
    def __init__(self, unique_id, model, destination):
        super().__init__(unique_id, model)
        self.direction = 0 # direction car is facing (for Unity visualization)
        self.destination = destination # assigned destination possition
        self.numMoves = 0 # track number of moves for dataCollection
        self.nextPos = None # keep track of next position depending on environment data
        self.path = [] # list of positions to reach destination
        self.parked = False # check if it has reached destination
    
    def getDirection(self, nextStep) -> int:
        """Function to calculate direction the car is facing (for Unity visualization)"""
        # face north if moving up
        if nextStep[1] > self.pos[1]:
            return 180
        
        # face south if moving down
        if nextStep[1] < self.pos[1]:
            return 0
        
        # face east if moving right 
        if nextStep[0] > self.pos[0]:
            return 270
        
        # face west if moving left
        if nextStep[0] < self.pos[0]:
            return 90


    def findPathTo(self, dst) -> bool:
        """A* pathfinding algorithm to find path between car and its destination
            taking into consideration the road's realNeighbors to follow traffic rules"""
        self.path = []
        count = 0
        open_set = PriorityQueue()
        start = self.model.grid.get_cell_list_contents(self.pos)[0]
        end = self.model.grid.get_cell_list_contents(dst)[0] 
        open_set.put((0, count, start))
        came_from = {}
        g_score = {contents[0]: float("inf") for contents, x, y in self.model.grid.coord_iter()}
        g_score[start] = 0
        f_score = {contents[0]: float("inf") for contents, x, y in self.model.grid.coord_iter()}
        f_score[start] = h(start.pos, end.pos)
        open_set_hash = {start}

        near_end = [cell.pos for cell in end.realNeighbors]
        
        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current.pos in near_end:
                end = current
                while end in came_from:
                    self.path.append(end.pos)
                    end = came_from[end]

                return True
            
            for neighbor in current.realNeighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.pos, dst)
                    
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
            
        return False
    

    def move(self):
        """Function that decides the car's next step and moves the car accordingly,
        taking into consideration the cars surrounding for proper rule abiding"""
        end = self.model.grid.get_cell_list_contents(self.destination)[0]
        near_end = [cell.pos for cell in end.realNeighbors]
        
        if self.pos in near_end: # if car is near its destination move to it
            self.model.grid.move_agent(self, end.pos)
            self.parked = True # set car as parked
        
        if not self.parked: # if car isn't parked
            if not self.path: # if path hasn't been calcualted
                self.model.updateNeighbors() # update road neighbors
                self.findPathTo(self.destination) # calculate path to car's destination
            
            
            self.nextPos = self.path[-1] # set next pos as next step in path
            
            # check whether next step is a diagonal turn
            roadA = self.model.grid.get_cell_list_contents(self.pos)[0] 
            roadB = self.model.grid.get_cell_list_contents(self.path[-1])[0]
            if abs(self.path[-1][0] - self.pos[0]) == 1 and abs(self.path[-1][1] - self.pos[1]) == 1 and roadA.directions != roadB.directions:
                # if the next step is a diagonal turn but not a lane switch, make turn adding intermediate tile to the path
                inter = intermediate[self.model.grid.get_cell_list_contents(self.pos)[0].directions[0]]
                self.nextPos = (self.pos[0]+inter[0], self.pos[1]+inter[1])

            self.direction = self.getDirection(self.nextPos) # calculate direction car will face for the next step
            
            carInFront = False
            redLight = False
            for agent in self.model.grid.get_cell_list_contents(self.nextPos):
                # check if there are cars or a red traffic light in the next step
                if isinstance(agent, TrafficLightAgent) and agent.state == "red":
                    redLight = True

                if isinstance(agent, CarAgent) and agent.nextPos == self.nextPos:
                    carInFront = True
                    break
            
            if not carInFront and not redLight: # if there aren't any cars and no red traffic lights in the car's next step
                # move to the next step
                if abs(self.path[-1][0] - self.pos[0]) == 1 and abs(self.path[-1][1] - self.pos[1]) == 1 and roadA.directions != roadB.directions:
                    self.model.grid.move_agent(self, (self.pos[0]+inter[0], self.pos[1]+inter[1]))
                
                else:
                    self.model.grid.move_agent(self, self.path.pop())
                
                self.numMoves += 1

            else: # if there is a car or a red traffic light, don't move
                self.nextPos = self.pos
        
    

    def step(self):
        if not self.parked: # only move if car isn't parked (AKA hasn't reached destination)
            self.move()