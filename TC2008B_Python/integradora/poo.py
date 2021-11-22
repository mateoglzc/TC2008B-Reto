from flask import Flask, jsonify
# from flask import render_template, url_for, redirect, jsonify, request
import random

app = Flask("Wall-E API")
app.config['SECRET_KEY'] = "peepeePooPoo"

def makeJson() -> dict:
    return {"x" : random.randint(0, 50),
            "y" : 0, 
            "z" : random.randint(0, 50)}

posAgents = []
carryBox = []
posBox = []

for i in range(5):
    posAgents.append(makePoint())
    if random.randint(0,1) == 1:
        carryBox.append(True)
    else:
        carryBox.append(False)
    posBox.append(makePoint())

# print(posAgents, carryBox, posBox)

@app.route('/')
def default():
    """ Test Connection"""
    return "Connection Established Successfully"

@app.route("/config", methods=['POST'])
def config():
    """Recieve Confimation"""
    print("Message Received")
    return "Message Received"

@app.route("/getAgents", methods=["GET"])
def update():
    """Send Agent Information"""
    return jsonify({"Items" : posAgents})

@app.route("/getBoxes", methods=["GET"])
def update():
    """Send Box Information"""
    return jsonify({"Items" : posAgents})


if __name__ == "__main__":
    app.run(debug=True)