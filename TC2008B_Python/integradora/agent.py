from mesa import Agent

class RobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        pass

    def step(self):
        pass

class BoxAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class WallAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class TileAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)