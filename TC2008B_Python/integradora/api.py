from flask import Flask, jsonify, request
from model import WarehouseModel, RobotAgent, BoxAgent, BoxDestination, TileAgent
import random

app = Flask("Wall-E API")
app.config['SECRET_KEY'] = "peepeePooPoo"

model = None

@app.route('/')
def default() -> str:
    """ Test Connection"""
    return "Connection Established Successfully"

@app.route("/config", methods=['POST'])
def config():
    """Recieve Confimation"""
    global model
    numAgents = int(request.form.get("numAgents"))
    numBoxes = int(request.form.get("numBoxes"))
    model  = WarehouseModel(10,10, numAgents, numBoxes)
    return "Message Received, Model Created"

@app.route("/makeStep")
def step():
    """Step"""
    global model
    if model.running:
        model.step()
        return "Step Made"
    return "Model finished"

@app.route("/getAgents", methods=["GET"])
def getAgents():
    """Send Agent Information"""
    global model
    posAgents = model.getRobots()
    return jsonify({"Items" : posAgents})

@app.route("/getBoxes", methods=["GET"])
def getBoxes():
    """Send Box Information"""
    global model
    posBoxes = model.getBoxes()
    return jsonify({"Items" : posBoxes})


if __name__ == "__main__":
    app.run(debug=True)