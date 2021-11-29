from model import WarehouseModel, CarAgent, TrafficLightAgent, Road, Obstacle, Destination
from mesa.visualization.modules import CanvasGrid, PieChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

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
        if agent.direction == directions["right"]:
            portrayal["Color"] = "#850278" # PURPLE
        elif agent.direction == directions["left"]:
            portrayal["Color"] = "#FED3FA" # LIGHT PINK
        elif agent.direction == directions["up"]:
            portrayal["Color"] = "#D9F818" # YELLOW
        elif agent.direction == directions["down"]:
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


modelParams = {}

grid = CanvasGrid(agent_portrayal, 26, 26, 500, 500)

server = ModularServer(WarehouseModel,
                       [grid],
                       "Box Stacking Robot",
                       modelParams)

server.port = 8521 # The default
server.launch()
