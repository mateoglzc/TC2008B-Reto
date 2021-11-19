# Class definition for Model to be used in the simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import RobotAgent, BoxAgent, BoxDestination
import random
import time


class WarehouseModel(Model):
    """ Model for Roomba simulation """
    def __init__(self,  width, height, numRobots=1, numBoxes=5):
        self.numRobots = numRobots
        self.numBoxes = numBoxes
        self.grid = MultiGrid(width, height, False) #No torus
        self.schedule = RandomActivation(self)
        self.running = True # For visualization
        self.startTime = None # For keeping track of time
        self.boxDst = (random.randint(0, width-1), random.randint(0, height-1))
        self.boxesInPlace = None

        a = BoxDestination(-1, self)
        self.schedule.add(a)
        self.grid.place_agent(a, self.boxDst)
        
        # Add dirty agents to grid
        for i in range(self.numBoxes):
            a = BoxAgent(i, self) # create instance of dirty agent
            self.schedule.add(a) # add it to the schedule

            randomPos = (random.randint(0, width-1), random.randint(0, height-1)) # generate a random position
            count = 1
            while count > 0: # generate a new randomPos while there is a DirtyAgent in randomPos
                count = 0
                agents_in_cell = self.grid.get_cell_list_contents([randomPos])
                for agent in agents_in_cell:
                    if isinstance(agent, BoxAgent):
                        randomPos = (random.randint(0, width-1), random.randint(0, height-1))
                        count += 1

            self.grid.place_agent(a, randomPos) # place DirtyAgent in randomPos that isn't already dirty

        for i in range(self.numRobots):
            a = RobotAgent(i+1000, self, self.boxDst) #create instance of RoombaAngent with unique id starting from 1000
            a.boxDst = self.boxDst
            self.schedule.add(a) # add it to the schedule
            
            self.grid.place_agent(a, (1, 1)) # place all Roombas at pos (1, 1)
        
    
    def changeBoxDst(self):
        # move Box destination to the right
        if self.boxDst[0] < self.grid.width-1:
            newBoxDst = (self.boxDst[0] + 1, self.boxDst[1])
        
        # move Box destination to the left
        elif self.boxDst[0] == self.grid.width-1:
            newBoxDst = (self.boxDst[0] - 1, self.boxDst[1])
        
        # move Box destination up
        elif self.boxDst[1] < self.grid.height-1:
            newBoxDst = (self.boxDst[0], self.boxDst[1] + 1)
        
        # move Box destination down
        elif self.boxDst[1] == self.grid.height-1:
            newBoxDst = (self.boxDst[0], self.boxDst[1] - 1)
        

        for agent in self.schedule.agents:
            if isinstance(agent, RobotAgent):
                agent.boxDst = newBoxDst
            elif isinstance(agent, BoxDestination):
                self.grid.move_agent(agent, newBoxDst)
            elif isinstance(agent, BoxAgent):
                agent.prevDsts.append(self.boxDst)
        
        self.boxDst = newBoxDst
        

    def step(self):
        '''Advance the model by one step.'''

        count = 0

        for agent in self.grid.get_cell_list_contents(self.boxDst):
            if isinstance(agent, BoxAgent):
                count += 1
                self.boxesInPlace = len(agent.prevDsts)*5 + count



        if self.boxesInPlace == self.numBoxes:
            self.running = False
        
        #change box destination if box destination has 5 boxes
        if count == 5:
            self.changeBoxDst()
        



        if not self.startTime:
            self.startTime = time.time()
        
        self.schedule.step()