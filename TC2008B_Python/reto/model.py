# Class definition for Model to be used in the simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from mesa.time import SimultaneousActivation, RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import CarAgent, TrafficLightAgent, Road, Obstacle, Destination
from mesa.datacollection import DataCollector
import time, json

directions = {"down": [0], "up": [180], "left": [90], "right": [270], "up_left": [180, 90], "up_right" : [180, 270], "down_right" : [0, 270], "down_left" : [0, 90]}
trafficLightDirections = {"l": [90], "L": [90], "r": [270], "R": [270], "u": [180], "U": [180], "b": [0], "B": [0]}

def compatible(road: Road, roadB: Road):
        nx, ny = roadB.pos
        rx, ry = road.pos
        if road.directions == directions["up_left"]:
            if nx > rx and ny == ry:
                return False
                
            if ny < ry:
                return False
            
            if nx > rx and ny > ry and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False
            
            return True
        
        elif road.directions == directions["up_right"]:
            if nx < rx and ny == ry:
                return False
                
            if ny < ry:
                return False
            
            if nx < rx and ny > ry and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False
            
            return True
        
        elif road.directions == directions["down_right"]:
            if nx < rx and ny == ry:
                return False
                
            if ny > ry:
                return False
            
            if nx < rx and ny < ry and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False
            
            return True

        elif road.directions == directions["down_left"]:
            if nx > rx and ny == ry:
                return False
                
            if ny > ry:
                return False
            
            if nx > rx and ny < ry and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False
            
            return True


        elif road.directions == directions["right"]:
            if nx < rx: # if neighbor is to the left
                return False
            
            if nx == rx and ny != ry: # if neighbor is above or below
                return False
                        
            if nx > rx and ny < ry and roadB.directions == directions["up"]: # if neighbor is to the right, below and is facing up
                return False
            
            if ny != ry and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False
            
            return True
        
        elif road.directions == directions["down"]:
            if ny > ry: # if neighbor is above
                return False
            
            if ny == ry and nx != rx: # if neighbor is to the left or right
                return False
            
            if nx < rx and ny < ry and roadB.directions == directions["right"]: # if neighbor is to the left, below and facing right
                return False
            
            if nx != rx and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False
            
            return True

        elif road.directions == directions["left"]:
            if nx > rx: # if neighbor is to the right
                return False
            
            if nx == rx and ny != ry: # if neighbor is above or below
                return False
            
            if nx < rx and ny > ry and roadB.directions == directions["down"]:
                return False
            
            if ny != ry and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False
            
            return True

        else:
            if ny < ry: # if neighbor is below
                return False
            
            if ny == ry and nx != rx: # if neighbor is to the left or right
                return False
            
            if nx > rx and ny > ry and roadB.directions == directions["left"]: # if neighbor is to the right, above and facing left
                return False
            
            if nx != rx and [1 for i in road.model.grid.get_cell_list_contents(roadB.pos) if isinstance(i, TrafficLightAgent)]:
                return False

            return True

class TrafficModel(Model):
    """ Model for Traffic simulation """
    def __init__(self, numCars=11, seed=None):
        self.numCars = numCars
        self.running = True # For visualization
        self.startTime = None # For keeping track of time
        self.timeLimit = 180
        self.datacollector = DataCollector({
            "Moves": lambda m: {agent.unique_id: agent.numMoves for agent in m.schedule.agents if isinstance(agent, CarAgent)},
            "Total Time": lambda m: time.time() - m.startTime
        })

        self.destinations = set()
        self.allRoads = set()
        trafficLights = set()
        dataDictionary = json.load(open("mapDictionary.txt", encoding="utf-8-sig"))

        # create model using base1.txt as the template
        with open('base1.txt', encoding="utf-8-sig") as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = SimultaneousActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in "v^><↖↗↘↙":
                        agent = Road(f"r{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.allRoads.add(agent)
                        self.schedule.add(agent)
                    elif col in "lrubLRUB":
                        agent = Road(f"r{r*self.width+c}", self, trafficLightDirections[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.allRoads.add(agent)
                        self.schedule.add(agent)
                        agent = TrafficLightAgent(f"tl{r*self.width+c}", self, dataDictionary[col], agent.directions[0]-180)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        trafficLights.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.add(agent.pos)
                        self.schedule.add(agent)
        

        roads = self.allRoads.copy()
        destinations = self.destinations.copy()
        for i in range(self.numCars):
            dst = self.random.choice(list(destinations)) # choose random destination
            destinations.remove(dst) # remove it from possible destinations
            agent = CarAgent(i+1, self, dst) # create car agent with id, model, destination
            carPos = self.random.choice(list(roads)) # give car random road position
            while len(carPos.directions) > 1:
                carPos = self.random.choice(list(roads))
            
            roads.remove(carPos) # remove road from all roads
            agent.direction = carPos.directions[0] # update car direction
            self.grid.place_agent(agent, carPos.pos) # place agent in grid
            self.schedule.add(agent) # add agent to schedule


    def updateNeighbors(self):
        """Function to calculate the road and destination neighbors not including obstacles"""
        for road in self.allRoads: # iterate through every road tile
            #road.realNeighbors = []
            possible = self.grid.get_neighborhood(road.pos, True, False)
            for neighbor in possible:
                n_agent = self.grid.get_cell_list_contents(neighbor)[0]
                containsObstacle = False
                if isinstance(n_agent, Obstacle):
                    containsObstacle = True

                elif isinstance(n_agent, Destination):
                    containsObstacle = True

                elif not isinstance(n_agent, Destination) and not compatible(road, n_agent):
                    containsObstacle = True

                if not containsObstacle:
                    road.realNeighbors.append(n_agent)
        
        for dst in self.destinations:
            dst_a = self.grid.get_cell_list_contents(dst)[0]
            possible = self.grid.get_neighborhood(dst, False, False)
            for neighbor in possible:
                n_agent = self.grid.get_cell_list_contents(neighbor)[0]
                containsObstacle = False
                if isinstance(n_agent, Obstacle):
                    containsObstacle = True

                if not containsObstacle:
                    dst_a.realNeighbors.append(n_agent)
    

    def stopRunning(self):
        """Function to end simulation and print data collected in the last step of the simulation"""
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
        
        count = 0
        for dst in self.destinations:
            if self.grid.get_cell_list_contents(dst)[0].hasCar:
                count += 1

        if time.time() - self.startTime >= self.timeLimit or count == self.numCars:
            self.stopRunning()
            
        self.schedule.step()

    def getCars(self):
        """Build Json object which represents each Car Agent"""
        cars = [(agnt.unique_id, (x, y, agnt.direction)) for content, x, y in self.grid.coord_iter() for agnt in content if isinstance(agnt, CarAgent)]
        cars.sort(key=lambda x : x[0])
        carJson = [{"x" : car[1][0], "y" : 0, "z" : car[1][1], "direction" : car[1][2]} for car in cars]
        print(carJson)
        return carJson

    def getTrafficLights(self):
        """Build Json object which represents each Traffic Light Agent"""
        trafficLights = [(agnt.unique_id, (x, y, agnt.state, agnt.direction)) for content, x, y in self.grid.coord_iter() for agnt in content if isinstance(agnt, TrafficLightAgent)]
        trafficLights.sort(key=lambda x : x[0])
        trafficLightJson = [{"x" : tl[1][0], "y" : 0, "z" : tl[1][1], "state" : tl[1][2], "direction" : tl[1][3]} for tl in trafficLights]
        return trafficLightJson
