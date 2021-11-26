# Class definition for Model to be used in the simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import CarAgent, BoxAgent, CarDestination, TileAgent
from mesa.datacollection import DataCollector
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
        self.timeLimit = 180
        self.boxDst = (self.random.randint(0, width-1), self.random.randint(0, height-1))
        self.boxesInPlace = []
        self.prevDsts = []
        self.datacollector = DataCollector({
            "Moves": lambda m: {agent.unique_id: agent.numMoves for agent in m.schedule.agents if isinstance(agent, CarAgent)},
            "Total Time": lambda m: time.time() - m.startTime
        })

        # add tile agents to every cell in grid
        id = 0
        for i in range(width):
            for j in range(height):
                a = TileAgent(id, self)
                id += 1
                self.schedule.add(a)
                self.grid.place_agent(a, (i, j))
        
        a = CarDestination(-1, self)
        self.schedule.add(a)
        self.grid.place_agent(a, self.boxDst)
        
        # Add box agents to grid
        for i in range(self.numBoxes):
            a = BoxAgent(1000+i, self) # create instance of box agent
            self.schedule.add(a) # add it to the schedule

            randomPos = (self.random.randint(0, width-1), self.random.randint(0, height-1)) # generate a random position
            contains = True
            while contains: # generate a new randomPos while there is a BoxAgent in randomPos
                contains = False
                agents_in_cell = self.grid.get_cell_list_contents([randomPos])
                for agent in agents_in_cell:
                    if isinstance(agent, BoxAgent) or isinstance(agent, CarAgent):
                        randomPos = (self.random.randint(0, width-1), self.random.randint(0, height-1))
                        contains = True
                        break

            self.grid.place_agent(a, randomPos) # place DirtyAgent in randomPos that isn't already dirty

        # add robot agents to the gird
        for i in range(self.numRobots):
            a = CarAgent(2000+i, self, self.boxDst) #create instance of RobotAngent with unique id starting from 1000
            a.boxDst = self.boxDst
            self.schedule.add(a) # add it to the schedule
            randomPos = (self.random.randint(0, width-1), self.random.randint(0, height-1)) # generate a random position
            contains = True
            while contains > 0: # generate a new randomPos while there is an Agent in randomPos
                contains = False
                agents_in_cell = self.grid.get_cell_list_contents([randomPos])
                for agent in agents_in_cell:
                    if isinstance(agent, BoxAgent) or isinstance(agent, CarAgent):
                        randomPos = (self.random.randint(0, width-1), self.random.randint(0, height-1))
                        contains = True
                        break
            
            self.grid.place_agent(a, randomPos) # place robot at random position
        
    
    def changeBoxDst(self):
        dstNeighbors = self.grid.get_cell_list_contents([self.boxDst])[0].realNeighbors
        accessible = []
        for neighbor in dstNeighbors:
            if len(neighbor.realNeighbors) != 0: # if neighbor is accessible
                accessible.append(neighbor)


        if len(accessible) > 0: # choose a random neighbor that is accessible
            newBoxDst = self.random.choice(accessible).pos

        else: # if none are accessible
            # move to a random position in the grid
            newBoxDst = (self.random.randint(0, self.grid.width-1), self.random.randint(0, self.grid.height-1))
            while newBoxDst in self.prevDsts:
                newBoxDst = (self.random.randint(0, self.grid.width-1), self.random.randint(0, self.grid.height-1))

        for agent in self.schedule.agents:
            if isinstance(agent, CarAgent):
                agent.boxDst = newBoxDst
            if isinstance(agent, CarDestination):
                self.grid.move_agent(agent, newBoxDst)
        
        self.prevDsts.append(self.boxDst)
        self.boxDst = newBoxDst
    
    def updateNeighbors(self):
        
        for (contents, x, y) in self.grid.coord_iter(): # iterate through each cell
            contents[0].realNeighbors = []
            possible = self.grid.get_neighborhood((x, y), False)
            for neighbor in possible: # iterate through each cell neighbor
                containsObstacle = False
                for agent in self.grid.get_cell_list_contents(neighbor): # iterate through each agent in neighbor
                    if isinstance(agent, BoxAgent) or isinstance(agent, CarAgent):
                        containsObstacle = True
                        break
                
                if not containsObstacle:
                    contents[0].realNeighbors.append(self.grid.get_cell_list_contents(neighbor)[0])


    
    def getRobots(self) -> list:
        robotJson = []
        l = [(agnt.unique_id, (x, y, agnt.direction, agnt.hasBox)) for content, x, y in self.grid.coord_iter() for agnt in content if isinstance(agnt, CarAgent)]
        l.sort(key= lambda x : x[0])
        for robot in l:
            temp = {"x" : robot[1][0] + 0.5, "y" : 0.3, "z" : robot[1][1] + 0.5, "direction" : robot[1][2], "carryBox" : robot[1][3]}
            robotJson.append(temp)
        return robotJson


    def getBoxes(self) -> list:
        boxJson = []
        l = [(agnt.unique_id, (x, y)) for content, x, y in self.grid.coord_iter() for agnt in content if isinstance(agnt, BoxAgent)]
        l.sort(key= lambda x : x[0])

        i = 0
        for j in range(1000, 1000 + self.numBoxes):
            if i < len(l) and l[i][0] == j:
                temp = {"x" : l[i][1][0] + .305, "y" : 0, "z" : l[i][1][1] + .695, "active" : True}
                i += 1
            else:
                temp = {"x" : -1 + .305, "y" : 0, "z" : -1 + .695, "active" : False}
            boxJson.append(temp)
        return boxJson
    

    def stopRunning(self):
        self.running = False
        df = self.datacollector.get_model_vars_dataframe()
        
        agentMoves = ""
        for key, value in df.iat[-1, 0].items():
            agentMoves += f"Agent {key}: {value} moves\n"


        totalTime = f"Time Elapsed: {df.iat[-1, 1]} seconds"

        print(totalTime)
        print(agentMoves)


    def step(self):
        '''Advance the model by one step.'''
        
        if not self.startTime:
            self.startTime = time.time()

        self.datacollector.collect(self)

        for agent in self.grid.get_cell_list_contents(self.boxDst):
            if isinstance(agent, BoxAgent) and agent.unique_id not in self.boxesInPlace:
                self.boxesInPlace.append(agent.unique_id)


        if len(self.boxesInPlace) == self.numBoxes or time.time() - self.startTime >= self.timeLimit:
            self.stopRunning()

        
        #change box destination if box destination has 5 boxes
        count = 0
        for agent in self.grid.get_cell_list_contents(self.boxDst):
            if isinstance(agent, BoxAgent):
                count += 1
        
        if count >= 5:
            self.changeBoxDst()
                
        
        
        self.schedule.step()