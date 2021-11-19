from mesa import Agent

from collections import defaultdict
import random

class BoxAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.prevDsts = []

class WallAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class TileAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

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
        self.nextPos = None
        self.boxSrc = None
        self.boxDst = boxDst
        self.vertices = dict()
        self.boxId = None

    
    def moveTo(self, dst):
        newPos = [self.pos[0], self.pos[1]]
        if self.pos[0] < dst[0]:
            newPos[0] += 1
        
        elif self.pos[0] > dst[0]:
            newPos[0] -= 1
        
        if self.pos[1] < dst[1]:
            newPos[1] += 1
        
        elif self.pos[1] > dst[1]:
            newPos[1] -= 1
        
        self.model.grid.move_agent(self, (newPos[0], newPos[1]))

    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # include diagonal neighbors
            include_center=False) #Doesn't include its own position

        if (self.hasBox):
           self.moveTo(self.boxDst)
        
        
        elif (self.boxSrc):
            self.moveTo(self.boxSrc)

        else:
            move = False
            count = 0
            while (not move and count < 8):
                move = True
                self.nextPos = self.random.choice(possibleSteps) # choose random position to move to
                for agent in self.model.grid.get_cell_list_contents([self.nextPos]): 
                    if isinstance(agent, RobotAgent): # check whether random postion contains another Robot
                        if (agent.nextPos == self.nextPos):
                            self.nextPos
                            move = False # if it does, it doesn't move
            
            if move:
                self.model.grid.move_agent(self, self.nextPos) # move roomba to random possible position
    

    def step(self):
        #get direct neighbors
        near = self.model.grid.iter_neighbors(
                self.pos,
                moore=True, # include diagonal neighbors
                include_center=True) #Doesn't include its own position

        near_pos = [cell.pos for cell in near]

        # if agent has a box and box destination is near 
        if self.hasBox and self.boxDst in near_pos:
            a = BoxAgent(self.boxId, self) # create instance of box agent
            self.model.schedule.add(a) # add it to the schedule
            self.model.grid.place_agent(a, self.boxDst) # place BoxAgent in box destination
            self.hasBox = False
            self.boxSrc = None

        if not self.hasBox:
            fourNeighbors = self.model.grid.iter_neighbors(
            self.pos,
            moore=True, # include diagonal neighbors
            include_center=False,
            radius=4) #Doesn't include its own position

            for cell in fourNeighbors:
                for agent in self.model.grid.get_cell_list_contents([cell.pos]):
                    if isinstance(agent, BoxAgent) and agent.pos != self.boxDst and agent.pos not in agent.prevDsts:
                        self.boxSrc = agent.pos
                        break
                
                if self.boxSrc:
                    break
            
            near = self.model.grid.iter_neighbors(
                self.pos,
                moore=True, # include diagonal neighbors
                include_center=True) #Doesn't include its own position

            for cell in near:
                for agent in self.model.grid.get_cell_list_contents([cell.pos]):
                    if isinstance(agent, BoxAgent) and agent.pos != self.boxDst and not self.hasBox and agent.pos not in agent.prevDsts:
                        print("Found Box")
                        self.hasBox = True
                        self.boxId = agent.unique_id
                        self.model.grid._remove_agent(agent.pos, agent)
                        self.model.schedule.remove(agent)
        
        self.move()

        

