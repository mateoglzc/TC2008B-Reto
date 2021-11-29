# Class definition for Model to be used in the simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import CarAgent, TrafficLightAgent, Road, Obstacle, Destination
from mesa.datacollection import DataCollector
import time, json

directions = {"down": 0, "up": 180, "left": 90, "right": 270}
trafficLightDirections = {"l": 90, "L": 90, "r": 270, "R": 270, "u": 180, "U": 180, "b": 0, "B": 0}

def compatible(road: Road, roadB: Road):
        nx, ny = roadB.pos
        rx, ry = road.pos
        if road.direction == directions["right"]:
            if nx < rx: # if neighbor is to the left
                return False
            
            if nx == rx and ny != ry: # if neighbor is above or below
                return False
                        
            if nx > rx and ny < ry and roadB.direction == directions["up"]: # if neighbor is to the right, below and is facing up
                return False
            
            return True
        
        if road.direction == directions["down"]:
            if ny > ry: # if neighbor is above
                return False
            
            if ny == ry and nx != rx: # if neighbor is to the left or right
                return False
            
            if nx < rx and ny < ry and roadB.direction == directions["right"]: # if neighbor is to the left, below and facing right
                return False
            
            return True

        if road.direction == directions["left"]:
            if nx > rx: # if neighbor is to the right
                return False
            
            if nx == rx and ny != ry: # if neighbor is above or below
                return False
            
            if nx < rx and ny > ry and roadB.direction == directions["down"]:
                return False
            
            return True

        else:
            if ny < ry: # if neighbor is below
                return False
            
            if ny == ry and nx != rx: # if neighbor is to the left or right
                return False
            
            if nx > rx and ny > ry and roadB.direction == directions["left"]: # if neighbor is to the right, above and facing left
                return False

            return True

class WarehouseModel(Model):
    """ Model for Roomba simulation """
    def __init__(self, numCars=1):
        self.numCars = numCars
        self.running = True # For visualization
        self.startTime = None # For keeping track of time
        self.timeLimit = 180
        self.datacollector = DataCollector({
            "Moves": lambda m: {agent.unique_id: agent.numMoves for agent in m.schedule.agents if isinstance(agent, CarAgent)},
            "Total Time": lambda m: time.time() - m.startTime
        })

        destinations = set()
        trafficLights = set()
        self.allRoads = set()
        dataDictionary = json.load(open("mapDictionary.txt"))


        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = SimultaneousActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r{r*self.width+c}", self, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.allRoads.add(agent)
                    elif col in "lrubLRUB":
                        agent = Road(f"r{r*self.width+c}", self, trafficLightDirections[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.allRoads.add(agent)
                        agent = TrafficLightAgent(f"tl{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        trafficLights.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        destinations.add(agent.pos)
            
            
        roads = self.allRoads
        for i in range(numCars):
            dst = self.random.choice(list(destinations))
            destinations.remove(dst)
            agent = CarAgent(i+1, self, dst)
            carPos = self.random.choice(list(roads))
            roads.remove(carPos)
            agent.direction = carPos.direction
            self.grid.place_agent(agent, carPos.pos)
            self.schedule.add(agent)


    def updateNeighbors(self):
        
        for road in self.allRoads: # iterate through every road tile
            road.realNeighbors = []
            possible = self.grid.get_neighborhood(road.pos, True, False)
            for neighbor in possible:
                n_agent = self.grid.get_cell_list_contents(neighbor)[0]
                containsObstacle = False
                if isinstance(n_agent, Obstacle):
                    containsObstacle = True

                elif not compatible(road, n_agent):
                    containsObstacle = True

                if not containsObstacle:
                    road.realNeighbors.append(n_agent)
    

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

        if time.time() - self.startTime >= self.timeLimit:
            self.stopRunning()
            
        self.schedule.step()