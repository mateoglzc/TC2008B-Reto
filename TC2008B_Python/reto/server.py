from model import TrafficModel, CarAgent, TrafficLightAgent, Road, Obstacle, Destination
from mesa.visualization.modules import CanvasGrid, PieChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# Hello comment

directions = {"down": 0, "up": 180, "left": 90, "right": 270}

def agent_portrayal(agent):
    """Function that defines how each Agent is going to be portrayed visualy"""
    portrayal = {"Shape": "circle",
                 "Filled": True,
                 "Layer": 0}

    if isinstance(agent, CarAgent):
        portrayal["Color"] = "blue"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    
    elif isinstance(agent, TrafficLightAgent):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = agent.state
        portrayal["r"] = 0.8
        portrayal["Layer"] = 1
    
    elif isinstance(agent, Road):
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        if agent.directions == directions["right"]:
            portrayal["Color"] = "#850278" # PURPLE
        elif agent.directions == directions["left"]:
            portrayal["Color"] = "#FED3FA" # LIGHT PINK
        elif agent.directions == directions["up"]:
            portrayal["Color"] = "#D9F818" # YELLOW
        elif agent.directions == directions["down"]:
            portrayal["Color"] = "#FC5CED" # HOT PINK
        
        portrayal["Color"] = "grey"
    
    elif isinstance(agent, Obstacle):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
    
    elif isinstance(agent, Destination):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9

    

    return portrayal


modelParams = { "numCars": UserSettableParameter("slider", "Number of Cars", value=1, min_value=1, max_value=11, step=1),
                "seed": UserSettableParameter("slider", "Seed", value=1, min_value=1, max_value=1000, step=1)}

grid = CanvasGrid(agent_portrayal, 26, 26, 494, 494)

server = ModularServer(TrafficModel,
                       [grid],
                       "Traffic Simulation",
                       modelParams)

server.port = 8521 # The default
server.launch()
