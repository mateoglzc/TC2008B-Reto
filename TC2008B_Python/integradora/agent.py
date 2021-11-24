from mesa import Agent
from collections import defaultdict
from queue import PriorityQueue

""" Things to fix:
    - 2 or more robots move into the same cell
"""


def h(src, dst):
    x1, y1 = src
    x2, y2 = dst 
    return abs(x1 - x2) + abs(y1 - y2)


class BoxAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class WallAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class TileAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.realNeighbors = []

class BoxDestination(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.numBoxes = 0
        self.full = False
    
    def step(self):
        self.numBoxes = 0
        for agent in self.model.grid.get_cell_list_contents([self.pos]):
            if isinstance(agent, BoxAgent):
                self.numBoxes += 1
        
        if self.numBoxes == 5:
            self.full = True

class RobotAgent(Agent):
    def __init__(self, unique_id, model, boxDst):
        super().__init__(unique_id, model)
        self.hasBox = False
        self.boxSrc = None
        self.boxSrcs = []
        self.boxDst = boxDst
        self.boxId = None
        self.path = []
        self.direction = None
        self.numMoves = 0
    

    def getDirection(self, nextStep):

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


    def findPathTo(self, dst):
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
        self.model.update_neighbors()
        near = self.model.grid.get_neighborhood(
                self.pos,
                moore=False, # don't include diagonal neighbors
                include_center=False) #Doesn't include its own position


        if self.hasBox and self.boxDst not in near:
            foundPath = self.findPathTo(self.boxDst)

            if foundPath:
                self.direction = self.getDirection(self.path[-1])
                self.model.grid.move_agent(self, self.path.pop())
                self.numMoves += 1
        

        elif self.boxSrc and self.boxSrc not in near:
            
            foundPath = self.findPathTo(self.boxSrc)

            if foundPath:
                self.direction = self.getDirection(self.path[-1])
                self.model.grid.move_agent(self, self.path.pop())
                self.numMoves += 1

        else:
            possible = [cell.pos for cell in self.model.grid.get_cell_list_contents(self.pos)[0].realNeighbors]
            newPos = self.model.random.choice(possible)
            self.direction = self.getDirection(newPos)
            self.model.grid.move_agent(self, newPos)
            self.numMoves += 1
    

    def step(self):
        #get direct neighbors
        near = self.model.grid.get_neighborhood(
                self.pos,
                moore=False, # don't include diagonal neighbors
                include_center=True) #Doesn't include its own position


        # if agent has a box and box destination is near 
        if self.hasBox and self.boxDst in near:
            a = BoxAgent(self.boxId, self) # create instance of box agent
            self.model.schedule.add(a) # add it to the schedule
            self.model.grid.place_agent(a, self.boxDst) # place BoxAgent in box destination
            self.hasBox = False
            self.boxSrc = None

        if not self.hasBox:
            fourNeighbors = self.model.grid.iter_neighbors(
            self.pos,
            moore=True, # don't include diagonal neighbors
            include_center=False,
            radius=4) #Doesn't include its own position

            # Detect box in 4 cell range
            for cell in fourNeighbors:
                for agent in self.model.grid.get_cell_list_contents([cell.pos]):
                    if isinstance(agent, BoxAgent) and agent.pos != self.boxDst and agent.pos not in self.model.prevDsts:
                            self.boxSrc = agent.pos
                            break
                        
                        
                
            
            near = self.model.grid.iter_neighbors(
                self.pos,
                moore=False, # don't include diagonal neighbors
                include_center=True) #Doesn't include its own position

            # Pick up box if one is near
            for cell in near:
                for agent in self.model.grid.get_cell_list_contents([cell.pos]):
                    if isinstance(agent, BoxAgent) and agent.pos != self.boxDst and not self.hasBox and agent.pos not in self.model.prevDsts:
                        self.hasBox = True
                        self.boxId = agent.unique_id
                        self.model.grid._remove_agent(agent.pos, agent)
                        self.model.schedule.remove(agent)
                        break
                
                if self.hasBox:
                    break
        
        self.move()