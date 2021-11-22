from flask import Flask
from flask import render_template, url_for, redirect, jsonify, request
import random

app = Flask("Wall-E API")
app.config['SECRET_KEY'] = "peepeePooPoo"

def makePoint() -> dict:
    return {"x" : random.randint(0, 50), "y" : random.randint(0, 50), "z" : 0}

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

@app.route("/update", methods=["GET"])
def update():
    """Send Agent Information"""
    return jsonify({"Items" : posAgents})


if __name__ == "__main__":
    app.run(debug=True)