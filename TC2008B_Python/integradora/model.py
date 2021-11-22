# Class definition for Model to be used in the simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import RobotAgent, BoxAgent, BoxDestination, TileAgent
import random
import time


class WarehouseModel(Model):
    """ Model for Roomba simulation """
    def __init__(self,  width, height, numRobots=1, numBoxes=5, seed=None):
        self.numRobots = numRobots
        self.numBoxes = numBoxes
        self.grid = MultiGrid(width, height, False) #No torus
        self.schedule = RandomActivation(self)
        self.running = True # For visualization
        self.startTime = None # For keeping track of time
        self.boxDst = (random.randint(0, width-1), random.randint(0, height-1))
        self.boxesInPlace = []
        self.prevDsts = []
        self.unique_id = 0

        print(self._seed)
        # add tile agents to every cell in grid
        for i in range(width):
            for j in range(height):
                a = TileAgent(self.unique_id, self)
                self.unique_id += 1
                self.schedule.add(a)
                self.grid.place_agent(a, (i, j))
        
        a = BoxDestination(-1, self)
        self.schedule.add(a)
        self.grid.place_agent(a, self.boxDst)
        
        # Add box agents to grid
        for i in range(self.numBoxes):
            a = BoxAgent(self.unique_id, self) # create instance of box agent
            self.unique_id += 1
            self.schedule.add(a) # add it to the schedule

            randomPos = (random.randint(0, width-1), random.randint(0, height-1)) # generate a random position
            contains = True
            while contains: # generate a new randomPos while there is a BoxAgent in randomPos
                contains = False
                agents_in_cell = self.grid.get_cell_list_contents([randomPos])
                for agent in agents_in_cell:
                    if isinstance(agent, BoxAgent) or isinstance(agent, RobotAgent):
                        randomPos = (random.randint(0, width-1), random.randint(0, height-1))
                        contains = True
                        break

            self.grid.place_agent(a, randomPos) # place DirtyAgent in randomPos that isn't already dirty

        # add robot agents to the gird
        for i in range(self.numRobots):
            a = RobotAgent(self.unique_id, self, self.boxDst) #create instance of RobotAngent with unique id starting from 1000
            self.unique_id += 1
            a.boxDst = self.boxDst
            self.schedule.add(a) # add it to the schedule
            randomPos = (random.randint(0, width-1), random.randint(0, height-1)) # generate a random position
            contains = True
            while contains > 0: # generate a new randomPos while there is an Agent in randomPos
                contains = False
                agents_in_cell = self.grid.get_cell_list_contents([randomPos])
                for agent in agents_in_cell:
                    if isinstance(agent, BoxAgent) or isinstance(agent, RobotAgent):
                        randomPos = (random.randint(0, width-1), random.randint(0, height-1))
                        contains = True
                        break
            
            self.grid.place_agent(a, randomPos) # place robot at random position
        
    
    def changeBoxDst(self):
        newBoxDst = random.choice(self.grid.get_cell_list_contents([self.boxDst])[0].realNeighbors)
        while len(newBoxDst.realNeighbors) == 0 and newBoxDst.pos in self.prevDsts:
           newBoxDst = random.choice(self.grid.get_cell_list_contents([self.boxDst])[0].realNeighbors)
        

        for agent in self.schedule.agents:
            if isinstance(agent, RobotAgent):
                agent.boxDst = newBoxDst.pos
            if isinstance(agent, BoxDestination):
                self.grid.move_agent(agent, newBoxDst.pos)
        
        self.prevDsts.append(self.boxDst)
        self.boxDst = newBoxDst.pos
    
    def update_neighbors(self):
        
        for (contents, x, y) in self.grid.coord_iter(): # iterate through each cell
            contents[0].realNeighbors = []
            possible = self.grid.get_neighborhood((x, y), False)
            for neighbor in possible: # iterate through each cell neighbor
                containsObstacle = False
                for agent in self.grid.get_cell_list_contents(neighbor): # iterate through each agent in neighbor
                    if isinstance(agent, BoxAgent) or isinstance(agent, RobotAgent):
                        containsObstacle = True
                        break
                
                if not containsObstacle:
                    contents[0].realNeighbors.append(self.grid.get_cell_list_contents(neighbor)[0])





        

    def step(self):
        '''Advance the model by one step.'''

        for agent in self.grid.get_cell_list_contents(self.boxDst):
            if isinstance(agent, BoxAgent) and agent.unique_id not in self.boxesInPlace:
                self.boxesInPlace.append(agent.unique_id)


        if len(self.boxesInPlace) == self.numBoxes:
            self.running = False
        
        #change box destination if box destination has 5 boxes
        count = 0
        for agent in self.grid.get_cell_list_contents(self.boxDst):
            if isinstance(agent, BoxAgent):
                count += 1
        
        if count == 5:
            self.changeBoxDst()
        
        if not self.startTime:
            self.startTime = time.time()
        
        
        
        
        self.schedule.step()