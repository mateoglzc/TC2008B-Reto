from model import WarehouseModel, RobotAgent, BoxAgent, BoxDestination
from mesa.visualization.modules import CanvasGrid, PieChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    """Function that defines how each Agent is going to be portrayed visualy"""
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0}

    if isinstance(agent, RobotAgent):
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
    
    elif isinstance(agent, BoxDestination):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
    

    return portrayal


modelParams = {
    "width": 10,
    "height": 10,
    "numBoxes": UserSettableParameter("slider",
                                        name="Number of Boxes",
                                        value=5,
                                        min_value=1,
                                        max_value=10)}

grid = CanvasGrid(agent_portrayal, modelParams["width"], modelParams["height"], 500, 500)

server = ModularServer(WarehouseModel,
                       [grid],
                       "Box Stacking Robot",
                       modelParams)

server.port = 8521 # The default
server.launch()