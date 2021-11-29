from mesa import Agent
from collections import defaultdict
from queue import PriorityQueue



def h(src, dst):
    x1, y1 = src
    x2, y2 = dst 
    return abs(x1 - x2) + abs(y1 - y2)


class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model, state):
        super().__init__(unique_id, model)
        self.state = state

class TileAgent(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.realNeighbors = []
        self.direction = direction
        self.isCarDestination = False
        self.hasCar = False

class CarAgent(Agent):
    def __init__(self, unique_id, model, boxDst):
        super().__init__(unique_id, model)
        self.direction = 0
        self.destination = ()
        self.blinkers = [False, False]
        self.numMoves = 0
        self.path = []
    
    def getDirection(self, nextStep) -> int:

        # face north if moving up
        if nextStep[1] > self.pos[1]:
            return 180
        
        # face south if moving down
        if nextStep[1] < self.pos[1]:
            return 0
        
        # face east if moving right 
        if nextStep[0] > self.pos[0]:
            return 270
        
        # face west if moving right 
        if nextStep[0] < self.pos[0]:
            return 90


    def findPathTo(self, dst) -> bool:
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

        if not self.path:
            self.findPathTo(self.destination)
        
        nextPos = self.path[-1]
        self.direction = self.getDirection(nextPos)
        carInFront = False
        redLight = False
        for agent in self.model.grid.get_cell_list_contents(nextPos):
            if isinstance(agent, TrafficLightAgent) and agent.state == "red":
                redLight = True

            if isinstance(agent, CarAgent):
                carInFront = True
                break
        
        if not carInFront and not redLight:
            self.model.grid.move_agent(self, self.path.pop())
    

    def step(self):
        
        self.move()