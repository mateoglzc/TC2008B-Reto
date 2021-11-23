from flask import Flask, jsonify, request
import random

app = Flask("Wall-E API")
app.config['SECRET_KEY'] = "peepeePooPoo"

def makeJson() -> dict:
    return {"x" : random.randint(0, 9) + 0.5,
            "y" : 0.5, 
            "z" : random.randint(0, 9) + 0.5,
            "direction": "north",
            "carryBox" : False}

posAgents = []
posBoxes = []
numAgents = 0

for i in range(5):
    posAgents.append(makeJson())

@app.route('/')
def default() -> str:
    """ Test Connection"""
    return "Connection Established Successfully"

@app.route("/config", methods=['POST'])
def config():
    """Recieve Confimation"""
    print("Message Received")
    return "Message Received"

@app.route("/getAgents", methods=["GET"])
def getAgents():
    """Send Agent Information"""
    global numAgents
    numAgents = int(request.form.get("numAgents"))
    return jsonify({"Items" : posAgents})

@app.route("/getBoxes", methods=["GET"])
def getBoxes():
    """Send Box Information"""
    return jsonify({"Items" : posBoxes})


if __name__ == "__main__":
    app.run(debug=True)