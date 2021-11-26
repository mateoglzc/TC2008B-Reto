from model import WarehouseModel, CarAgent, BoxAgent, CarDestination, TileAgent
from mesa.visualization.modules import CanvasGrid, PieChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter



def agent_portrayal(agent):
    """Function that defines how each Agent is going to be portrayed visualy"""
    portrayal = {"Shape": "circle",
                 "Filled": True,
                 "Layer": 0}

    if isinstance(agent, CarAgent):
        portrayal["Color"] = "red"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
        if agent.hasBox:
            portrayal["Color"] = "green"
    
    elif isinstance(agent, BoxAgent):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "#944300"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    
    elif isinstance(agent, CarDestination):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
    
    if isinstance(agent, TileAgent):
        portrayal["Filled"] = False
    

    return portrayal


modelParams = {
    "width": 10,
    "height": 10,
    "seed": UserSettableParameter("slider",
                                        name="Seed",
                                        value=5,
                                        min_value=1,
                                        max_value=1000),
    "numBoxes": UserSettableParameter("slider",
                                        name="Number of Boxes",
                                        value=5,
                                        min_value=1,
                                        max_value=30),
    "numRobots": UserSettableParameter("slider",
                                        name="Number of Robots",
                                        value=1,
                                        min_value=1,
                                        max_value=5)}

grid = CanvasGrid(agent_portrayal, modelParams["width"], modelParams["height"], 500, 500)

server = ModularServer(WarehouseModel,
                       [grid],
                       "Box Stacking Robot",
                       modelParams)

server.port = 8521 # The default
server.launch()
