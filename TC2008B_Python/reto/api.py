from flask import Flask, jsonify, session, request
import model
import os

app = Flask("RetoTC2008B")
app.config['SECRET_KEY'] = "21973489274861289364"
port = int(os.getenv('PORT', 8000))
global mdl

@app.route('/test', methods=["GET"])
def test() -> str:
    """Test Connection"""
    return "Connection Established"

@app.route('/config', methods=["POST"])
def config() -> str:
    """Recieve model configuration and create model"""
    global mdl
    numCars = int(request.form.get("numCars"))
    mdl = model.TrafficModel(numCars)
    return "Configuration Successful"

@app.route("/makeStep")
def step() -> str:
    global mdl
    if mdl.running:
        mdl.step()
        return "Step Succesful"
    return "Finished Simulation"

@app.route('/getCars')
def getCars():
    """Get Car Agents"""
    global mdl
    model = mdl
    return jsonify({"Items" : model.getCars()})

@app.route('/getTL')
def getTrafficLights():
    """Get Traffic Lights"""
    global mdl
    model = mdl
    return jsonify({"Items" : model.getTrafficLights()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run()